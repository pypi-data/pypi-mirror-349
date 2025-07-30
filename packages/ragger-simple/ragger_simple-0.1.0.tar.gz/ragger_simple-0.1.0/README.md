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

### Initialize the vector database

```bash
vector-search init --collection my_documents
```

### Process documents

Create a JSON file (e.g., `documents.json`) with your articles:

```json
{
  "Article 1": "This is the full text of article 1...",
  "Article 2": "This is the full text of article 2..."
}
```

Then process them:

```bash
vector-search process --input documents.json --collection my_documents
```

### Search for relevant chunks

```bash
vector-search search --query "your search query here" --collection my_documents
```

## Python API

```python
from vector_search import VectorDB

# Initialize
db = VectorDB(collection_name="my_documents")

# Add documents
documents = {
    "Article 1": "This is the content of article 1...",
    "Article 2": "This is the content of article 2..."
}
db.add_documents(documents)

# Search
results = db.search("your query here", k=5)
print(results)
```

## License

MIT