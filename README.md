**MetaXtractor — Extract README & Structured Software Metadata**

MetaXtractor extracts software metadata (CodeMeta) from GitHub repositories by combining three sources:
- GitHub API metadata
- available structured files (e.g. `CITATION.cff`, `pyproject.toml`, `package.json`, `codemeta.json`)
- NER-based extraction from README text

The pipeline merges these sources with this priority: GitHub API → structured files → model extraction.

**Quick Summary**
- Purpose: generate per-repository CodeMeta JSONs for analysis and evaluation.
- Main outputs: per-repo `{repo_name}_codemeta.json`, aggregated CSVs, and evaluation plots in `data/analysis_results/`.

**Requirements**
- **Python 3.9 or 3.10** (recommended — some tools like SOMEF and other dependencies target these versions).
- Install Git LFS and fetch model files: run `git lfs install` and `git lfs pull` after cloning.
- GPU recommended for training/inference but not strictly required for small runs.

**Quick Start (zsh)**
```bash
# clone repo and fetch large files
git clone <https://github.com/SurMesure237/MetaXtractor>
cd MetaXtractor
git lfs install
git lfs pull

# optional: create virtual env and activate
python -m venv .venv
source .venv/bin/activate

# install common dependencies (adjust / pin versions as needed) or run the dependencies installation cell located in each notebook header
pip install -r requirements.txt
```

**Core paths**
- Dataset (Label Studio / merged): `data/dataset/dataset.json`
- Raw & analysis outputs: `data/analysis_results/`
- Label Studio exports: `data/label_studio_exports/`, `data/evaluation_ground_truth_exports/`
- Extraction outputs: `pipelines/extraction/output/` and `../evaluation/extrated_codemeta_files/`
- Models and checkpoints: `model/`
- Notebooks: `notebooks/` and `pipelines/`

**Notebooks (short)**
- `notebooks/1_repository_metadata_files_extraction.ipynb`: scrape repos and save raw metadata + readmes.
- `notebooks/2_readme_preprocessing.ipynb`: clean & chunk READMEs for model input.
- `notebooks/3_structured_metadata_files_preprocessing.ipynb`: convert/normalize structured files to CodeMeta format.
- `notebooks/4_label_studio_project_uploader.ipynb`: create Label Studio projects from snippets.
- `notebooks/5_label_studio_project_exporter.ipynb`: export annotated tasks for local use.
- `notebooks/6_ground_truth_formatter.ipynb`: convert Label Studio exports into CodeMeta ground-truth JSONs.

**Pipelines (short)**
- `pipelines/extraction/model_extraction_pipeline.ipynb`: batch extraction orchestration (cloning, README extraction, NER inference, merge → CodeMeta JSONs). Requires `model/` and external converters for some structured-file flows.
- `pipelines/extraction/somef_extraction_notebook.ipynb`: run SOMEF and filter README-sourced fields. Useful to compare structured-file output vs README-derived metadata.
- `pipelines/model_training/model_training.ipynb`: training/fine-tuning the NER model.
- `pipelines/evaluation/model_vs_somef_evaluation.ipynb`: compare model vs SOMEF vs ground truth and generate evaluation reports/plots.
