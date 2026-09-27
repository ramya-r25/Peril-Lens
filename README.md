# Peril-Lens

## Supervisory Analytics Tool for SOC Assessment (SAT-SA)

**SIH Problem Statement:** SIH26157  
**Organization:** National Technical Research Organisation (NTRO)  
**Category:** Software  
**Theme:** Blockchain & Cybersecurity

---

## 1. Overview

**Peril-Lens** is a supervisory analytics platform designed to assist supervisors in analysing structured SOC alert and case-management data from Critical Sector Entities (CSEs).

The platform focuses on identifying operational evidence that may indicate:

- Potential execution gaps
- Potential negative-space conditions
- Operational anomalies and suspicious patterns
- Peer deviations
- Unusual investigation or escalation behaviour
- Entities requiring supervisory attention
- Alert and case samples requiring manual review

Peril-Lens is designed as a **supervisory analytics capability**, not as a replacement for a Security Operations Centre (SOC), SIEM, real-time monitoring system, or human supervisory judgement.

The platform follows a human-in-the-loop approach in which analytical findings are presented with supporting evidence and rationale for further examination by supervisors.

---

## 2. Problem Statement

Manual review of SOC alerts and case-management records can reveal operational weaknesses that may not be visible through conventional reports, policies, audits, KPIs, or compliance documentation.

However, manual analysis becomes resource-intensive when supervisory assessments involve:

- Multiple Critical Sector Entities
- Large volumes of alert and case records
- Multiple assessment periods
- Repetitive investigation patterns
- Cross-entity comparisons
- Missing or unexpected operational evidence

Peril-Lens addresses this challenge by applying structured supervisory analytics to periodic operational data and helping supervisors identify where deeper manual review may be required.

---

## 3. Proposed Solution

Peril-Lens follows the workflow:

**Structured Evidence → Analytics → Supervisory Signals → Prioritisation → Explanation → Human Review**

The system processes structured SOC and case-management information and generates supervisory signals across multiple analytical dimensions.

These signals are not treated as final compliance or security judgements. They are intended to support human examiners by identifying areas that may warrant further investigation.

---

## 4. Key Capabilities

### 4.1 Data Ingestion

Supports structured supervisory data used for analysis, including information representing:

- Security alert metadata
- Case-management records
- Investigation activity
- Escalation information
- Alert disposition and closure information
- Asset and system information where available

---

### 4.2 Execution Gap Detection

Identifies patterns where reported or expected operational effectiveness may not be supported by the available operational evidence.

Examples include:

- Unusually rapid case closure
- Weak investigation behaviour
- Missing escalation patterns
- Repetitive investigation behaviour
- Operational activity inconsistent with expected controls

---

### 4.3 Negative Space Detection

Identifies situations where expected operational evidence is absent or unusually limited.

Examples include:

- Missing monitoring evidence
- Low activity in areas where activity may be expected
- Missing investigation or escalation records
- Potential monitoring blind spots

---

### 4.4 Anomaly and Operational Pattern Analysis

Analyses operational records to identify unusual patterns, outliers and behaviours that may require supervisory attention.

---

### 4.5 Peer Benchmarking

Compares relevant operational indicators across CSEs to identify significant deviations from peer patterns.

Peer comparison is used as a supervisory signal and does not by itself represent a compliance judgement.

---

### 4.6 Supervisory Prioritisation

Combines analytical findings into a prioritisation view that helps supervisors determine:

- Which entities may require attention
- Which assessments may require deeper review
- Which controls or processes may warrant examination
- Which alert or case samples may be useful for manual review

---

### 4.7 Explainability and Evidence

Peril-Lens provides supporting information for analytical findings so that supervisors can understand:

- What was detected
- Why it was flagged
- Which operational evidence contributed to the finding
- Which entity or assessment is affected

The objective is to preserve traceability and support auditable supervisory decision-making.

---

### 4.8 Supervisory Dashboards and Reporting

The platform provides dashboard-based views for:

- Supervisory indicators
- Assessment trends
- Entity-level observations
- Prioritisation
- Notable signals
- Supporting evidence and drill-down analysis

---

## 5. Analytics Methodology

The analytical pipeline is organised into modular components:

```text
Structured CSE Data
        |
        v
Data Ingestion
        |
        v
Preprocessing & Feature Extraction
        |
        v
+-------------------------------+
| Supervisory Analytics         |
|                               |
| Execution Gap Detection       |
| Negative Space Detection      |
| Anomaly Detection             |
| Operational Pattern Analysis  |
| Peer Benchmarking             |
+-------------------------------+
        |
        v
Supervisory Risk Indicators
        |
        v
Prioritisation
        |
        v
Evidence & Explainability
        |
        v
Dashboard / Reports
        |
        v
Human Supervisory Review