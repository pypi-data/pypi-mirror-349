"""
capella_pdf_qa_generator.py

AIDA Architecture Processing Pipeline.

This module provides an end-to-end pipeline to:

1. Build a directed graph of Capella model elements from an XML file.
2. Extract and resolve entities mentioned in user queries.
3. Retrieve and rank relevant XML snippets and PDF chunks.
4. Generate BEIR-style `corpus.jsonl` (PDF text chunks) and `queries.jsonl`
   (ten generated Q-A pairs per seed question) using LLMs.

Usage:
    from ragformance.data_generation.generators.capella_pdf_qa_generator import run

    run(
        seed_questions_path=Path("questions.json"),
        data_dir=Path("./pdfs"),
        output_dir=Path("results"),
        openrouter_key=os.getenv("OPENROUTER_API_KEY"),
        openrouter_base_url=os.getenv("OPENROUTER_BASE_URL"),
        hf_embed_model="ibm-granite/granite-embedding-30m-english",
        capella_path=Path("./model.capella"),
        entity_model_name="google/gemini-2.0-flash-001",
        qa_model_name="google/gemini-2.5-pro-preview",
    )


"""

import re
import uuid
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np
import networkx as nx
from lxml import etree
from rapidfuzz import process, fuzz
from pydantic import BaseModel, Field
import litellm
import instructor
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_community.document_loaders import PyPDFium2Loader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# Constants & Data Models

XMI_NS_URI = "http://www.omg.org/XMI"
ID_ATTRS   = [f"{{{XMI_NS_URI}}}id", "id"]
TAG_RE     = re.compile(r"\[S[a-f0-9]{6}\]", re.I)

class EntityList(BaseModel):
    """Schema for a list of extracted Capella entity names."""
    entities: List[str] = Field(..., description="exact names as they appear in Capella")

class QA(BaseModel):
    """Schema for a single Q-A pair."""
    question: str
    answer:   str
    sources:  List[str]

class QASet(BaseModel):
    """Schema for a full set of ten categorized Q-A pairs."""
    simple_fact:        QA
    simple_conditional: QA
    comparison:         QA
    interpretative:     QA
    multi_answer:       QA
    aggregation:        QA
    multi_hop:          QA
    heavy_post:         QA
    erroneous:          QA
    summary:            QA


# XML / Graph Utilities

def iter_capella_elements(xml_path: Path):
    print(f"[iter_capella_elements] Parsing XML file: {xml_path}")
    for _, elem in etree.iterparse(str(xml_path), events=("end",)):
        yield elem
        elem.clear()
        parent = elem.getparent()
        if parent is not None:
            while elem.getprevious() is not None:
                del parent[0]
    print(f"[iter_capella_elements] Completed parsing {xml_path}")

def get_node_id(elem: etree._Element) -> str:
    for attr in ID_ATTRS:
        nid = elem.get(attr)
        if nid:
            return nid
    return None

