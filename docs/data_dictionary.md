# SAT-SA Data Dictionary

## Purpose

This document defines the data required by SAT-SA to perform
supervisory analytics on SOC alert and case-management evidence.

The data is designed to support:

- Execution gap detection
- Negative-space detection
- Operational anomaly detection
- Peer benchmarking
- Supervisory risk indicators
- Manual review prioritization
- Explainability and auditability

---

## 1. Entities

Represents Critical Sector Entities (CSEs) being assessed.

| Field | Description |
|---|---|
| entity_id | Unique identifier of the entity |
| entity_name | Name of the entity |
| sector | Critical infrastructure sector |
| entity_size | Relative organizational size/category |

---

## 2. Assessments

Represents a periodic supervisory data submission from an entity.

| Field | Description |
|---|---|
| assessment_id | Unique assessment identifier |
| entity_id | Entity being assessed |
| period_start | Start of assessment period |
| period_end | End of assessment period |
| submission_date | Date data was submitted |

---

## 3. Assets

Represents systems/assets belonging to an entity.

| Field | Description |
|---|---|
| asset_id | Unique asset identifier |
| entity_id | Entity owning the asset |
| asset_name | Asset/system name |
| asset_type | Type of system or asset |
| criticality | Criticality level |
| business_function | Business function supported |
| expected_monitoring | Whether monitoring is expected |

---

## 4. Alerts

Represents SOC alert metadata.

| Field | Description |
|---|---|
| alert_id | Unique alert identifier |
| assessment_id | Assessment associated with the alert |
| asset_id | Asset associated with the alert |
| timestamp | Alert generation time |
| severity | Alert severity |
| alert_category | Category of alert |
| source | Source/system generating the alert |
| acknowledged | Whether the alert was acknowledged |
| acknowledgement_time | Time at which alert was acknowledged |
| case_id | Associated case, if one exists |

---

## 5. Cases

Represents case-management records created from alerts.

| Field | Description |
|---|---|
| case_id | Unique case identifier |
| assessment_id | Assessment associated with the case |
| case_created_time | Time case was created |
| priority | Case priority |
| status | Current/final case status |
| disposition | Final case disposition |
| closure_time | Time case was closed |
| closure_reason | Recorded reason for closure |

---

## 6. Investigations

Represents investigation activity associated with cases.

| Field | Description |
|---|---|
| investigation_id | Unique investigation identifier |
| case_id | Associated case |
| start_time | Investigation start time |
| end_time | Investigation end time |
| evidence_count | Number of recorded evidence items |
| steps_recorded | Number of investigation steps recorded |
| root_cause_identified | Whether root cause was identified |
| remediation_recorded | Whether remediation was recorded |
| template_id | Investigation template used |
| notes_length | Length of investigation notes |

---

## 7. Escalations

Represents escalation activity associated with cases.

| Field | Description |
|---|---|
| escalation_id | Unique escalation identifier |
| case_id | Associated case |
| escalation_level | Level/type of escalation |
| escalation_time | Time escalation occurred |
| escalation_reason | Recorded reason for escalation |

---

## 8. Monitoring

Represents expected versus observed monitoring activity.

| Field | Description |
|---|---|
| monitoring_id | Unique monitoring record |
| assessment_id | Associated assessment |
| asset_id | Monitored asset |
| expected_coverage_hours | Expected monitoring coverage |
| observed_coverage_hours | Observed monitoring coverage |
| telemetry_available | Whether telemetry/evidence was available |

---

# Derived Analytical Indicators

The following values will NOT be stored as raw data.
They will be calculated by SAT-SA.

Examples:

- Acknowledgement time
- Investigation duration
- Closure time
- Critical alert investigation rate
- Critical alert escalation rate
- Premature closure rate
- Investigation completeness score
- Repetitive investigation rate
- Monitoring coverage gap
- Peer deviation score
- Entity supervisory risk score
- Review priority score

---

# Important Design Principle

SAT-SA should analyze operational evidence rather than directly
declaring that an entity is compliant or non-compliant.

A detected pattern should produce:

1. Supervisory indicator
2. Supporting evidence
3. Reason for flagging
4. Relevant entity/process
5. Representative records for manual review

Final supervisory judgement remains with the human examiner.