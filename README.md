<div align="center">

# 🔎 Peril-Lens

### Explainable Supervisory Analytics for SOC Assessment

**Evidence-driven analytics for identifying potential operational weaknesses, detecting supervisory signals, and prioritizing manual review across Critical Sector Entities.**

<br>

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Analytics-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Offline](https://img.shields.io/badge/Deployment-Offline%20%2F%20Air--Gapped-1F2937?style=for-the-badge)](#-offline-by-design)
[![SIH 2026](https://img.shields.io/badge/SIH%202026-SIH26157-6D28D9?style=for-the-badge)](#-problem-context)

<br>

**Problem Statement:** SIH26157 — Supervisory Analytics Tool for SOC Assessment (SAT-SA)

</div>

---

## 🧭 Overview

**Peril-Lens** is an offline supervisory analytics prototype designed to support the assessment of Security Operations Centre (SOC) effectiveness across **Critical Sector Entities (CSEs)**.

Traditional supervisory assessment can involve manually reviewing samples of SOC alerts, investigations, escalations, and case-management records. These operational records can reveal weaknesses that may not be visible through policies, compliance documentation, management reports, KPIs, or conventional dashboards.

Peril-Lens analyzes structured SOC evidence to surface **potential supervisory signals** such as:

- 🔍 Execution gaps
- 🌑 Negative-space conditions
- 🚨 Unusual operational patterns
- 📊 Peer deviations
- 🧭 Supervisory attention indicators
- 🎯 High-value samples for manual examination

The platform is designed to **support human supervisory judgement — not replace it**.

---

## 🎯 Problem Context

SOC assessments often rely on evidence distributed across alerts, cases, investigations, escalation records, monitoring information, and asset inventories.

A challenge arises when reported controls and metrics appear healthy while operational evidence tells a different story.

Examples include:

- High-severity alerts being closed unusually quickly
- Critical alerts lacking expected escalation
- Repeated alerts affecting the same asset without visible remediation
- Investigations containing repetitive or template-like patterns
- Critical systems showing unexpectedly low monitoring activity
- Important alert categories appearing absent
- Workloads or closure behaviour deviating significantly from peers
- Operational metrics appearing inconsistent with underlying evidence

These signals may be difficult to identify consistently when large volumes of records must be reviewed manually.

**Peril-Lens addresses this gap through structured, explainable supervisory analytics.**

---

## 💡 What Peril-Lens Does

Peril-Lens follows an evidence-to-signal workflow:

```text
┌─────────────────────────────┐
│     Structured SOC Data     │
│                             │
│ Alerts • Cases •            │
│ Investigations • Escalation │
│ Monitoring • Assets         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Data Validation &            │
│ Feature Engineering          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│       Supervisory Analytics Layer       │
│                                         │
│  Execution Gaps     Negative Space      │
│  Operational       Peer Benchmarking    │
│  Patterns          Supervisory Signals  │
└───────────────────┬─────────────────────┘
                    │
                    ▼
┌─────────────────────────────┐
│ Explainability & Evidence   │
│                             │
│ Why was it flagged?         │
│ What evidence supports it?  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Supervisory Prioritization  │
│                             │
│ Entities • Controls •       │
│ Processes • Alert Samples   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Peril-Lens Dashboard   │
│                             │
│ Human Supervisory Review    │
└─────────────────────────────┘
