# 🧭 Backlog Insights Copilot (Local & Private)

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B.svg)](https://streamlit.io/) [![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **PM-first** local app that turns your JIRA/Linear CSV export into:

- ✅ de-duplicated issues
- 🧩 topic clusters with human-readable labels
- 📊 RICE & WSJF scoring (editable assumptions)
- 🚀 a capacity-aware **release plan**
- 📥 exportable CSV & Markdown artifacts

Runs fully on **localhost**. No data leaves your machine. Perfect for interviews, portfolio demos, and day-to-day PM decisions.

---

## ✨ Demo (30 seconds)

1. `Upload` your `issues.csv`
2. See **clusters**, **duplicates**, **RICE/WSJF**
3. Click **Generate Release Plan** → export **CSV/Markdown**

> For a quick test, use the sample: `sample_data/issues_sample.csv`

---

## 🧰 Tech Stack

- **Frontend / App**: Streamlit
- **Data**: pandas, numpy
- **ML**: scikit-learn (MiniBatchKMeans), TF-IDF; optional Sentence Transformers
- **Stats/Utils**: SciPy
- **Storage**: in-memory + export to CSV/MD

---

## 🚀 Quickstart

```bash
# 1) Clone
git clone https://github.com/<YOUR_USERNAME>/backlog-insights-copilot.git
cd backlog-insights-copilot

# 2) Create & activate a venv (recommended)
python3 -m venv .venv
source .venv/bin/activate

# 3) Install deps
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4) Run
python -m streamlit run app.py
```

Open the local URL shown (e.g., http://localhost:8501).

---

## 📂 Data Schema

The app expects these columns (case-insensitive):

| Column | Type | Notes |
|--------|------|-------|
| `id` | str/int | Unique issue ID |
| `title` | str | Short title |
| `description` | str | Longer detail |
| `priority` | str | e.g., Critical/High/Medium/Low (mapped to Impact) |
| `status` | str | e.g., Open / In Progress / Done / Resolved |
| `story_points` | number | Non-zero preferred |
| `created_at` | date | ISO date string |

> See `sample_data/issues_sample.csv` for a working example.

---

## 🧪 Sample Dataset

A realistic backlog is provided at `sample_data/issues_sample.csv` with overlapping items (e.g., Search & CSV Export) so you can see clustering and duplicate detection in action.

---

## 🧠 How it works

- **Embedding**
  - Uses Sentence Transformers (`all-MiniLM-L6-v2`) if available; otherwise **TF-IDF** fallback (fast & local).
- **Clustering**
  - MiniBatchKMeans over embeddings → groups issues into N themes
  - Each cluster is **labeled** using top TF-IDF terms from its items.
- **Prioritization**
  - **RICE** = (Reach × Impact × Confidence) / Effort
  - **WSJF** = (BusinessValue + TimeCriticality + RiskReduction) / JobSize
  - Defaults are editable in the UI and row-by-row.
- **Release planning**
  - Greedy assignment by RICE to `R1 … Rn` subject to **capacity** (story points)
  - Unplaced items go to **Backlog**.
- **Duplicates**
  - Pairwise cosine similarity on embeddings; threshold adjustable in the UI.
  - For very large files, duplicate search samples to keep things snappy.

---

## 🏗️ Architecture

```mermaid
flowchart LR
  A[CSV Upload] --> B[Sanitize & Schema Check]
  B --> C[Text Join (title + description)]
  C --> D{Embeddings}
  D -->|SBERT available| E[Sentence Transformers]
  D -->|Fallback| F[TF-IDF Vectorizer]
  E --> G[MiniBatchKMeans]
  F --> G[MiniBatchKMeans]
  G --> H[Cluster Labels (Top TF-IDF terms)]
  G --> I[Theme Summary Table]
  B --> J[RICE/WSJF Defaults]
  J --> K[Editable Table]
  K --> L[Recompute Scores]
  L --> M[Capacity-based Planner]
  L --> N[Duplicate Finder (Cosine Sim)]
  M --> O[Export: Release Plan CSV/MD]
  N --> P[Export: Duplicates CSV]
```

---

## 📤 Exports

- `exports/release_plan.csv`
- `exports/release_plan.md`
- `exports/duplicates.csv`

Attach these artifacts to applications or bring them to interviews to show your decision logic.

---

## ⚙️ Configuration

- Tune the **priority→impact** mapping in `app.py` (`PRIORITY_TO_IMPACT`)
- Change default cluster count, capacity, releases, and duplicate threshold in the UI
- Switch to **SBERT** by installing `sentence-transformers`

---

## 🧯 Troubleshooting

- **`command not found: pip`**  
  Use `python -m pip install -r requirements.txt` inside an activated venv.
- **No Python interpreter in PyCharm**  
  Configure project interpreter → point to `.venv/bin/python`.
- **Large CSV slow on duplicates**  
  Increase threshold or accept sampling (auto-enabled > 2,500 rows).

---

## 🗺️ Roadmap

- PDF Release Brief (charts + risks)
- Multi-file project support (merge Jira + ticket data)
- Smarter capacity planning (skills/owner constraints)
- Inline dedupe (merge candidates with diff view)

---

## 🤝 Contributing

PRs welcome! Please:

1. Create a feature branch
2. Add tests (where practical)
3. Keep functions pure/testable where possible
4. Open a PR with a concise description, before/after screenshots

---

## 🪪 License

MIT — see [LICENSE](LICENSE).

---

## 🙌 Credits

Built for Product Managers who want **decision-quality analytics** and **privacy-safe** local demos.
