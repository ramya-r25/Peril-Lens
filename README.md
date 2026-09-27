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
![Offline](https://img.shields.io/badge/Deployment-Offline%20%2F%20Air--Gapped-2E7D32?style=for-the-badge)

</p>

<p align="center">

**SIH 2026 · SIH26157 · NTRO / NCIIPC · Blockchain & Cybersecurity**

</p>

---

## 🧭 Overview

**Peril-Lens** is an offline supervisory analytics prototype designed to help examiners analyse structured **SOC alert and case-management data** from multiple Critical Sector Entities (CSEs).

The platform treats operational SOC records as **evidence for supervisory assessment** rather than attempting to function as a SOC itself.

Peril-Lens helps identify:

- 🔎 Potential execution gaps
- 🌑 Potential negative-space conditions
- 📊 Operational anomalies and suspicious patterns
- 📈 Peer deviations and benchmarking signals
- 🚨 Entities requiring supervisory attention
- 🎯 Alert and case samples that may warrant deeper manual review
- 🔍 Evidence supporting each supervisory signal

The objective is simple:

> **Help supervisors determine where deeper examination may be warranted, why the area was flagged, and what evidence supports that attention.**

Peril-Lens is designed to **support human supervisory judgement — not replace it.**

---

## 🎯 Problem Context

The **National Critical Information Infrastructure Protection Centre (NCIIPC)** assesses the cyber resilience of Critical Sector Entities.

During these assessments, manual examination of samples of SOC security alerts and case-management records can reveal operational findings that may not be visible through policies, audits, self-assessments, management reports, KPI dashboards, or compliance documentation.

However, increasing data volumes and the need to assess multiple entities make manual review resource-intensive and difficult to scale.

SIH Problem Statement **SIH26157 — Supervisory Analytics Tool for SOC Assessment (SAT-SA)** therefore calls for a deployable supervisory analytics capability that can help:

1. Identify entities requiring supervisory attention.
2. Prioritise alert samples and investigations for manual review.
3. Detect operational weaknesses and cyber-resilience concerns.
4. Improve the efficiency, consistency, and scalability of supervisory assessments.

---

# 🧠 How Peril-Lens Works

Peril-Lens follows an evidence-driven supervisory workflow:

```text
┌──────────────────────────────┐
│  Structured CSE Submissions   │
│                              │
│  Alerts • Cases              │
│  Investigations • Escalations│
│  Dispositions • Assets       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Data Validation &        │
│     Feature Engineering      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│    Supervisory Analytics     │
│                              │
│  • Execution Gaps            │
│  • Negative Space            │
│  • Operational Patterns      │
│  • Peer Benchmarking         │
│  • Supervisory Indicators    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Evidence & Explainability  │
│                              │
│  Why was it flagged?         │
│  What evidence supports it?  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Review Prioritization   │
│                              │
│  Entities • Controls        │
│  Processes • Alert Samples  │
└──────────────┬───────────────┘
               │
               ▼
        👤 HUMAN EXAMINER
