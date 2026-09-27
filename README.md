# 🔎 Peril-Lens

### Explainable Supervisory Analytics for SOC Assessment

<p align="center">

**Evidence → Signal → Priority → Human Review**

</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Analytics-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Data%20Processing-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Offline](https://img.shields.io/badge/Runtime-Offline%20%2F%20Local-2E7D32?style=for-the-badge)

</p>

<p align="center">

**SIH 2026 · SIH26157 · NTRO / NCIIPC · Blockchain & Cybersecurity**

</p>

---

## 📌 Project Overview

**Peril-Lens** is a prototype for **SIH26157 — Supervisory Analytics Tool for SOC Assessment (SAT-SA)**.

It helps supervisory examiners analyse structured SOC alert and case-management evidence from Critical Sector Entities (CSEs), identify signals that may require supervisory attention, and prioritize records for deeper human review.

The prototype is intentionally **not a SOC, SIEM, real-time monitoring platform, or replacement for supervisory judgement**.

### What the prototype demonstrates

- 🔎 Potential execution gaps
- 🌑 Potential negative-space conditions
- 📊 Operational anomaly and pattern analysis
- 📈 Peer benchmarking and deviation analysis
- 🚨 Entity-level supervisory attention indicators
- 🎯 Review prioritization
- 🔍 Evidence-backed explainability
- 📄 Local report generation

> **Design principle:** Peril-Lens identifies evidence and signals for examination. Final supervisory conclusions remain with the human examiner.

---

## 🎯 SIH26157 Alignment

The official SIH26157 problem statement asks for a supervisory analytics capability that can help supervisors:

1. Identify entities requiring supervisory attention.
2. Prioritize alert samples and investigations for manual review.
3. Detect operational weaknesses and cyber-resilience concerns.
4. Improve the efficiency, consistency, and scalability of supervisory assessments.

The problem statement also requires fully offline/local operation without dependency on cloud services, SaaS platforms, externally hosted AI models, or external APIs.

**Official problem statement:** https://sih2026.vuce.in/ps/SIH26157

---

# 🚀 Setup Instructions

This is the primary evaluator quick-start section.

## 1. System Requirements

Recommended:

- Python 3.x
- Windows, Linux, or macOS
- 4 GB RAM minimum recommended
- 1 GB+ free storage
- Modern web browser

The prototype uses:

| Package | Version |
|---|---:|
| Streamlit | 1.63.0 |
| Pandas | 3.0.5 |
| NumPy | 2.5.2 |
| Plotly | 7.0.0 |
| ReportLab | 5.0.1 |
| cryptography | 50.0.1 |

---

## 2. Clone the Repository

Open a terminal:

    git clone https://github.com/ramya-r25/Peril-Lens.git
    cd Peril-Lens

---

## 3. Create a Virtual Environment

### Windows PowerShell

    python -m venv .venv
    .venv\Scripts\Activate.ps1

### Windows Command Prompt

    .venv\Scripts\activate.bat

### Linux / macOS

    python3 -m venv .venv
    source .venv/bin/activate

---

## 4. Install Dependencies

    python -m pip install -r requirements.txt

For a controlled offline deployment, the required Python packages/wheels should be provisioned locally before installation. The application does not require Internet access during runtime.

---

# ▶️ Running the Prototype

From the repository root:

    python -m streamlit run dashboard/app.py

Windows PowerShell:

    python -m streamlit run dashboard\app.py

Then open:

**http://localhost:8501**

---

# ⚡ Evaluator Quick Start

If you only have a few minutes to inspect the prototype:

### 1. Start Peril-Lens

    python -m streamlit run dashboard/app.py

### 2. Open the local dashboard

Open **http://localhost:8501**

### 3. Recommended exploration order

**Command Center**  
Understand entity-level supervisory attention and overall signals.

**Entity Intelligence**  
Inspect entity-level findings, indicators, and comparative signals.

**Evidence Analytics**  
Inspect execution-gap, negative-space, anomaly, and operational evidence.

**Review Queue**  
See records prioritized for deeper manual examination.

**Case Review**  
Drill down into representative cases and supporting evidence.

**Governance / Reporting**  
Inspect governance-oriented views and locally generated reporting.

### 4. Check explainability

For a flagged signal, inspect:

- Why it was flagged
- Supporting evidence
- Analytical category
- Contribution to supervisory attention
- Underlying records available for examiner review

---

# 📂 Prototype Data

The current prototype uses synthetic structured data stored locally:

    data/
    └── synthetic/
        ├── alerts.csv
        ├── cases.csv
        ├── escalations.csv
        ├── investigations.csv
        └── monitoring.csv

These datasets are for prototype demonstration and validation only.

They do not represent real CSE data, NCIIPC data, customer information, or operational SOC telemetry.

---

# 🧾 Data Flow

    Structured CSE Data
            ↓
    Data Validation
            ↓
    Feature Engineering
            ↓
    Supervisory Analytics
       ┌─────┼─────┬────────────┐
       ↓     ↓     ↓            ↓
    Execution Negative Operational Peer
      Gaps    Space  Patterns   Benchmarking
       └─────┴─────┴────────────┘
            ↓
    Supervisory Indicators
            ↓
    Explainability
            ↓
    Review Prioritization
            ↓
       Human Examiner

---

# 🧠 Analytics Modules

| Module | Purpose |
|---|---|
| execution_gap_engine.py | Potential execution-gap signals |
| negative_space_engine.py | Potential absence-of-evidence signals |
| operational_pattern_engine.py | Operational patterns and anomalies |
| peer_benchmarking.py | Entity comparison and deviation analysis |
| supervisory_indicators.py | Entity-level supervisory indicators |
| prioritization_engine.py | Manual-review prioritization |
| explainability_engine.py | Supporting rationale and evidence traceability |

---

# 🗂️ Repository Structure

    Peril-Lens/
    │
    ├── dashboard/
    │   ├── app.py
    │   ├── Peril_Lens_core.py
    │   ├── theme.py
    │   ├── components/
    │   └── pages/
    │       ├── command_center.py
    │       ├── entity_intelligence.py
    │       ├── evidence_analytics.py
    │       ├── review_queue.py
    │       ├── case_review.py
    │       ├── governance.py
    │       └── data_validation.py
    │
    ├── data/
    │   └── synthetic/
    │
    ├── src/
    │   ├── analytics/
    │   ├── anomaly_detection/
    │   ├── features/
    │   ├── reports/
    │   └── security/
    │
    ├── tests/
    │
    ├── requirements.txt
    ├── README.md
    └── .gitignore

---

# 🔐 Offline Deployment

Offline operation is a core SIH26157 requirement.

### Prototype runtime

- Local Streamlit application
- Local synthetic CSV data
- Local analytics execution
- Local report generation
- No cloud database dependency
- No SaaS dependency
- No external AI-model/API dependency
- No Internet requirement during application execution

### Controlled deployment

A production NCIIPC-controlled deployment would additionally require approved:

1. Python/runtime environment
2. Dependency package set
3. CSE data interfaces
4. Identity and access controls
5. Audit infrastructure
6. Analytics/model update procedures where applicable
7. Security validation and operational controls

The current repository is a prototype and is not presented as a production deployment package.

---

# 📊 Validation Approach

The SIH problem statement requires validation against findings derived from expert manual review.

The prototype uses controlled synthetic scenarios representing supervisory signals such as:

- Unusually rapid case closure
- Missing or insufficient escalation evidence
- Repeated activity around the same asset
- Potentially repetitive investigation behaviour
- Low or missing monitoring evidence
- Deviations between entities
- Operational workloads inconsistent with expected activity

Validation assets and dataset checks are located under:

    tests/

A production validation program should compare Peril-Lens outputs with findings independently derived by expert examiners and assess:

- Signal identification effectiveness
- False-positive / false-negative behaviour
- Prioritization usefulness
- Explainability and traceability
- Consistency across entities
- Performance at larger data volumes

---

# 🧑‍💻 Human-in-the-Loop Design

Peril-Lens assists supervisory examination; it does not automate final supervisory judgement.

    Analytics identifies a signal
                ↓
    Evidence explains the signal
                ↓
    Priority determines review attention
                ↓
    Human examiner reviews records
                ↓
    Examiner makes the supervisory determination

---

# 🔎 Current Prototype Scope

### Demonstrated

- Local Streamlit dashboard
- Synthetic structured SOC datasets
- Data validation views
- Execution-gap analytics
- Negative-space analytics
- Operational pattern/anomaly analysis
- Peer benchmarking
- Supervisory indicators
- Review prioritization
- Explainability and evidence traceability
- Case-level review workflow
- Local report generation

### Production extensions

The current repository demonstrates the concept using synthetic CSV data.

A production SAT-SA deployment may additionally require:

- Organization-specific schemas
- JSON/database/API ingestion
- Larger-scale data processing
- Enterprise identity and access controls
- Production audit infrastructure
- Controlled analytics/model update procedures
- Formal validation against expert supervisory findings
- NCIIPC-approved operational and security controls

These are intentionally documented as extensions rather than claimed as already implemented.

---

# 🛠️ Troubleshooting

## Streamlit command not found

Use:

    python -m streamlit run dashboard/app.py

## Dependency installation fails

Activate the virtual environment and retry:

    python -m pip install -r requirements.txt

For restricted offline environments, verify that required package wheels are available locally.

## Port 8501 is already in use

    python -m streamlit run dashboard/app.py --server.port 8502

Then open:

**http://localhost:8502**

## Expected data is not visible

Confirm that these files exist:

    data/synthetic/alerts.csv
    data/synthetic/cases.csv
    data/synthetic/investigations.csv
    data/synthetic/escalations.csv
    data/synthetic/monitoring.csv

---

# 📋 Evaluator Checklist

- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install requirements
- [ ] Start Streamlit
- [ ] Open local dashboard
- [ ] Inspect Command Center
- [ ] Inspect entity intelligence
- [ ] Review execution-gap / negative-space evidence
- [ ] Inspect operational patterns and peer deviations
- [ ] Open prioritized review records
- [ ] Trace findings to supporting evidence
- [ ] Inspect case-level review
- [ ] Generate/view local reporting
- [ ] Review prototype data and validation assets

---

# 📦 SIH Evaluation Deliverables

This repository provides the **source-code component** and the **README with setup instructions** required for SIH26157 evaluation.

The wider submission package includes:

- Solution architecture
- Functional design
- Analytics methodology
- Data requirements
- Infrastructure requirements
- Validation methodology
- Deployment and operational requirements
- Demo video
- Technical presentation

---

# ⚠️ Prototype Disclaimer

Peril-Lens is an academic/prototype implementation developed for **SIH 2026 Problem Statement SIH26157**.

It uses synthetic data for demonstration.

The tool surfaces evidence, analytical signals, and areas that may warrant human supervisory review. It does not make final supervisory, compliance, or risk determinations and is not intended to replace a SOC, SIEM, real-time monitoring system, or expert examiner.

---

## 👥 Project

**Peril-Lens**  
**SIH 2026 — SIH26157**  
**Supervisory Analytics Tool for SOC Assessment (SAT-SA)**  
**NTRO / NCIIPC**

**Repository:** https://github.com/ramya-r25/Peril-Lens

---

> **Evidence → Signal → Priority → Human Review**
