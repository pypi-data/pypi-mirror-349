from __future__ import annotations

##############################################################################
#  Imports & logger                                                          #
##############################################################################
import logging, sys

logging.basicConfig(
    level=logging.INFO,  # allow INFO and above
    stream=sys.stdout,  # send to notebook output
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    force=True)  # override Databricks defaults

import importlib, searchpubmed.pubmed as pubmed

importlib.reload(pubmed)

import re
import time
import xml.etree.ElementTree as ET
from math import ceil
from typing import List, Dict, Tuple, Union, Pattern

import dateparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, RequestException

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_pmid_from_pubmed(
    query: str,
    *,
    retmax: int = 2_000,
    api_key: str | None = None,
    timeout: int = 20,
    max_retries: int = 5,
    delay: float = 0.34,
) -> list[str]:
    """
    ------------------------------------------------------------------------
    Return a list of PubMed IDs (PMIDs) for an arbitrary search expression.
    ------------------------------------------------------------------------

    Parameters
    ----------
    query : str
        Any valid PubMed search term (Boolean logic, field tags, etc.).
    retmax : int, default 2 000
        Maximum number of PMIDs to retrieve (ESearch hard-cap = 100 000).
    api_key : str | None, optional
        NCBI API key – raises the personal rate limit to ~10 req s⁻¹.
    timeout : int, default 20 s
        Socket timeout for the HTTP request.
    max_retries : int, default 5
        How many times to retry on HTTP 429 or 5xx errors.
    delay : float, default 0.34 s
        Base pause between successive retries (doubles each attempt).

    Returns
    -------
    list[str]
        Unique PMIDs (as strings).  Empty list if the query matches none or
        if all retries fail.

    Notes
    -----
    *   The function is deliberately lightweight – no pandas dependency.
    *   It logs its progress and failures through the *logging* module; hook
        this into your existing logger configuration if needed.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "xml",
    }
    if api_key:
        params["api_key"] = api_key

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(base_url, data=params, timeout=timeout)
            resp.raise_for_status()
            break  # success
        except HTTPError as e:
            status = getattr(e.response, "status_code", None)
            if status and (status == 429
                           or 500 <= status < 600) and attempt < max_retries:
                wait = delay * (2**(attempt - 1))
                logger.warning(
                    f"ESearch HTTP {status}; retry {attempt}/{max_retries} in {wait:.1f}s"
                )
                time.sleep(wait)
                continue
            logger.error(f"ESearch failed (HTTP {status}): {e}")
            return []
        except RequestException as e:
            logger.error(f"ESearch network error: {e}")
            return []

    try:
        xml_payload = getattr(resp, "content", None) or resp.text
        root = ET.fromstring(xml_payload)
        pmids = [
            id_el.text for id_el in root.findall(".//IdList/Id") if id_el.text
        ]
        # Deduplicate while preserving order
        seen: set[str] = set()
        return [p for p in pmids if not (p in seen or seen.add(p))]
    except ET.ParseError as e:
        logger.error(f"ESearch XML parse error: {e}")
        return []


##############################################################################
#  Utility: PMID → PMCID mapping                                             #
##############################################################################
def map_pmids_to_pmcids(
    pmids: List[str],
    *,
    api_key: str | None = None,
    batch_size: int = 500,
    timeout: int = 20,
    max_retries: int = 5,
    delay: float = 0.34,
) -> pd.DataFrame:
    """
    ------------------------------------------------------------------------
    Map **PubMed IDs (PMIDs)** to **all** corresponding **PMC IDs (PMCIDs)**.
    ------------------------------------------------------------------------

    Parameters
    ----------
    pmids : list[str]
        PMIDs to map.  Duplicates are tolerated in the input.
    api_key : str | None, optional
        NCBI API key (raises personal limit to ≈10 req s⁻¹).
    batch_size : int, default 500
        Number of PMIDs sent per ELink request (hard cap = 2 000).
    timeout : int, default 20 s
        Socket timeout per HTTP request.
    max_retries : int, default 5
        Attempts per batch on HTTP-429 / 5xx before falling back to
        ``pmcid = <NA>`` for the affected PMIDs.
    delay : float, default 0.34 s
        Base pause between retries (exponential back-off).

    Returns
    -------
    pandas.DataFrame
        Columns
        ``pmid``   | string  
        ``pmcid``  | string  (``<NA>`` if no PMC record exists)

        The DataFrame contains **one row per unique (pmid, pmcid) pair**.

    Notes
    -----
    * Uses **ELink** (``dbfrom=pubmed``, ``db=pmc``) under the hood.
    * Rate-limit friendly (≤3 req s⁻¹ without key, ~10 req s⁻¹ with key).
    * XML parse errors on individual batches degrade gracefully to
      ``pmcid = <NA>`` for the PMIDs in that batch.
    """
    # ── Guard clause ────────────────────────────────────────────
    if not pmids:
        return pd.DataFrame(columns=["pmid", "pmcid"]).astype("string")

    base_elink = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
    session = requests.Session()
    records: list[tuple[str, str | None]] = []

    total_batches = ceil(len(pmids) / batch_size)

    for idx in range(total_batches):
        chunk = pmids[idx * batch_size:(idx + 1) * batch_size]

        # Build URL-encoded body once; add each PMID as a separate "id"
        data = [
            ("dbfrom", "pubmed"),
            ("db", "pmc"),
            ("retmode", "xml"),
        ]
        if api_key:
            data.append(("api_key", api_key))
        data.extend(("id", pmid) for pmid in chunk)

        logger.info("ELink batch %d/%d (size=%d)", idx + 1, total_batches,
                    len(chunk))

        # ── HTTP with retry ─────────────────────────────────────
        response = None
        for attempt in range(1, max_retries + 1):
            try:
                response = session.post(base_elink, data=data, timeout=timeout)
                if response.status_code == 429:
                    raise HTTPError(response=response)
                response.raise_for_status()
                break  # success
            except (HTTPError, RequestException) as exc:
                status = getattr(exc.response, "status_code", None)
                if status and (status == 429 or
                               500 <= status < 600) and attempt < max_retries:
                    wait = delay * (2**(attempt - 1))
                    logger.warning(
                        "Batch %d: HTTP %s, retry %d/%d in %.1fs",
                        idx + 1,
                        status,
                        attempt,
                        max_retries,
                        wait,
                    )
                    time.sleep(wait)
                    continue
                logger.error("Batch %d failed: %s", idx + 1, exc)
                break  # fall through

        # On total failure → all PMIDs in chunk get <NA>
        if response is None or not response.ok:
            records.extend((pmid, None) for pmid in chunk)
            continue

        # ── XML parse ──────────────────────────────────────────
        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as e:
            logger.error("XML parse error for batch %d: %s", idx + 1, e)
            records.extend((pmid, None) for pmid in chunk)
            time.sleep(delay)
            continue

        # ── Extract mappings ──────────────────────────────────
        for linkset in root.findall("LinkSet"):
            pmid_text = linkset.findtext("IdList/Id")
            if not pmid_text:
                continue
            pmcids = [
                link.text for db in linkset.findall("LinkSetDb")
                if db.findtext("DbTo") == "pmc"
                for link in db.findall("Link/Id") if link.text
            ]
            if pmcids:
                records.extend((pmid_text, pmcid) for pmcid in pmcids)
            else:  # preserve the PMID even if it lacks a PMC record
                records.append((pmid_text, None))

        time.sleep(delay)

    # Always deduplicate before returning
    df = (pd.DataFrame(records, columns=[
        "pmid", "pmcid"
    ]).astype("string").drop_duplicates(ignore_index=True))

    return df


def get_pubmed_metadata_pmid(
    pmids: List[str],
    *,
    api_key: str | None = None,
    batch_size: int = 200,
    timeout: int = 20,
    max_retries: int = 3,
    delay: float = 0.34,
) -> pd.DataFrame:
    """
    ------------------------------------------------------------------------
    Fetch structured PubMed metadata for an arbitrary list of PMIDs.
    ------------------------------------------------------------------------

    Parameters
    ----------
    pmids : list[str]
        PubMed IDs to retrieve.  Duplicates are tolerated and de-duplicated.
    api_key : str | None, optional
        NCBI API key (optional but recommended – lifts rate-limit to ≈10 req s⁻¹).
    batch_size : int, default 200
        PMIDs per EFetch request (ceiling = 10 000).
    timeout : int, default 20 s
        Socket timeout per HTTP call.
    max_retries : int, default 3
        Attempts per batch on HTTP-429 / 5xx before giving up.
    delay : float, default 0.34 s
        Base back-off (doubles each retry).

    Returns
    -------
    pandas.DataFrame
        Column               | dtype  | description
        ---------------------|--------|----------------------------------------
        pmid                 | string | PubMed identifier
        title                | string | Article title (sentence case)
        abstract             | string | Abstract (paragraphs joined)
        journal              | string | Full journal title
        publicationDate      | string | ISO-8601 date (YYYY-MM-DD / YYYY-MM)
        doi                  | string | Digital Object Identifier
        firstAuthor          | string | “Given Surname” of first author
        lastAuthor           | string | “Given Surname” of last author
        authorAffiliations   | string | “; ”-separated affiliations
        meshTags             | string | “, ”-separated MeSH descriptors
        keywords             | string | “, ”-separated author keywords

        Missing data are filled with the literal string ``"N/A"`` for
        type-stability.

    Notes
    -----
    * Only **one HTTP round-trip per *batch***; results are concatenated.
    * Parsing failures for individual articles degrade gracefully to rows
      filled with ``"N/A"``.
    """
    # ── Guard clause ────────────────────────────────────────────
    unique_pmids = list(dict.fromkeys(pmids))  # de-dup, keep order
    if not unique_pmids:
        return pd.DataFrame(columns=[
            "pmid",
            "title",
            "abstract",
            "journal",
            "publicationDate",
            "doi",
            "firstAuthor",
            "lastAuthor",
            "authorAffiliations",
            "meshTags",
            "keywords",
        ]).astype("string")

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    session = requests.Session()
    records: list[dict] = []

    # ── Helpers ─────────────────────────────────────────────────
    def _parse_pubdate(elem: ET.Element | None) -> str:
        if elem is None:
            return "N/A"
        y = elem.findtext("Year")
        m = elem.findtext("Month") or ""
        d = elem.findtext("Day") or ""
        if y and m:
            try:
                return dateparser.parse(
                    f"{y} {m} {d or '1'}").date().isoformat()
            except Exception:
                return "-".join(p for p in (y, m, d) if p)
        return elem.findtext("MedlineDate") or y or "N/A"

    def _fullname(author: ET.Element) -> str:
        fore = author.findtext("ForeName") or author.findtext("Initials") or ""
        last = author.findtext("LastName") or ""
        name = f"{fore} {last}".strip()
        return name or "N/A"

    # ── Main loop ───────────────────────────────────────────────
    for start in range(0, len(unique_pmids), batch_size):
        batch = unique_pmids[start:start + batch_size]
        params = {
            "db": "pubmed",
            "retmode": "xml",
            "id": ",".join(batch),
        }
        if api_key:
            params["api_key"] = api_key

        # ---- HTTP with retry ----------------------------------
        resp = None
        for attempt in range(1, max_retries + 1):
            try:
                resp = session.get(base_url, params=params, timeout=timeout)
                resp.raise_for_status()
                break
            except HTTPError as e:
                status = getattr(e.response, "status_code", None)
                if status and (status == 429 or
                               500 <= status < 600) and attempt < max_retries:
                    wait = delay * (2**(attempt - 1))
                    logger.warning(
                        f"Batch {start//batch_size+1}: HTTP {status}; retry in {wait:.1f}s "
                        f"(attempt {attempt}/{max_retries})")
                    time.sleep(wait)
                    continue
                logger.error(f"EFetch HTTP error for PMIDs {batch}: {e}")
                break
            except RequestException as e:
                logger.error(f"Network error for PMIDs {batch}: {e}")
                break

        if resp is None or not resp.ok:
            # total failure → placeholder rows
            for pmid in batch:
                records.append({
                    k: "N/A"
                    for k in ("title", "abstract", "journal",
                              "publicationDate", "doi", "firstAuthor",
                              "lastAuthor", "authorAffiliations", "meshTags",
                              "keywords")
                } | {"pmid": "N/A"})
            continue

        # ---- XML parse ----------------------------------------
        try:
            root = ET.fromstring(resp.content)
        except ET.ParseError as e:
            logger.error(f"XML parse error for PMIDs {batch}: {e}")
            for pmid in batch:
                records.append({
                    k: "N/A"
                    for k in ("title", "abstract", "journal",
                              "publicationDate", "doi", "firstAuthor",
                              "lastAuthor", "authorAffiliations", "meshTags",
                              "keywords")
                } | {"pmid": "N/A"})
            time.sleep(delay)
            continue

        # ---- Extract article info -----------------------------
        for art in root.findall(".//PubmedArticle"):
            pmid = art.findtext(".//PMID", default="N/A")

            title = art.findtext(".//ArticleTitle", default="N/A").strip()

            abstract = " ".join(t.text or "" for t in art.findall(
                ".//Abstract/AbstractText")).strip() or "N/A"

            journal = art.findtext(".//Journal/Title", default="N/A")

            pubdate_elem = art.find(".//JournalIssue/PubDate")
            publication_date = _parse_pubdate(pubdate_elem)

            doi = art.findtext('.//ArticleIdList/ArticleId[@IdType="doi"]',
                               default="N/A")

            authors = art.findall(".//AuthorList/Author")
            first_author = _fullname(authors[0]) if authors else "N/A"
            last_author = _fullname(authors[-1]) if authors else "N/A"

            affiliations = [
                aff.text for a in authors
                for aff in a.findall("AffiliationInfo/Affiliation") if aff.text
            ]
            author_affiliations = "; ".join(affiliations) or "N/A"

            mesh_tags = ", ".join(
                mh.text for mh in art.findall(".//MeshHeading/DescriptorName")
                if mh.text) or "N/A"

            keywords = ", ".join(
                kw.text for kw in art.findall(".//KeywordList/Keyword")
                if kw.text) or "N/A"

            records.append({
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "journal": journal,
                "publicationDate": publication_date,
                "doi": doi,
                "firstAuthor": first_author,
                "lastAuthor": last_author,
                "authorAffiliations": author_affiliations,
                "meshTags": mesh_tags,
                "keywords": keywords,
            })

        time.sleep(delay)

    return (pd.DataFrame(records).astype("string").sort_values(
        "pmid", ignore_index=True))


def get_pubmed_metadata_pmcid(
    pmcids: list[str],
    *,
    api_key: str | None = None,
    batch_size: int = 200,
    timeout: int = 20,
    max_retries: int = 3,
    delay: float = 0.34,
) -> pd.DataFrame:
    """
    Fetch structured metadata for one or many PubMed Central IDs (PMCIDs).

    Columns returned
    ----------------
    ``pmcid`` | string  
    ``pmid``  | string  
    ``title`` | string  
    ``abstract`` | string  
    ``journal`` | string  
    ``publicationDate`` | string (ISO-8601)  
    ``doi`` | string  
    ``firstAuthor`` | string  
    ``lastAuthor`` | string  
    ``authorAffiliations`` | string  
    ``meshTags`` | string  
    ``keywords`` | string
    """
    # ── Guard clause ────────────────────────────────────────────
    if not pmcids:
        cols = [
            "pmcid",
            "pmid",
            "title",
            "abstract",
            "journal",
            "publicationDate",
            "doi",
            "firstAuthor",
            "lastAuthor",
            "authorAffiliations",
            "meshTags",
            "keywords",
        ]
        return pd.DataFrame(columns=cols).astype("string")

    # Normalise IDs (“12345” → “PMC12345”)
    norm_ids = [
        pid if str(pid).upper().startswith("PMC") else f"PMC{pid}"
        for pid in pmcids
    ]
    unique_ids = list(dict.fromkeys(norm_ids))  # de-dup, keep order

    # Helpers ───────────────────────────────────────────────────
    def _strip_default_ns(xml_bytes: bytes) -> bytes:
        """Remove first xmlns=… to simplify tag addressing."""
        return re.sub(rb'\sxmlns="[^"]+"', b"", xml_bytes, count=1)

    def _fullname(author: ET.Element) -> str:
        fore = author.findtext("given-names") or author.findtext(
            "initials") or ""
        last = author.findtext("surname") or ""
        name = f"{fore} {last}".strip()
        return name or "N/A"

    # API plumbing ──────────────────────────────────────────────
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    session = requests.Session()
    records: list[dict] = []

    total_batches = ceil(len(unique_ids) / batch_size)
    for idx in range(total_batches):
        chunk = unique_ids[idx * batch_size:(idx + 1) * batch_size]
        params = {
            "db": "pmc",
            "id": ",".join(cid.removeprefix("PMC") for cid in chunk),
            "retmode": "xml",
        }
        if api_key:
            params["api_key"] = api_key

        # ── HTTP with retry ───────────────────────────────────
        resp = None
        for attempt in range(1, max_retries + 1):
            try:
                resp = session.get(base_url, params=params, timeout=timeout)
                resp.raise_for_status()
                break
            except requests.HTTPError as e:
                status = e.response.status_code
                if status in (429, *range(500, 600)) and attempt < max_retries:
                    wait = delay * (2**(attempt - 1))
                    logger.warning(
                        f"Batch {idx+1}: HTTP {status}; "
                        f"retry {attempt}/{max_retries} in {wait:.1f}s")
                    time.sleep(wait)
                    continue
                logger.error(f"Batch {idx+1}: HTTP error {e}")
                break
            except requests.RequestException as e:
                logger.error(f"Batch {idx+1}: network error {e}")
                break

        if resp is None or not resp.ok:
            # total failure → placeholder rows
            for cid in chunk:
                records.append({
                    "pmcid": cid,
                    **{
                        k: "N/A"
                        for k in ("pmid", "title", "abstract", "journal", "publicationDate", "doi", "firstAuthor", "lastAuthor", "authorAffiliations", "meshTags", "keywords")
                    }
                })
            continue

        # ── XML parse ─────────────────────────────────────────
        try:
            root = ET.fromstring(_strip_default_ns(resp.content))
        except ET.ParseError as e:
            logger.error(f"Batch {idx+1}: XML parse error {e}")
            for cid in chunk:
                records.append({
                    "pmcid": cid,
                    **{
                        k: "N/A"
                        for k in ("pmid", "title", "abstract", "journal", "publicationDate", "doi", "firstAuthor", "lastAuthor", "authorAffiliations", "meshTags", "keywords")
                    }
                })
            time.sleep(delay)
            continue

        # ── Extract per-article metadata ──────────────────────
        for art in root.findall(".//article"):
            pmcid = next(
                (art.findtext(f'.//article-id[@pub-id-type="{t}"]')
                 for t in ("pmcid", "pmc", "pmcid-ver", "pmcaid")
                 if art.find(f'.//article-id[@pub-id-type="{t}"]') is not None
                 ),
                "N/A",
            )
            if pmcid and "." in pmcid:
                pmcid = pmcid.split(".", 1)[0]
            if pmcid and not pmcid.upper().startswith("PMC"):
                pmcid = f"PMC{pmcid}"
            pmid = art.findtext('.//article-id[@pub-id-type="pmid"]',
                                default="N/A")
            title = (art.findtext(".//article-title", default="N/A")
                     or "").strip()

            # Abstract paragraphs joined
            abstract = " ".join(
                p.text or ""
                for p in art.findall(".//abstract//p")).strip() or "N/A"

            journal = art.findtext(".//journal-title", default="N/A")

            # Publication date (take <pub-date publication-format="electronic"> if present)
            pub_date_elem = (art.find('.//pub-date[@pub-type="epub"]')
                             or art.find('.//pub-date[@pub-type="pub"]')
                             or art.find(".//pub-date"))
            if pub_date_elem is not None:
                y = pub_date_elem.findtext("year") or ""
                m = pub_date_elem.findtext("month") or ""
                d = pub_date_elem.findtext("day") or ""
                publication_date = "-".join(p for p in (y, m, d) if p) or "N/A"
            else:
                publication_date = "N/A"

            doi = art.findtext('.//article-id[@pub-id-type="doi"]',
                               default="N/A")

            authors = art.findall(
                ".//contrib-group/contrib[@contrib-type='author']")
            first_author = _fullname(authors[0]) if authors else "N/A"
            last_author = _fullname(authors[-1]) if authors else "N/A"

            affiliations = [
                aff.text for aff in art.findall(".//aff") if aff.text
            ]
            author_affiliations = "; ".join(affiliations) or "N/A"

            # MeSH in JATS appears under <kwd-group kwd-group-type="MeSH">
            mesh_tags = ", ".join(  # modern kwd-group layout
                kw.text
                for kg in art.findall('.//kwd-group[@kwd-group-type="MeSH"]')
                for kw in kg.findall(".//kwd")
                if kw.text) or ", ".join(  # ← fallback for fixture
                    mh.text for mh in art.findall(
                        ".//mesh-heading-list/mesh-heading/descriptor-name")
                    if mh.text) or "N/A"

            # Author‐provided keywords → any kwd-group **without** @kwd-group-type
            keywords = ", ".join(kw.text for kg in art.findall(".//kwd-group")
                                 if "kwd-group-type" not in kg.attrib
                                 for kw in kg.findall(".//kwd")
                                 if kw.text) or "N/A"

            records.append({
                "pmcid": pmcid,
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "journal": journal,
                "publicationDate": publication_date,
                "doi": doi,
                "firstAuthor": first_author,
                "lastAuthor": last_author,
                "authorAffiliations": author_affiliations,
                "meshTags": mesh_tags,
                "keywords": keywords,
            })

        time.sleep(delay)

    return (pd.DataFrame(records).astype("string").sort_values(
        "pmcid", ignore_index=True))


def _strip_default_ns(xml_bytes: bytes) -> bytes:
    """
    Remove the *first* default namespace declaration (xmlns="…") so that the
    returned XML is easy to address with bare tag names.
    """
    return re.sub(rb'\sxmlns="[^"]+"', b"", xml_bytes, count=1)
    
    
def _classify_pubmed_xml(xml_str: str, *, probe: int = 4096) -> str:
    """
    Classify an XML payload as
      'pmc'      – JATS full-text (root <article>)
      'medline'  – PubMed/MEDLINE citation (<PubmedArticle> or <MedlineCitation>)
      'unknown'  – anything else / malformed
    The first `probe` bytes are inspected case-insensitively.
    """
    if not xml_str or xml_str == "N/A":
        return "unknown"

    head = xml_str.lstrip()[:probe].lower()       # still O(1) w.r.t. file size
    if re.search(r"<article\b", head):
        return "pmc"
    if re.search(r"<pubmedarticle\b", head) or re.search(r"<medlinecitation\b", head):
        return "medline"
    return "unknown"


def get_pmc_full_xml(
    pmcids: List[str],
    *,
    api_key: str | None = None,
    batch_size: int = 200,
    timeout: int = 20,
    max_retries: int = 3,
    delay: float = 0.34,
) -> pd.DataFrame:
    """
    ------------------------------------------------------------------------
    Retrieve the full-text **JATS XML** for one or many PubMed Central IDs.
    ------------------------------------------------------------------------

    Parameters
    ----------
    pmcids : list[str]
        PMC IDs *with or without* the “PMC” prefix (e.g. ["PMC123", "456"]).
    api_key : str | None, optional
        NCBI API key – lifts the personal rate-limit to ≈10 req s⁻¹.
    batch_size : int, default 200
        IDs per EFetch request (PMC ceiling = 10 000).
    timeout : int, default 20 s
        Socket timeout for each HTTP request.
    max_retries : int, default 3
        Attempts per batch on HTTP-429 / 5xx before giving up.
    delay : float, default 0.34 s
        Base pause between retries (doubles each attempt).

    Returns
    -------
    pandas.DataFrame
        Columns
        -------
        pmcid       | string   (canonical “PMC…” identifier)
        fullXML     | string   (entire `<article>` subtree or "N/A")
        isFullText  | boolean  (True ⇢ a <body> element exists)
        hasSuppMat  | boolean  (True ⇢ supplementary material present)
        xmlKind     | string   ("pmc", "medline", or "unknown")

        Every PMC ID you supplied is represented exactly once—even if the
        record is missing, withdrawn, or the request fails.
    """
    # ── Guard clause ───────────────────────────────────────────
    if not pmcids:
        return (
            pd.DataFrame(
                columns=[
                    "pmcid",
                    "fullXML",
                    "isFullText",
                    "hasSuppMat",
                    "xmlKind",
                ]
            ).astype(
                {
                    "pmcid": "string",
                    "fullXML": "string",
                    "isFullText": "boolean",
                    "hasSuppMat": "boolean",
                    "xmlKind": "string",
                }
            )
        )

    # --- Prefix-safe normalisation ----------------------------
    norm_ids = [
        pid if str(pid).upper().startswith("PMC") else f"PMC{pid}"
        for pid in pmcids
    ]

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    session = requests.Session()
    records: list[dict] = []

    total_batches = ceil(len(norm_ids) / batch_size)

    # ── Main loop ─────────────────────────────────────────────
    for b_idx in range(total_batches):
        chunk = norm_ids[b_idx * batch_size : (b_idx + 1) * batch_size]
        params = {"db": "pmc", "retmode": "xml", "id": ",".join(chunk)}
        if api_key:
            params["api_key"] = api_key

        # ── Fetch with retries ────────────────────────────────
        response = None
        for attempt in range(1, max_retries + 1):
            try:
                response = session.get(base_url, params=params, timeout=timeout)
                response.raise_for_status()
                break
            except (HTTPError, RequestException) as exc:
                status = getattr(exc.response, "status_code", None)
                if (
                    status
                    and (status == 429 or 500 <= status < 600)
                    and attempt < max_retries
                ):
                    wait = delay * (2 ** (attempt - 1))
                    logger.warning(
                        f"Batch {b_idx+1}: HTTP {status}; retry "
                        f"{attempt}/{max_retries} in {wait:.1f}s"
                    )
                    time.sleep(wait)
                    continue
                logger.error(f"Batch {b_idx+1} failed: {exc}")
                break

        # ── On complete failure, emit placeholders ────────────
        if response is None or not response.ok:
            records.extend(
                {
                    "pmcid": cid,
                    "fullXML": "N/A",
                    "isFullText": False,
                    "hasSuppMat": False,
                    "xmlKind": "unknown",
                }
                for cid in chunk
            )
            continue

        # ── Parse / strip namespace ───────────────────────────
        try:
            root = ET.fromstring(_strip_default_ns(response.content))
        except ET.ParseError as e:
            logger.error(f"XML parse error in batch {b_idx+1}: {e}")
            records.extend(
                {
                    "pmcid": cid,
                    "fullXML": "N/A",
                    "isFullText": False,
                    "hasSuppMat": False,
                    "xmlKind": "unknown",
                }
                for cid in chunk
            )
            time.sleep(delay)
            continue

        # ── Extract <article> records ─────────────────────────
        seen: set[str] = set()
        for art in root.findall(".//article"):
            # Robust PMCID extraction & normalisation
            pmcid_text = next(
                (
                    art.findtext(f'.//article-id[@pub-id-type="{t}"]')
                    for t in ("pmcid", "pmc", "pmcid-ver", "pmcaid")
                    if art.find(f'.//article-id[@pub-id-type="{t}"]')
                    is not None
                ),
                "N/A",
            )
            if "." in pmcid_text:  # drop version suffix
                pmcid_text = pmcid_text.split(".", 1)[0]
            if not pmcid_text.upper().startswith("PMC"):
                pmcid_text = f"PMC{pmcid_text}"

            xml_str = ET.tostring(art, encoding="unicode")
            has_body = art.find(".//body") is not None
            has_supp = any(
                art.find(path) is not None
                for path in (
                    ".//supplementary-material",
                    ".//inline-supplementary-material",
                    ".//sub-article[@article-type='supplementary-material']",
                )
            )

            records.append(
                {
                    "pmcid": pmcid_text,
                    "fullXML": xml_str,
                    "isFullText": has_body,
                    "hasSuppMat": has_supp,
                    "xmlKind": _classify_pubmed_xml(xml_str),
                }
            )
            seen.add(pmcid_text)
                     

        # ── Placeholder rows for IDs not returned ─────────────
        for cid in chunk:
            if cid not in seen:
                records.append(
                    {
                        "pmcid": cid,
                        "fullXML": "N/A",
                        "isFullText": pd.NA,
                        "hasSuppMat": pd.NA,
                        "xmlKind": "unknown",
                    }
                )

        time.sleep(delay)
        
    # 1) build the DataFrame
    df = pd.DataFrame(records)

    # 2) add the extracted text column
    df['fullText'] = df['fullXML'].apply(extract_full_text_from_xml)

    # 3) enforce your nullable dtypes (including fullText) and return
    return df.astype(
        {
            "pmcid": "string",
            "fullXML": "string",
            "fullText": "string",
            "isFullText": "boolean",
            "hasSuppMat": "boolean",
            "xmlKind": "string",
        }
    )




def get_pmc_html_text(
    pmcids: List[str],
    *,
    timeout: int = 20,
    max_retries: int = 3,
    delay: float = 0.5,
) -> pd.DataFrame:
    """
    ------------------------------------------------------------------------
    Download the **flat-HTML** body of any number of PubMed Central articles.
    ------------------------------------------------------------------------

    Parameters
    ----------
    pmcids : list[str]
        PMC IDs *with or without* the ``"PMC"`` prefix.  Duplicates are
        tolerated; each ID is represented exactly once in the output.
    timeout : int, default 20 s
        Socket timeout for each HTTP request.
    max_retries : int, default 3
        Attempts per article on HTTP 429 / 5xx before giving up.
    delay : float, default 0.5 s
        Base pause between retries (multiplied by 2**attempt).

    Returns
    -------
    pandas.DataFrame
        Columns
        --------
        ``pmcid``      | string  
        ``htmlText``   | string   (raw, cleaned HTML **as text**; ``"N/A"`` on failure)
        ``scrapeMsg``  | string   (empty on success, diagnostic message on failure)

        The frame always contains one row per requested PMCID, in the order
        they were supplied.
    """
    # ── Guard clause ────────────────────────────────────────────
    if not pmcids:
        return pd.DataFrame(
            columns=["pmcid", "htmlText", "scrapeMsg"]).astype("string")

    # Preserve the IDs exactly as the caller gave them  ➜ `orig`
    # Canonicalise just for the network call            ➜ `canon`
    canon_ids: list[str] = []
    canon_to_orig: dict[str, str] = {}
    seen: set[str] = set()
    for orig in pmcids:
        canon = orig if str(orig).upper().startswith("PMC") else f"PMC{orig}"
        if canon not in seen:  # <── ensures we fetch each article once
            canon_ids.append(canon)
            seen.add(canon)
        canon_to_orig.setdefault(canon, orig)  # first occurrence wins
    records = []

    base_tpl = "https://pmc.ncbi.nlm.nih.gov/articles/{pid}/?format=flat"
    headers = {
        "User-Agent": ("Mozilla/5.0 (compatible; PubMedCrawler/1.0; "
                       "+https://github.com/you/yourrepo)")
    }

    # ── Main loop over individual IDs ───────────────────────────
    for pid in canon_ids:  # use canonical value for the URL
        url = base_tpl.format(pid=pid)
        html_text: str | None = None
        msg = ""

        for attempt in range(1, max_retries + 1):
            try:
                resp = requests.get(url, headers=headers, timeout=timeout)
                if resp.status_code in (403, 429) and attempt < max_retries:
                    wait = delay * (2**(attempt - 1))
                    logger.warning(
                        f"{pid}: HTTP {resp.status_code}; retry {attempt}/{max_retries} in {wait:.1f}s"
                    )
                    time.sleep(wait)
                    continue

                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")

                # Prefer the content under #maincontent; fall back to full doc
                main = soup.find(id="maincontent") or soup
                # Keep HTML (with basic cleanup), not plain text:
                #   – drop <script>, <style>, navigation junk
                for tag in main.find_all(
                    ["script", "style", "nav", "footer", "aside"]):
                    tag.decompose()

                html_text = str(main)  # raw HTML as str
                break  # success – leave retry loop

            except (HTTPError, RequestException) as exc:
                msg = f"{type(exc).__name__}: {exc}"
                if attempt < max_retries:
                    wait = delay * (2**(attempt - 1))
                    time.sleep(wait)
                    continue
                logger.error(
                    f"{pid}: giving up after {max_retries} attempts – {msg}")
                html_text = None
            except Exception as exc:  # BeautifulSoup / unexpected
                msg = f"{type(exc).__name__}: {exc}"
                logger.error(f"{pid}: parsing error – {msg}")
                html_text = None
            finally:
                # avoid flooding PMC with rapid requests
                time.sleep(0.1)

        # map back to the exact value supplied by the caller
        records.append({
            "pmcid": canon_to_orig.get(pid, pid),
            "htmlText": html_text or "N/A",
            "scrapeMsg": msg,
        })

    return pd.DataFrame(records).astype("string")


def get_pmc_full_text(pmcids: List[str] | str,
                      *,
                      xml_fallback_min_chars: int = 2_000,
                      timeout: int = 20) -> dict[str, str]:
    """
    Retrieve plain full-text for one or many PMCIDs:
      1) try the “flat” HTML view,
      2) fall back to the JATS <body> from EFetch.

    Parameters
    ----------
    pmcids : list[str] | str
        A single PMCID or an iterable of them (with or without "PMC" prefix).
    xml_fallback_min_chars : int, default 2_000
        If the flat view yields fewer chars, we attempt XML and keep the longer.
    timeout : int, default 20
        Socket timeout for each HTTP request.

    Returns
    -------
    dict[str, str]
        Mapping pmcid → plain text (or "N/A" on failure).
    """
    # normalize to list
    if isinstance(pmcids, str):
        pmcids = [pmcids]

    flat_tpl = "https://pmc.ncbi.nlm.nih.gov/articles/{pid}/?format=flat"
    headers = {
        "User-Agent": ("Mozilla/5.0 (compatible; PubMedCrawler/1.1; "
                       "+https://github.com/OHDSI/searchpubmed)")
    }

    out: dict[str, str] = {}

    for raw_id in pmcids:
        pid = raw_id if str(raw_id).upper().startswith(
            "PMC") else f"PMC{raw_id}"
        text = ""
        success = False

        # ── step 1: flat HTML ──────────────────────────────────
        try:
            url = flat_tpl.format(pid=pid)
            r = requests.get(url, headers=headers, timeout=timeout)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            main = soup.find(id="maincontent") or soup
            flat_text = " ".join(
                p.get_text(" ", strip=True) for p in main.find_all("p"))
            text = flat_text.strip()
            success = len(text) >= xml_fallback_min_chars
            if success:
                logger.info(f"{pid}: used flat HTML ({len(text):,} chars)")
        except Exception as exc:
            logger.warning(f"{pid}: flat view failed – {exc}")

        # ── step 2: XML fallback if needed ─────────────────────
        if not success:
            try:
                # build a single URL so we don’t pass a params= kwarg
                xml_url = (
                    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
                    f"?db=pmc&id={pid}&retmode=xml")
                r = requests.get(xml_url, headers=headers, timeout=timeout)
                r.raise_for_status()

                # strip default namespace and parse
                xml_content = _strip_default_ns(r.content)
                root = ET.fromstring(xml_content)
                body = root.find(".//body")
                xml_text = (ET.tostring(
                    body, encoding="unicode", method="text").strip()
                            if body is not None else "")

                # keep whichever text is longer
                if len(xml_text) > len(text):
                    text = xml_text
                logger.info(f"{pid}: XML fallback used ({len(text):,} chars)")
            except Exception as exc:
                logger.error(f"{pid}: XML fallback failed – {exc}")

        out[pid] = text or "N/A"
        time.sleep(0.1)  # courtesy delay

    return out


def _scrape_pmc_standard_html(pmcid: str, *, timeout: int = 20) -> str:
    """
    Fetch the *regular* PMC HTML (not the `?format=flat` view) and return
    plain text.  Used only when both XML and flat-HTML versions are tiny.
    """
    url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/"
    headers = {"User-Agent": "Mozilla/5.0 (PubMedCrawler/2.0)"}
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # drop nav / scripts
        for tag in soup.find_all(["script", "style", "nav", "footer",
                                  "aside"]):
            tag.decompose()
        return soup.get_text(" ", strip=True)
    except Exception as exc:
        logger.warning(f"{pmcid}: standard HTML scrape failed – {exc}")
        return "N/A"


def get_pmc_licenses(pmcids: Iterable[str],
                     chunk_size: int = 200,
                     timeout: int = 30) -> Dict[str, Optional[str]]:
    """
    Query the PMC OA Web-service and return the licence string
    (e.g. 'CC BY', 'CC BY-NC', 'NO-CC CODE', …) for every PMCID.

    Parameters
    ----------
    pmcids      : an iterable of PMCIDs (with or without the 'PMC' prefix)
    chunk_size  : how many IDs to send in one HTTP request
                  (the service accepts up to ≈300; 200 is a safe default)
    timeout     : per-request timeout in seconds

    Returns
    -------
    dict mapping *pmcid* ➜ *license*  (None if the ID is unknown)

    Notes
    -----
    • The call is read-only and doesn’t require an API key.  
    • When a record is missing the <record … license="…"> attribute
      you’ll get None, which usually means the article is not in
      the OA subset or has “other”/unknown rights.
    """

    def _normalize(pid: str) -> str:
        """Upper-case & ensure the PMC prefix."""
        pid = pid.upper()
        return pid if pid.startswith("PMC") else f"PMC{pid}"

    # normalise, dedupe, & preserve original order
    unique_ids: List[str] = []
    seen = set()
    for pid in map(_normalize, pmcids):
        if pid not in seen:
            seen.add(pid)
            unique_ids.append(pid)

    out: Dict[str, Optional[str]] = {pid: None for pid in unique_ids}

    # hit the OA endpoint in chunks
    base = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi"
    for i in range(0, len(unique_ids), chunk_size):
        chunk = unique_ids[i:i + chunk_size]
        try:
            r = requests.get(
                base,
                params={"id": ",".join(chunk)},
                timeout=timeout,
                headers={"User-Agent": "pmc-licence-check/0.1"},
            )
            r.raise_for_status()
        except requests.RequestException as exc:
            # if the call fails, leave those IDs as None and continue
            print(f"[WARN] OA service call failed: {exc}")
            continue

        root = ET.fromstring(r.text)
        for rec in root.findall(".//record"):
            pid = _normalize(rec.attrib.get("pmcid", ""))
            lic = rec.attrib.get("license")
            if pid:
                out[pid] = lic

    return out





def extract_full_text_from_xml(xml_string: str) -> str:
    """
    Parse an NCBI efetch XML string and return the entire article text
    (all <abstract> blocks + every <sec> under <body>), in reading order,
    with double-newlines separating logical blocks.
    """
    # parse (will raise if truly malformed)
    root = ET.fromstring(xml_string)

    def local_name(elem):
        # strip namespace, if present
        return elem.tag.split('}', 1)[-1]

    blocks = []

    # 1) Abstracts (there may be multiple)
    for abstr in root.iter():
        if local_name(abstr) == "abstract":
            # optional title
            for child in list(abstr):
                if local_name(child) == "title" and child.text and child.text.strip():
                    blocks.append(child.text.strip())
            # all paragraphs under this abstract
            for p in abstr.iter():
                if local_name(p) == "p":
                    text = "".join(p.itertext()).strip()
                    if text:
                        blocks.append(text)

    # 2) Body sections
    for body in root.iter():
        if local_name(body) == "body":
            for sec in body.iter():
                if local_name(sec) == "sec":
                    # section heading
                    for child in list(sec):
                        if local_name(child) == "title" and child.text and child.text.strip():
                            blocks.append(child.text.strip())
                    # paragraphs in this section
                    for p in sec.iter():
                        if local_name(p) == "p":
                            text = "".join(p.itertext()).strip()
                            if text:
                                blocks.append(text)

    return "\n\n".join(blocks)



# ---------------------------------------------------------------------------

import re
import xml.etree.ElementTree as ET
from typing import List, Tuple, Dict, Pattern, Union

def get_jats_text_chunks(
    xml_string: str,
    *,
    min_len: int = 40,
    keywords: Union[None, str, Pattern, List[Union[str, Pattern]]] = None,
    include_table_cells: bool = False,
    include_tables: bool = False,
    text_only: bool = False,
) -> Union[List[str], List[Tuple[str, Dict[str, Union[str, bool]]]]]:
    """
    Extract meaningful text chunks from a JATS article *and* return
    lightweight metadata for every chunk.

    New metadata keys
    -----------------
    • section        – visible heading text at the current level
    • parent_sec     – visible heading one level up
    • section_type   – the <sec> element’s “sec-type” (methods, results…)
                       or "abstract" while inside <abstract>
    • in_abstract    – bool flag: True only for text coming from <abstract>

    Other behaviour is unchanged: short chunks are merged, optional keyword
    filtering, optional table flattening, etc.
    """

    # ------------------------------------------------------------------ #
    # 0.  Basic validation                                               #
    # ------------------------------------------------------------------ #
    if _classify_pubmed_xml(xml_string) != "pmc":
        raise ValueError("XML does not look like JATS full text")

    # ------------------------------------------------------------------ #
    # 1.  Robust XML parse                                               #
    # ------------------------------------------------------------------ #
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError:
        fixed = re.sub(r"&(?!amp;|lt;|gt;|apos;|quot;)", "&amp;", xml_string)
        root = ET.fromstring(fixed)

    # ------------------------------------------------------------------ #
    # 2.  Compile keyword regexes                                        #
    # ------------------------------------------------------------------ #
    if keywords is None:
        kw_res: List[Pattern] = []
    else:
        if not isinstance(keywords, list):
            keywords = [keywords]
        kw_res = [re.compile(p, re.I) if isinstance(p, str) else p for p in keywords]

    # ------------------------------------------------------------------ #
    # 3.  Helper to flatten full tables                                  #
    # ------------------------------------------------------------------ #
    def _table_to_text(tbl_el: ET.Element) -> str:
        caption_el = tbl_el.find(".//caption")
        caption = "".join(caption_el.itertext()).strip() if caption_el is not None else ""
        rows = []
        for tr in tbl_el.findall(".//tr"):
            cells = [" ".join(c.itertext()).strip() for c in tr]
            if cells:
                rows.append("\t".join(cells))
        return (caption + "\n" if caption else "") + "\n".join(rows)

    # ------------------------------------------------------------------ #
    # 4.  DFS traversal collecting chunks                                #
    # ------------------------------------------------------------------ #
    table_tags = {"table-wrap", "table"}
    candidates: List[Tuple[str, Dict[str, Union[str, bool]]]] = []
    captured_title = False

    sec_stack: List[str] = []
    sec_type_stack: List[str] = []
    in_abstract = False  # Set while walking inside <abstract>

    def recurse(el: ET.Element) -> None:
        nonlocal captured_title, in_abstract

        tag = el.tag

        # ---- entering structural nodes --------------------------------
        if tag == "abstract":
            in_abstract = True
            sec_stack.append("Abstract")
            sec_type_stack.append("abstract")

        elif tag == "sec":
            title_el = el.find("title")
            sec_title = "".join(title_el.itertext()).strip() if title_el is not None else ""
            sec_type = el.get("sec-type", "")
            # If no visible title, fall back to sec-type
            sec_stack.append(sec_title or sec_type)
            sec_type_stack.append(sec_type)

        # ---- decide if this element yields a text chunk ---------------
        collect = (
            tag in {"p", "li", "caption"}
            or (tag in {"title", "article-title"} and not sec_stack and not captured_title)
            or (tag == "td" and include_table_cells)
            or (tag in table_tags and include_tables)
        )
        if tag in {"title", "article-title"} and collect:
            captured_title = True

        if collect:
            txt = _table_to_text(el) if tag in table_tags else "".join(el.itertext()).strip()
            ctx = {
                "tag": tag,
                "section": sec_stack[-1] if sec_stack else "",
                "parent_sec": sec_stack[-2] if len(sec_stack) > 1 else "",
                "section_type": sec_type_stack[-1] if sec_type_stack else "",
                "in_abstract": in_abstract,
            }
            if not kw_res or any(r.search(txt) for r in kw_res):
                candidates.append((txt, ctx))
            # If we grabbed the whole table, skip its internals
            if tag in table_tags:
                return

        # ---- descend ---------------------------------------------------
        for child in el:
            recurse(child)

        # ---- leaving structural nodes ---------------------------------
        if tag == "abstract":
            in_abstract = False
            sec_stack.pop()
            sec_type_stack.pop()
        elif tag == "sec":
            sec_stack.pop()
            sec_type_stack.pop()

    recurse(root)

    # ------------------------------------------------------------------ #
    # 5.  Merge short chunks into neighbours                             #
    # ------------------------------------------------------------------ #
    merged: List[Tuple[str, Dict[str, Union[str, bool]]]] = []
    i = 0
    while i < len(candidates):
        txt, ctx = candidates[i]
        if len(txt) >= min_len:
            merged.append((txt, ctx))
            i += 1
            continue

        # txt is SHORT – decide whom to merge with
        if i + 1 < len(candidates):                     #  → merge into next
            nxt_txt, nxt_ctx = candidates[i + 1]
            candidates[i + 1] = (txt + " " + nxt_txt, nxt_ctx)
        elif merged:                                   #  → merge into previous
            prev_txt, prev_ctx = merged[-1]
            merged[-1] = (prev_txt + " " + txt, prev_ctx)
        else:                                          # only chunk; just keep it
            merged.append((txt, ctx))
        i += 1

    # optional second pass: remove trailing ultra-short chunk
    if merged and len(merged[-1][0]) < min_len and len(merged) > 1:
        prev_txt, prev_ctx = merged[-2]
        merged[-2] = (prev_txt + " " + merged[-1][0], prev_ctx)
        merged.pop()

    # ------------------------------------------------------------------ #
    # 6.  Return                                                         #
    # ------------------------------------------------------------------ #
    return [t for t, _ in merged] if text_only else merged
