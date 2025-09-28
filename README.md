# Mind Map AI Pipeline

A plain Python script that processes raw text into structured mind map JSON using Hugging Face APIs for AI processing and local Python for clustering.

## Features

- **Text Preprocessing**: Splits messy text into sentences and phrases
- **Embeddings**: Uses Hugging Face sentence-transformers API for semantic embeddings
- **Clustering**: Groups similar concepts using scikit-learn KMeans
- **Classification**: Labels clusters using Hugging Face zero-shot classification
- **Summarization**: Shortens long cluster labels using Hugging Face summarization
- **NER**: Extracts named entities using Hugging Face NER models
- **JSON Output**: Generates hierarchical mind map structure

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python mindmap_pipeline.py
```

This will use the default example text and generate `mindmap.json`.

### With Custom Text

```bash
python mindmap_pipeline.py --text "Your long text here..."
```

### With Input File

```bash
python mindmap_pipeline.py --file input.txt --output my_mindmap.json
```

### With Hugging Face Token (Optional)

```bash
python mindmap_pipeline.py --text "Your text" --token YOUR_HF_TOKEN
```

## API Requirements

The script uses Hugging Face Inference API endpoints:
- `sentence-transformers/all-MiniLM-L6-v2` for embeddings
- `facebook/bart-large-mnli` for zero-shot classification
- `facebook/bart-large-cnn` for summarization
- `dslim/bert-base-NER` for named entity recognition

These APIs are free to use but may have rate limits. A Hugging Face token is optional but recommended for higher rate limits.

## Output Format

The script generates a hierarchical JSON structure:

```json
{
  "root": "Mind Map",
  "children": [
    {
      "node": "Marketing",
      "children": ["TikTok Ads", "Campaign", "Social Media"]
    },
    {
      "node": "Finance", 
      "children": ["Budget", "Expenses", "ROI"]
    }
  ]
}
```

## Error Handling

The pipeline includes robust error handling:
- Fallback embeddings if API calls fail
- Graceful degradation for classification failures
- Text truncation for summarization errors
- Empty entity lists if NER fails

## Dependencies

- Python 3.7+
- requests
- scikit-learn
- numpy

No web frameworks required - pure Python with minimal dependencies.

