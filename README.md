# MetaXtractor - Extraction Pipeline

This directory contains the complete metadata extraction pipeline that combines multiple sources to generate comprehensive CodeMeta JSON output.

## Overview

The extraction pipeline integrates three main sources of metadata:

1. **GitHub API** - Repository information, README files, and basic metadata
2. **Structured Files** - Citation.cff, setup.py, pyproject.toml, package.json, etc.
3. **NER Model** - Metadata extraction from preprocessed README text using the trained model

## Pipeline Flow

```
GitHub Repository URL
         ↓
1. GitHub API Extraction
   - Repository metadata
   - README content
   - Structured files
         ↓
2. Structured Files Processing
   - Parse Citation.cff
   - Parse package.json
   - Parse pyproject.toml
   - Parse codemeta.json
         ↓
3. README Preprocessing & NER
   - Clean README text
   - Chunk for model input
   - Extract entities using NER model
         ↓
4. Priority-based Merging
   - GitHub metadata (highest priority)
   - Structured files metadata
   - Model-extracted metadata (lowest priority)
         ↓
5. CodeMeta JSON Output
```

## Usage

### Single Repository

1. Open `extraction_pipeline.ipynb`
2. Run all cells to set up the environment
3. Enter your GitHub token when prompted (optional but recommended)
4. Enter the GitHub repository URL
5. The pipeline will extract and merge metadata from all sources
6. Output will be saved as `{repo_name}_codemeta.json`

### Batch Processing

The notebook also includes batch processing functionality for multiple repositories:

```python
repo_urls = [
    "https://github.com/owner1/repo1",
    "https://github.com/owner2/repo2",
    # Add more URLs...
]
batch_process_repositories(repo_urls)
```

## Priority System

The pipeline uses a priority-based merging system:

1. **GitHub API** (Highest Priority)
   - Repository name, description, language
   - Creation/modification dates
   - Topics/keywords
   - License information
   - Author (repository owner)

2. **Structured Files** (Medium Priority)
   - Citation.cff: Authors, version, DOI
   - package.json: Dependencies, scripts
   - pyproject.toml: Python-specific metadata
   - codemeta.json: Existing CodeMeta data

3. **NER Model** (Lowest Priority)
   - Entities extracted from README text
   - Additional metadata not found in other sources

## Output Format

The final output is a CodeMeta 3.0 compliant JSON file containing:

- `@context`: CodeMeta 3.0 context
- `@type`: "SoftwareSourceCode"
- Standard CodeMeta fields (name, description, author, etc.)
- `_modelExtracted`: Additional entities found by the NER model
- `_sources`: Information about which sources were used

## Requirements

- Python 3.8+
- PyTorch
- Transformers
- Requests
- BeautifulSoup4
- pandas
- tqdm
- tomli (for TOML parsing)
- PyYAML (for YAML parsing)
- Trained NER model in `../model/` directory

## Model Directory

The pipeline expects the trained NER model to be located in `../model/` relative to the notebook. This should contain:

- `config.json`
- `model.safetensors` (or `pytorch_model.bin`)
- `tokenizer.json`
- `tokenizer_config.json`
- `vocab.json`
- Other tokenizer files

## GitHub Token

While optional, providing a GitHub token is recommended to avoid API rate limits:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `public_repo` scope
3. Enter the token when prompted by the notebook

Without a token, you're limited to 60 requests per hour per IP address.