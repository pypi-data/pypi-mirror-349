# Vector Search

A simple Python package for vector database operations using Qdrant.

## Features

- Initialize connection with Qdrant vector database
- Parse, chunk, and process text into vector embeddings
- Search for relevant text chunks based on semantic similarity

## Installation

```bash
pip install vector-search
```

## Usage

### CLI Commands

You can use the `vector-search` console script with three commands: `init`, `process`, and `search`.

#### init

Initialize the vector database:

```bash
vector-search init \
  --collection COLLECTION_NAME \
  [--model MODEL_NAME] \
  [--qdrant-url QDRANT_URL] \
  [--qdrant-key QDRANT_API_KEY] \
  [--qdrant-path QDRANT_PATH]
```

Options:

- `--collection` (str, default: `"documents"`)  
- `--model` (str, default: `"all-MiniLM-L6-v2"`)  
- `--qdrant-url` (str) — Qdrant Cloud URL  
- `--qdrant-key` (str) — Qdrant API key  
- `--qdrant-path` (str) — Path for local Qdrant

#### process

Process a JSON file of documents and add to the database:

```bash
vector-search process \
  --input INPUT_FILE.json \
  [--collection COLLECTION_NAME] \
  [--chunk-size CHUNK_SIZE] \
  [--overlap OVERLAP] \
  [--qdrant-url QDRANT_URL] \
  [--qdrant-key QDRANT_API_KEY] \
  [--qdrant-path QDRANT_PATH]
```

Options:

- `--input` (str, required) — Path to JSON `{ name: text }`  
- `--collection` (str, default: `"documents"`)  
- `--chunk-size` (int, default: `200`) — words per chunk  
- `--overlap` (int, default: `50`) — overlapping words  
- `--qdrant-url`, `--qdrant-key`, `--qdrant-path` — same as `init`

#### search

Search for relevant chunks:

```bash
vector-search search \
  --query QUERY_TEXT \
  [--collection COLLECTION_NAME] \
  [--k K] \
  [--output OUTPUT_FILE.json] \
  [--qdrant-url QDRANT_URL] \
  [--qdrant-key QDRANT_API_KEY] \
  [--qdrant-path QDRANT_PATH]
```

Options:

- `--query` (str, required) — query text  
- `--collection` (str, default: `"documents"`)  
- `--k` (int, default: `5`) — number of results  
- `--output` (str) — path to write JSON output (defaults to stdout)  
- `--qdrant-url`, `--qdrant-key`, `--qdrant-path` — same as `init`

## Python API

Import and initialize [`VectorDB`](ragger_simple/db.py):

```python
from ragger_simple.db import VectorDB

db = VectorDB(
    collection_name="my_documents",
    model_name="all-MiniLM-L6-v2",
    qdrant_url=None,
    qdrant_api_key=None,
    qdrant_path=None,
    qdrant_timeout=500.0,
)
```

Constructor parameters:

- `collection_name` (str) — Qdrant collection name  
- `model_name` (str) — sentence-transformers model  
- `qdrant_url` (str, optional) — cloud URL  
- `qdrant_api_key` (str, optional) — cloud API key  
- `qdrant_path` (str, optional) — local path  
- `qdrant_timeout` (float, default: `500`) — request timeout

Methods:

```python
db.add_documents(
    documents: Dict[str, str],
    chunk_size: int = 200,
    overlap: int = 50,
)
```

- `documents` — dict mapping doc names to text  
- `chunk_size` — words per chunk  
- `overlap` — overlapping words

```python
results = db.search(
    query: str,
    k: int = 5,
) -> List[Dict]
```

- `query` — query text  
- `k` — number of results

Example:

```python
documents = {
    "Article 1": "This is the content of article 1...",
    "Article 2": "This is the content of article 2..."
}
db.add_documents(documents, chunk_size=200, overlap=50)
results = db.search("your query here", k=5)
print(results)
```

## License

MIT