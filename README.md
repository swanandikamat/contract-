# ⚖️ Legal Predictor: AI-Powered Contract Risk Assessment & Triage System

An intelligent, explainable legal document analysis platform designed for internal contract review and risk triage. Built for the internal company hackathon.

---

## 📌 Executive Summary

Reviewing commercial contracts (MSAs, NDAs, Vendor Agreements, SOWs) is historically manual, slow, and expensive. Non-legal stakeholders—such as procurement managers, engineers, and project leads—frequently sign or negotiate agreements without realizing they contain high-risk terms such as uncapped liability, one-sided indemnification, or aggressive termination penalties.

**Legal Predictor** automates first-pass legal review:
1. Ingests raw contract documents (`PDF`, `DOCX`, `TXT`).
2. Extracts and segments standard legal clauses.
3. Audits clauses using a **hybrid intelligence approach**: deterministic legal heuristics combined with zero-shot LLM contextual reasoning.
4. Produces an overall contract risk score (0–100) and classification (`CLEAN / LOW RISK` vs `PROB / HIGH RISK`).
5. Highlights problematic language verbatim and provides plain-English explanations with negotiation recommendations.

---

## 🎯 Hackathon Scope & Dataset Context

### The Benchmark Dataset
The project is calibrated against a provided benchmark dataset consisting of:
* **20 Contract Documents**: 10 marked as `CLEAN` and 10 marked as `PROB` (Probable Issues).
* **Scoring / Evaluation Framework**: Defined legal criteria outlining contractual pitfalls.
* **Project Summary Document**: Contextual metadata and guidelines.

> **Important Data Science Note:**  
> The `CLEAN` vs `PROB` labels are a competition proxy for risk triage, not certified courtroom ground truth. Because $N = 20$ is too small for statistical deep learning without catastrophic overfitting, **Legal Predictor** does not rely on black-box model training on these 20 files. Instead, it utilizes **pre-trained LLMs + domain-guided rule engines**, using the 20 contracts strictly as a calibration and evaluation benchmark.

---

## 🏗️ High-Level System Architecture

```
                       ┌─────────────────────────┐
                       │  Uploaded Contract      │
                       │   (PDF / DOCX / TXT)    │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │   Document Processor    │
                       │ (pdfplumber, PyMuPDF,   │
                       │      python-docx)       │
                       └────────────┬────────────┘
                                    │ Clean Text Blocks
                                    ▼
                       ┌─────────────────────────┐
                       │  Clause Segmentation &  │
                       │   Metadata Extraction   │
                       └────────────┬────────────┘
                                    │
            ┌───────────────────────┴───────────────────────┐
            ▼                                               ▼
┌─────────────────────────┐                     ┌─────────────────────────┐
│ Deterministic Heuristic │                     │   LLM Deep Reasoner     │
│       Rule Engine       │                     │    (Gemini 1.5 Flash)   │
├─────────────────────────┤                     ├─────────────────────────┤
│ • Uncapped liability    │                     │ • Contextual ambiguity  │
│ • Missing safeguards    │                     │ • Asymmetric terms      │
│ • Unilateral rights     │                     │ • Plain-English summary │
│ • Harsh payment terms   │                     │ • Redline suggestion    │
└───────────┬─────────────┘                     └───────────┬─────────────┘
            │                                               │
            └───────────────────────┬───────────────────────┘
                                    ▼
                       ┌─────────────────────────┐
                       │   Composite Risk Score  │
                       │  (0 - 100 Risk Index)   │
                       │   CLEAN vs PROB Proxy   │
                       └────────────┬────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │   Interactive UI / API  │
                       │   (Dashboard & Diffs)   │
                       └─────────────────────────┘
```

---

## 🔍 Core Risk Taxonomy

The engine evaluates contracts across 5 major legal risk pillars:

| Risk Pillar | Critical Red Flags Detected | Impact on Score |
| :--- | :--- | :--- |
| **1. Liability & Indemnity** | Uncapped liability, broad third-party indemnity, exclusion of indirect damage caps | **Critical (Highest)** |
| **2. Termination & Default** | Immediate termination for convenience without cause, cure periods < 10 days, lock-in auto-renewals | **High** |
| **3. Financial & Payment** | Aggressive interest penalties (>1.5%/month), ambiguous invoicing terms, one-sided set-off rights | **Medium to High** |
| **4. Dispute & Governing Law** | Inconvenient foreign jurisdiction, mandatory one-sided arbitration, class-action/jury waivers | **Medium** |
| **5. Drafting & Omissions** | Total absence of Limitation of Liability, Force Majeure, or Confidentiality clauses; vague subjective terms | **High** |

---

## 💻 Technology Stack

* **Backend Framework:** Python 3.11, [FastAPI](https://fastapi.tiangolo.com/), Uvicorn
* **Data Validation & Schemas:** [Pydantic v2](https://docs.pydantic.dev/)
* **Document Parsing:** `pdfplumber`, `PyMuPDF` (`fitz`), `python-docx`
* **AI & NLP:** Google Gemini API (`gemini-1.5-flash`), Python Regex Rule Engine
* **Frontend:** Streamlit (or React / Tailwind CSS dashboard)
* **Configuration & Environment:** `python-dotenv`

---

## 📁 Repository Structure

```text
Legal Predictor/
├── README.md                   # Project overview and technical documentation
├── .gitignore                  # Prevents data, secrets, and caches from leaking
├── .env.example                # Template for required environment variables
├── requirements.txt            # Python dependencies
│
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI entry point
│   │   ├── api/v1/             # REST endpoints (/upload, /analyze, /results)
│   │   ├── core/               # Configuration, constants, and settings
│   │   ├── services/           # Parsing, clause segmenter, rule engine, LLM client
│   │   └── utils/              # Text normalization and helper utilities
│   └── tests/                  # Unit and integration tests
│
├── frontend/                   # Web user interface (Streamlit or React app)
│   ├── app.py                  # Main UI dashboard
│   └── components/             # Reusable UI widgets and risk cards
│
├── data/                       # Local data workspace (Git-ignored)
│   ├── raw/                    # The 20 benchmark contracts (10 CLEAN, 10 PROB)
│   ├── processed/              # Extracted and segmented text caches
│   └── reference/              # Scoring framework PDF and TXT summaries
│
└── docs/                       # Architecture diagrams and pitch notes
```

---

## 🚦 Project Development Roadmap

* **Phase 0:** Environment & Scaffolding (Virtualenv, Git, dependencies)
* **Phase 1:** Data Ingestion & Scoring Framework Mapping
* **Phase 2:** Document Parsing (PDF / DOCX / TXT text extraction)
* **Phase 3:** Clause Segmentation & Metadata Identification
* **Phase 4:** Deterministic Rule Engine (Pattern-based red flags)
* **Phase 5:** LLM Reasoning Layer (Nuance, explanations, redlining)
* **Phase 6:** Risk Scoring Aggregator & FastAPI REST Backend
* **Phase 7:** Interactive Frontend UI Dashboard
* **Phase 8:** Benchmark Calibration & Validation Testing
* **Phase 9:** Live Demo Polish & Pitch Packaging

---

## ⚠️ Legal Disclaimer
*Legal Predictor is an educational and workflow assistance prototype built for a hackathon. It does not provide legal advice and does not substitute for licensed legal counsel.*

# contract-