def build_network(xml_path: Path) -> nx.DiGraph:
    print(f"[build_network] Building Capella graph from {xml_path}")
    G = nx.DiGraph()
    for elem in iter_capella_elements(xml_path):
        nid = get_node_id(elem)
        if not nid:
            continue
        G.add_node(
            nid,
            tag         = etree.QName(elem.tag).localname,
            name        = elem.get("name", ""),
            file        = str(xml_path.resolve()),
            line        = elem.sourceline,
            description = elem.get("description", ""),
        )
        parent = elem.getparent()
        pid = get_node_id(parent) if parent is not None else None
        if pid:
            G.add_edge(pid, nid, type="contains")
    print(f"[build_network] Completed graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G


# Entity Extraction Setup

def setup_entity_extractor(
    model_name: str,
    api_key:    str,
    api_base:   str
) -> Tuple[ChatPromptTemplate, type[BaseModel], str, str, str]:
    # Patch litellm to use Pydantic models if not already patched
    if not hasattr(litellm, "_patched_with_instructor"):
        instructor.patch(litellm)
        litellm._patched_with_instructor = True

    inst = PydanticOutputParser(pydantic_object=EntityList).get_format_instructions()
    inst = inst.replace("{", "{{").replace("}", "}}") # Keep for prompt construction
    system = SystemMessagePromptTemplate.from_template(
        "You are an assistant that extracts Capella element names "
        "from user queries and returns them **only** as JSON matching this schema:\n\n"
        + inst
    )
    print(f"[setup_entity_extractor] Configuring extractor for LLM: {model_name}")
    user = HumanMessagePromptTemplate.from_template("{user_query}")
    prompt = ChatPromptTemplate.from_messages([system, user])
    print(f"[setup_entity_extractor] Extractor prompt and response model configured")
    return prompt, EntityList, model_name, api_key, api_base


# Name Index & Fuzzy Matching

def build_name_index(G: nx.DiGraph) -> Dict[str, List[str]]:
    print(f"[build_name_index] Building name index from graph nodes")
    idx: Dict[str, List[str]] = {}
    for nid, attrs in G.nodes(data=True):
        key = attrs["name"].lower()
        idx.setdefault(key, []).append(nid)
    print(f"[build_name_index] Name index size: {len(idx)}")
    return idx

def fuzzy_candidates(query: str, choices: Dict[str, str], top_k: int = 5, score_cutoff: int = 80):
    return (
        (nid, score)
        for nid, score, _ in process.extract(query, choices, scorer=fuzz.token_set_ratio, limit=top_k)
        if score >= score_cutoff
    )

def resolve_entity(
    entity: str,
    name_index: Dict[str, List[str]],
    choices:    Dict[str, str],
    *,
    fuzzy: bool = True
) -> List[str]:
    key = entity.lower()
    if key in name_index:
        print(f"[resolve_entity] Exact match for '{entity}': {name_index[key]}")
        return name_index[key]
    if fuzzy:
        cands = [nid for nid, _ in fuzzy_candidates(entity, choices)]
        print(f"[resolve_entity] Fuzzy candidates for '{entity}': {cands}")
        return cands
    print(f"[resolve_entity] No match for '{entity}'")
    return []


# XML Slicing & Tag Utilities

def slice_xml(node_attrs: dict, *, context_lines: int = 0) -> str:
    path = Path(node_attrs["file"])
    start = max(node_attrs["line"] - 1 - context_lines, 0)
    lines = path.read_text(encoding="utf-8").splitlines()
    open_t, close_t = f"<{node_attrs['tag']}", f"</{node_attrs['tag']}>"
    depth, end = 0, None
    for i, ln in enumerate(lines[node_attrs["line"]-1:], start=node_attrs["line"]):
        if open_t in ln:
            depth += ln.count(open_t)
        if close_t in ln:
            depth -= ln.count(close_t)
        if depth <= 0 and end is None:
            end = i
    end = end if end is not None else len(lines) - 1
    return "\n".join(lines[start:end+context_lines+1])

def extract_tags(text: str) -> List[str]:
    seen, out = set(), []
    for m in TAG_RE.findall(text):
        t = m.strip("[]")
        if t not in seen:
            out.append(t); seen.add(t)
    return out

def slice_relevant_xml(nid: str, G: nx.DiGraph) -> str:
    raw = slice_xml(G.nodes[nid])
    if any(x in raw for x in ("ownedDiagrams", "layoutData", "filters")):
        return ""
    clean = re.sub(r"\s+", " ", raw).strip()
    return clean[:600] + ("…" if len(clean) > 600 else "")

def resolve_tag(tag: str, src_map: dict, G: nx.DiGraph) -> dict:
    e = src_map.get(tag)
    if not e:
        print(f"[resolve_tag] Tag {tag} not found")
        return {"tag": tag, "error": "not_found"}
    if e["kind"] == "pdf":
        print(f"[resolve_tag] Resolved PDF tag {tag} → page {e['page']}")
        return {"tag": tag, "kind": "pdf", "page": e["page"], "snippet": e["snippet"]}
    attrs = G.nodes[e["id"]]
    snippet = slice_relevant_xml(e["id"], G)
    print(f"[resolve_tag] Resolved Capella tag {tag} → node {e['id']}")
    return {"tag": tag, "kind": "capella", **attrs, "snippet": snippet}


# QA Pipeline Setup

def setup_qa_llm(
    model_name: str,
    api_key:    str,
    api_base:   str
) -> Tuple[type[BaseModel], str, str, str]:
    # Patch litellm to use Pydantic models if not already patched
    if not hasattr(litellm, "_patched_with_instructor"):
        instructor.patch(litellm)
        litellm._patched_with_instructor = True

    print(f"[setup_qa_llm] Configuring QA for LLM: {model_name}")
    # Pydantic model QASet is the "parser" or response model
    print(f"[setup_qa_llm] QA response model configured")
    return QASet, model_name, api_key, api_base

def generate_qa_set(
    user_query:   str,
    G:            nx.DiGraph,
    vectordb:     Chroma,
    embed_model:  str,
    # Parameters from setup_entity_extractor
    extract_prompt_template: ChatPromptTemplate,
    extract_response_model: type[BaseModel],
    entity_model_name: str,
    entity_api_key: str,
    entity_api_base: str,
    # Parameters from setup_qa_llm
    qa_response_model: type[BaseModel],
    qa_model_name: str,
    qa_api_key: str,
    qa_api_base: str,
    name_index:   Dict[str, List[str]],
    choices:      Dict[str, str],
    k_pdf:        int = 5,
    k_capella:    int = 8,
) -> Tuple[dict, dict]:
    print(f"[generate_qa_set] Generating QA for query: '{user_query}'")

    # 1) Entity extraction
    prompt_messages_lc = extract_prompt_template.format_prompt(user_query=user_query).to_messages()
    messages = []
    for msg in prompt_messages_lc:
        role = msg.type
        if role == "human":
            role = "user"
        elif role == "ai":
            role = "assistant"
        messages.append({"role": role, "content": msg.content})
    
    print(f"[generate_qa_set] Calling litellm for entity extraction with model {entity_model_name}")
    extracted_data = litellm.completion(
        model=entity_model_name,
        messages=messages,
        api_key=entity_api_key,
        base_url=entity_api_base,
        response_model=extract_response_model
    )
    entities = extracted_data.entities if extracted_data else []
    print(f"[generate_qa_set] Extracted entities: {entities}")

    resolved = {e: resolve_entity(e, name_index, choices) for e in entities}
    print(f"[generate_qa_set] Resolved entities to IDs: {resolved}")

    raw_ids = [nid for ids in resolved.values() for nid in ids]
    missing = [nid for nid in raw_ids if nid not in G.nodes]
    if missing:
        print(f"[generate_qa_set] Warning: these IDs not in graph and will be skipped: {missing}")
    flat_ids = [nid for nid in raw_ids if nid in G.nodes]

    # 2) Capella snippet ranking (skip if none)
    capella_blocks, src_map = [], {}
    if flat_ids:
        print(f"[generate_qa_set] Embedding query and descriptions")
        rank_emb = HuggingFaceEmbeddings(model_name=embed_model)
        q_vec = rank_emb.embed_query(user_query)
        descs = [G.nodes[n].get("description") or G.nodes[n]["name"] for n in flat_ids]
        doc_vecs = rank_emb.embed_documents(descs)
        scores = np.dot(doc_vecs, q_vec)
        top_nids = [flat_ids[i] for i in np.argsort(scores)[-k_capella:][::-1]]
        print(f"[generate_qa_set] Top Capella node IDs: {top_nids}")
        for nid in top_nids:
            xml = slice_relevant_xml(nid, G)
            if not xml:
                continue
            sid = f"S{uuid.uuid4().hex[:6]}"
            node = G.nodes[nid]
            src_map[sid] = {
                "kind":"capella","id":nid,"tag":node["tag"],
                "name":node["name"],"snippet":xml
            }
            capella_blocks.append(f"[{sid}] ({node['tag']})\n```xml\n{xml}\n```")
        print(f"[generate_qa_set] Built {len(capella_blocks)} Capella snippet blocks")
    else:
        print("[generate_qa_set] No Capella IDs to rank; skipping.")

    # 3) PDF retrieval
    pdf_blocks = []
    for ch in vectordb.similarity_search(user_query, k=k_pdf):
        sid = f"S{uuid.uuid4().hex[:6]}"
        src_map[sid] = {"kind":"pdf","page":ch.metadata.get("page","?"),"snippet":ch.page_content}
        pdf_blocks.append(f"[{sid}] (page {src_map[sid]['page']})\n{ch.page_content}")
    print(f"[generate_qa_set] Retrieved {len(pdf_blocks)} PDF blocks")

    # 4) Assemble & invoke QA prompt
    cat_desc = """
    1. simple_fact          : a single factual answer.
    2. simple_conditional    : answer depends on an 'if' condition.
    3. comparison            : compare / evaluate two items.
    4. interpretative        : requires interpretation of intent / rationale.
    5. multi_answer          : expects a set/list of items.
    6. aggregation           : numeric or textual aggregation.
    7. multi_hop             : needs reasoning over ≥2 facts.
    8. heavy_post            : answer needs transformation (e.g., unit conversion).
    9. erroneous             : user premise wrong; correct it politely.
    10. summary              : produce a concise summary.
    """
    schema = qa_ps.get_format_instructions().replace("{","{{").replace("}", "}}")
    sys_msg = (
        "You are an aerospace-domain assistant. Prefer PDF snippets for facts; "
        "use Capella XML only as supplementary context and do NOT leak XML.\n\n"
        "Generate TEN Q-A pairs matching schema below, citing at least one [Sxxxxx] token per answer.\n\n"
        "Categories:\n" + cat_desc + "\n\nSchema:\n" + schema
    )
    # qa_ps (PydanticOutputParser for QASet) is replaced by qa_response_model (QASet itself)
    # The schema for the prompt is still obtained from PydanticOutputParser(pydantic_object=qa_response_model)
    temp_parser_for_schema = PydanticOutputParser(pydantic_object=qa_response_model)
    schema_instructions = temp_parser_for_schema.get_format_instructions().replace("{","{{").replace("}", "}}")
    
    sys_msg_for_prompt = (
        "You are an aerospace-domain assistant. Prefer PDF snippets for facts; "
        "use Capella XML only as supplementary context and do NOT leak XML.\n\n"
        "Generate TEN Q-A pairs matching schema below, citing at least one [Sxxxxx] token per answer.\n\n"
        "Categories:\n" + cat_desc + "\n\nSchema:\n" + schema_instructions
    )
    
    qa_prompt_template = ChatPromptTemplate.from_messages([
        ("system", sys_msg_for_prompt),
        ("human",
         "## Documents\n" + "\n\n".join(pdf_blocks) +
         "\n\n## Capella\n" + "\n\n".join(capella_blocks) +
         "\n\n## Question\n" + user_query)
    ])
    
    prompt_messages_lc_qa = qa_prompt_template.format_prompt().to_messages()
    messages_qa = []
    for msg in prompt_messages_lc_qa:
        role = msg.type
        if role == "human":
            role = "user"
        elif role == "ai":
            role = "assistant"
        messages_qa.append({"role": role, "content": msg.content})

    print(f"[generate_qa_set] Assembled QA prompt, calling litellm with model {qa_model_name}")
    qa_set_response = litellm.completion(
        model=qa_model_name,
        messages=messages_qa,
        api_key=qa_api_key,
        base_url=qa_api_base,
        response_model=qa_response_model
    )
    print(f"[generate_qa_set] QA set generation complete")

    return qa_set_response.dict() if qa_set_response else {}, src_map


# Run wrapper

def run(
    seed_questions_path: Path,
    data_dir:            Path,
    output_dir:          Path,
    openrouter_key:      str,
    openrouter_base_url: str,
    hf_embed_model:      str,
    capella_path:        Path,
    entity_model_name:   str = "google/gemini-2.0-flash-001",
    qa_model_name:       str = "google/gemini-2.5-pro-preview",
    chunk_size:          int = 750,
    chunk_overlap:       int = 100,
    persist_dir:         Path = Path("chroma_index"),
    k_pdf:               int = 5,
    k_capella:           int = 8,
) -> None:
    """
    Run the full AIDA QA generation pipeline.

    This function orchestrates the entire process of:
      1. Parsing a Capella XML to build a directed graph of model elements.
      2. Building a name index for entity resolution.
      3. Loading and chunking all PDFs in `data_dir`.
      4. Creating and persisting a Chroma vector store for text search.
      5. Initializing LLMs and parsers for entity extraction and QA generation.
      6. Writing out:
         - `corpus.jsonl`: BEIR-style text chunks from PDFs.
         - `queries.jsonl`: Generated Q-A pairs for each seed question.

    Args:
        seed_questions_path (Path): Path to a JSON file containing a list of
            seed questions (one string per entry).
        data_dir (Path): Directory containing PDF files to index.
        output_dir (Path): Directory where `corpus.jsonl` and `queries.jsonl`
            will be created. Will be created if it does not exist.
        openrouter_key (str): API key for the OpenRouter-compatible LLM service.
        openrouter_base_url (str): Base URL for the OpenRouter-compatible LLM service.
        hf_embed_model (str): HuggingFace embedding model identifier for vector search.
        capella_path (Path): Path to the Capella `.capella` XML file.
        entity_model_name (str, optional): LLM model for entity extraction.
            Defaults to "google/gemini-2.0-flash-001".
        qa_model_name (str, optional): LLM model for QA pair generation.
            Defaults to "google/gemini-2.5-pro-preview".
        chunk_size (int, optional): Maximum number of characters per text chunk.
            Defaults to 750.
        chunk_overlap (int, optional): Character overlap between consecutive chunks.
            Defaults to 100.
        persist_dir (Path, optional): Directory to persist the Chroma index.
            Defaults to Path("chroma_index").
        k_pdf (int, optional): Number of top PDF chunks to retrieve per query.
            Defaults to 5.
        k_capella (int, optional): Number of top Capella node snippets to retrieve
            per query. Defaults to 8.

    Raises:
        OSError: If reading from or writing to disk fails.
        ValueError: If any of the provided arguments are invalid.
    """
    
    print("[run] Starting BEIR-style pipeline run")

    # 1) Build Capella graph
    G = build_network(capella_path)

    # 2) Name index & choices
    name_index = build_name_index(G)
    choices = {nid: attrs["name"] for nid, attrs in G.nodes(data=True)}

    # 3) Load & chunk PDFs
    pages = []
    for pdf in sorted(data_dir.glob("*.pdf")):
        loaded = PyPDFium2Loader(str(pdf)).load()
        for p in loaded:
            p.metadata["source"] = Path(pdf).name
        pages.extend(loaded)
        print(f"[run]   Loaded {len(loaded)} pages from {pdf}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    raw_chunks = splitter.split_documents(pages)
    chunks = []
    for idx, chunk in enumerate(raw_chunks):
        meta = dict(chunk.metadata)
        meta["corpus_id"] = f"doc{idx}"
        meta["title"] = meta.get("source","")
        chunks.append(type(chunk)(page_content=chunk.page_content, metadata=meta))
    print(f"[run]   Split into {len(chunks)} chunks")

    # 4) Build & persist Chroma index
    emb_model = HuggingFaceEmbeddings(model_name=hf_embed_model)
    vectordb = Chroma.from_documents(chunks, embedding=emb_model, persist_directory=str(persist_dir))
    vectordb.persist()
    print(f"[run]   Chroma index persisted at {persist_dir}")

    # 5) Setup LLMs & parsers
    # Returns: prompt_template, response_model, model_name, api_key, api_base
    extract_prompt_template, extract_response_model, \
    entity_model_name_out, entity_api_key_out, entity_api_base_out = setup_entity_extractor(
        entity_model_name, openrouter_key, openrouter_base_url
    )
    # Returns: response_model, model_name, api_key, api_base
    qa_response_model_out, qa_model_name_out, \
    qa_api_key_out, qa_api_base_out = setup_qa_llm(
        qa_model_name, openrouter_key, openrouter_base_url
    )

    # 6) Prepare output
    output_dir.mkdir(parents=True, exist_ok=True)
    corpus_path  = output_dir / "corpus.jsonl"
    queries_path = output_dir / "queries.jsonl"

    # 7) Emit corpus
    with corpus_path.open("w", encoding="utf-8") as cf:
        for chunk in chunks:
            cf.write(json.dumps({
                "_id":   chunk.metadata["corpus_id"],
                "title": chunk.metadata["title"],
                "text":  chunk.page_content
            }, ensure_ascii=False) + "\n")
    print(f"[run] Wrote corpus to {corpus_path}")

    # 8) Load seeds & emit generated Q-A
    with seed_questions_path.open("r", encoding="utf-8") as f:
        seeds = json.load(f)

    with queries_path.open("w", encoding="utf-8") as qf:
        for qi, seed in enumerate(seeds):
            qa_set, src_map = generate_qa_set(
                user_query=seed, 
                G=G, 
                vectordb=vectordb, 
                embed_model=hf_embed_model,
                extract_prompt_template=extract_prompt_template, 
                extract_response_model=extract_response_model,
                entity_model_name=entity_model_name_out, # from setup
                entity_api_key=entity_api_key_out,     # from setup
                entity_api_base=entity_api_base_out,   # from setup
                qa_response_model=qa_response_model_out, # from setup
                qa_model_name=qa_model_name_out,       # from setup
                qa_api_key=qa_api_key_out,           # from setup
                qa_api_base=qa_api_base_out,         # from setup
                name_index=name_index, 
                choices=choices,
                k_pdf=k_pdf, 
                k_capella=k_capella
            )
            if qa_set: # Ensure qa_set is not None before iterating
                for category, qa in qa_set.items():
                entry = {
                    "_id":      f"q{qi}_{category}",
                    "question": qa["question"],
                    "answer":   qa["answer"],
                    "sources":  qa["sources"],
                    "metadata": {"seed_index": qi, "category": category}
                }
                qf.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print("[run] Generator pipeline complete.")
