# Data Lineage & Quality Checker (Streamlit)

Lightweight Streamlit app demonstrating data lineage analysis, data quality checks, and an optional local/remote LLM assistant.

## Repository layout

- `app.py` — Streamlit front-end. Presents three sections: Data Lineage, Data Quality, and AI Assistant.
- `utils/` — helper modules used by the app:
	- `data_lineage.py` — loads source CSV and optional `config.json` (mapping), dynamically imports `data/transform.py`, runs `transform(df_source)`, and builds a mapping tree of source → transformed → target columns.
	- `quality.py` — data-quality utilities and plotting helpers. Reads processed versions (expected under `data/processed_files_for_DQ/`).
	- `llama_helper.py` — small LLM wrapper using `litellm` (example uses `ollama/gpt-oss:20b`).
	- `__init__.py` — package initializer.

## How the linkage works (contract)

1. `app.py` imports functions from `utils` and calls them when the user triggers actions in the UI.
2. `analyze_lineage()` (from `utils.data_lineage`):
	 - Loads serializable inputs (e.g., `data/source.csv` and optional `data/config.json`) using a cached loader.
	 - Dynamically imports `data/transform.py` at runtime and calls `transform(df_source)` to get `df_transformed`.
	 - Inspects column names to infer which source columns contributed to which transformed columns.
	 - Uses `config.json` mapping (if present) to map transformed columns to final targets; marks unmapped columns as `(🟡 Unmapped column)`.
3. `run_data_quality()` (from `utils.quality`) reads `data/processed_files_for_DQ/processed_v2.csv` and `processed_v1.csv`, runs checks (completeness, uniqueness, duplicates), prepares figures, and returns results for rendering by Streamlit.
4. `ask_llama()` (from `utils.llama_helper`) wraps a call to `litellm.completion` and returns a plain text response or an error string.

## Expected data files

Place the following under a `data/` folder at the project root:

- `data/source.csv` — source dataset used by the lineage analyzer.
- `data/transform.py` — must define a function `transform(df: pandas.DataFrame) -> pandas.DataFrame`. This file is imported dynamically so you can update transforms without restarting the app.
- `data/config.json` (optional) — mapping of transformed column names to target names. Example:

```json
{
	"columns": {
		"trans_col_1": "target_table.target_col_1",
		"trans_col_2": "target_table.target_col_2"
	}
}
```

- `data/processed_files_for_DQ/processed_v2.csv` and `processed_v1.csv` — used by `utils.quality` for version comparisons.

If files are missing, the Streamlit UI will show errors or empty results; update file paths in the utilities if your layout differs.

## Install & run (Windows PowerShell)

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install required packages (example):

```powershell
pip install streamlit pandas matplotlib seaborn litellm
```

Note: `litellm` and the model are optional; skip them if you don't need the AI Assistant.

3. Run the app:

```powershell
streamlit run app.py
```

## Error modes and behavior

- `data_lineage` marks unmapped transformed columns as `(🟡 Unmapped column)` when `config.json` has no entry.
- `quality` returns empty DataFrames and shows `st.error` when expected files are missing.
- `llama_helper` catches exceptions and returns an error message string so the UI can display it.

## Next suggestions

- Add a `requirements.txt` or `pyproject.toml` for reproducible installs.
- Add a sample `data/transform.py` and a minimal `data/source.csv` so the app can run out-of-the-box.
- Add pytest unit tests for utilities in `utils/`.

---

If you want, I can also scaffold a small sample `data/transform.py` and a sample CSV so you can launch the app immediately. Tell me which sample data shape you'd like (columns and a few rows) and I'll add them.

