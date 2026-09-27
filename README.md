# 🔎 Peril-Lens

### Explainable Supervisory Analytics for SOC Assessment

> **Evidence → Signal → Priority → Human Review**

Peril-Lens is an **offline supervisory analytics platform** designed to help examiners analyse structured SOC alert and case-management data from **Critical Sector Entities (CSEs)**.

It identifies potential **execution gaps, negative-space conditions, operational anomalies, peer deviations, and supervisory attention signals**, then connects those signals back to supporting evidence so that human examiners can decide where deeper manual review is warranted.

---

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Analytics-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Offline](https://img.shields.io/badge/Deployment-Offline%20%2F%20Air--Gapped-2E7D32?style=for-the-badge)

</p>

<p align="center">

**SIH 2026 · SIH26157 · Supervisory Analytics Tool for SOC Assessment**

</p>

---

## 🎯 Problem Context

The **National Critical Information Infrastructure Protection Centre (NCIIPC)** assesses the cyber resilience of Critical Sector Entities.

During supervisory assessments, manual examination of SOC **security alerts and case-management records** can reveal operational weaknesses that may not be visible through conventional policies, audits, self-assessments, management reports, KPI dashboards, or compliance documentation.

However, manually reviewing increasing volumes of operational evidence across multiple entities is resource-intensive and difficult to scale.

The objective of SIH Problem Statement **SIH26157** is therefore to develop a deployable **Supervisory Analytics Tool for SOC Assessment (SAT-SA)** that assists human examiners in analysing this evidence at scale. :contentReference[oaicite:1]{index=1}

---

# 🧭 Our Approach

Peril-Lens treats SOC alert and case-management data as **operational evidence**.

Instead of attempting to replace a SOC or make an automated compliance decision, the platform analyses structured submissions to answer:

> **Where should a supervisor look more closely, and what evidence supports that attention?**

```text
      Structured CSE Submissions
                 │
                 ▼
       ┌───────────────────┐
       │ Data Validation   │
       │ & Feature         │
       │ Engineering       │
       └─────────┬─────────┘
                 │
                 ▼
      ┌─────────────────────────┐
      │ Supervisory Analytics   │
      │                         │
      │ • Execution Gaps       │
      │ • Negative Space       │
      │ • Operational Patterns │
      │ • Peer Benchmarking    │
      └────────────┬────────────┘
                   │
                   ▼
       ┌──────────────────────┐
       │ Evidence &           │
       │ Explainability       │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │ Supervisory          │
       │ Prioritization       │
       └──────────┬───────────┘
                  │
                  ▼
          👤 Human Examiner
