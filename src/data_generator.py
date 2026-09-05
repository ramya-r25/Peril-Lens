import pandas as pd
import random
random.seed(42)
entities = [
    {
        "entity_id": "CSE-001",
        "entity_name": "NorthGrid Power",
        "sector": "Energy",
        "entity_size": "Large"
    },
    {
        "entity_id": "CSE-002",
        "entity_name": "MetroBank",
        "sector": "Banking",
        "entity_size": "Large"
    },
    {
        "entity_id": "CSE-003",
        "entity_name": "AeroLink Systems",
        "sector": "Transport",
        "entity_size": "Medium"
    },
    {
        "entity_id": "CSE-004",
        "entity_name": "NationalHealth Network",
        "sector": "Healthcare",
        "entity_size": "Large"
    },
    {
        "entity_id": "CSE-005",
        "entity_name": "SecureTel Communications",
        "sector": "Telecommunications",
        "entity_size": "Large"
    },
    {
        "entity_id": "CSE-006",
        "entity_name": "RiverWater Utilities",
        "sector": "Water",
        "entity_size": "Medium"
    }
]


df = pd.DataFrame(entities)

df.to_csv(
    "data/synthetic/entities.csv",
    index=False
)

print(df)

assessments = [
    {
        "assessment_id": "A-001",
        "entity_id": "CSE-001",
        "period_start": "2026-01-01",
        "period_end": "2026-03-31",
        "submission_date": "2026-04-10"
    },
    {
        "assessment_id": "A-002",
        "entity_id": "CSE-001",
        "period_start": "2026-04-01",
        "period_end": "2026-06-30",
        "submission_date": "2026-07-10"
    },
    {
        "assessment_id": "A-003",
        "entity_id": "CSE-002",
        "period_start": "2026-01-01",
        "period_end": "2026-03-31",
        "submission_date": "2026-04-10"
    },
    {
        "assessment_id": "A-004",
        "entity_id": "CSE-002",
        "period_start": "2026-04-01",
        "period_end": "2026-06-30",
        "submission_date": "2026-07-10"
    },
    {
        "assessment_id": "A-005",
        "entity_id": "CSE-003",
        "period_start": "2026-01-01",
        "period_end": "2026-03-31",
        "submission_date": "2026-04-10"
    },
    {
        "assessment_id": "A-006",
        "entity_id": "CSE-004",
        "period_start": "2026-01-01",
        "period_end": "2026-03-31",
        "submission_date": "2026-04-10"
    },
    {
        "assessment_id": "A-007",
        "entity_id": "CSE-005",
        "period_start": "2026-01-01",
        "period_end": "2026-03-31",
        "submission_date": "2026-04-10"
    },
    {
        "assessment_id": "A-008",
        "entity_id": "CSE-006",
        "period_start": "2026-01-01",
        "period_end": "2026-03-31",
        "submission_date": "2026-04-10"
    }
]

assessments_df = pd.DataFrame(assessments)

assessments_df.to_csv(
    "data/synthetic/assessments.csv",
    index=False
)

print("\nAssessments:")
print(assessments_df)

assets = [
    {
        "asset_id": "AST-001",
        "entity_id": "CSE-001",
        "asset_name": "PowerGrid Control System",
        "asset_type": "Industrial Control System",
        "criticality": "Critical",
        "business_function": "Power Operations",
        "expected_monitoring": True
    },
    {
        "asset_id": "AST-002",
        "entity_id": "CSE-001",
        "asset_name": "Corporate Network",
        "asset_type": "Enterprise Network",
        "criticality": "High",
        "business_function": "Corporate IT",
        "expected_monitoring": True
    },
    {
        "asset_id": "AST-003",
        "entity_id": "CSE-002",
        "asset_name": "Core Banking Platform",
        "asset_type": "Application Server",
        "criticality": "Critical",
        "business_function": "Banking Operations",
        "expected_monitoring": True
    },
    {
        "asset_id": "AST-004",
        "entity_id": "CSE-002",
        "asset_name": "Employee Network",
        "asset_type": "Enterprise Network",
        "criticality": "Medium",
        "business_function": "Corporate IT",
        "expected_monitoring": True
    },
    {
        "asset_id": "AST-005",
        "entity_id": "CSE-003",
        "asset_name": "Flight Operations System",
        "asset_type": "Operational System",
        "criticality": "Critical",
        "business_function": "Flight Operations",
        "expected_monitoring": True
    },
    {
        "asset_id": "AST-006",
        "entity_id": "CSE-004",
        "asset_name": "Patient Information System",
        "asset_type": "Healthcare Application",
        "criticality": "Critical",
        "business_function": "Healthcare Services",
        "expected_monitoring": True
    },
    {
        "asset_id": "AST-007",
        "entity_id": "CSE-005",
        "asset_name": "Telecom Core Network",
        "asset_type": "Network Infrastructure",
        "criticality": "Critical",
        "business_function": "Telecommunications",
        "expected_monitoring": True
    },
    {
        "asset_id": "AST-008",
        "entity_id": "CSE-006",
        "asset_name": "Water Treatment Control System",
        "asset_type": "Industrial Control System",
        "criticality": "Critical",
        "business_function": "Water Operations",
        "expected_monitoring": True
    }
]

assets_df = pd.DataFrame(assets)

assets_df.to_csv(
    "data/synthetic/assets.csv",
    index=False
)

print("\nAssets:")
print(assets_df)

import random
from datetime import datetime, timedelta


# -----------------------------
# Alert Data Generation
# -----------------------------

alert_categories = [
    "Authentication",
    "Network Anomaly",
    "Malware Detection",
    "Privilege Escalation",
    "Data Access",
    "Endpoint Security"
]

sources = [
    "SIEM",
    "EDR",
    "IDS",
    "Firewall",
    "IAM"
]

severities = [
    "Low",
    "Medium",
    "High",
    "Critical"
]


alerts = []

alert_counter = 1

for assessment in assessments:

    assessment_id = assessment["assessment_id"]
    entity_id = assessment["entity_id"]

    # Get assets belonging to this entity
    entity_assets = [
        asset for asset in assets
        if asset["entity_id"] == entity_id
    ]

    start_date = datetime.strptime(
        assessment["period_start"],
        "%Y-%m-%d"
    )

    for _ in range(100):

        asset = random.choice(entity_assets)

        severity = random.choices(
            severities,
            weights=[40, 30, 20, 10]
        )[0]

        alert_time = start_date + timedelta(
            days=random.randint(0, 89),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        acknowledged = random.random() < 0.95

        acknowledgement_time = None

        if acknowledged:
            acknowledgement_time = (
                alert_time
                + timedelta(
                    minutes=random.randint(5, 180)
                )
            )

        alerts.append({
            "alert_id": f"ALT-{alert_counter:04d}",
            "assessment_id": assessment_id,
            "asset_id": asset["asset_id"],
            "timestamp": alert_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "severity": severity,
            "alert_category": random.choice(
                alert_categories
            ),
            "source": random.choice(sources),
            "acknowledged": acknowledged,
            "acknowledgement_time": (
                acknowledgement_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if acknowledgement_time
                else None
            ),
            "case_id": None
        })

        alert_counter += 1


alerts_df = pd.DataFrame(alerts)

alerts_df.to_csv(
    "data/synthetic/alerts.csv",
    index=False
)

print("\nAlerts:")
print(alerts_df.head())
print(f"\nTotal alerts generated: {len(alerts_df)}")
# -------------------------
# Case Generation
# -------------------------

cases = []
case_counter = 1

for alert in alerts:
    # Only some alerts become cases
    if random.random() < 0.70:

        case_created_time = datetime.strptime(
            alert["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )

        priority = alert["severity"]

        # Most cases are resolved, but some remain open
        status = random.choices(
            ["Closed", "Open", "In Progress"],
            weights=[75, 10, 15]
        )[0]

        disposition = random.choice([
            "True Positive",
            "False Positive",
            "Benign",
            "Needs Review"
        ])

        closure_time = None
        closure_reason = None

        if status == "Closed":
            closure_time = (
                case_created_time
                + timedelta(
                    hours=random.randint(1, 72)
                )
            )

            closure_reason = random.choice([
                "Resolved",
                "False Positive",
                "Contained",
                "No Further Action"
            ])

        case_id = f"CASE-{case_counter:04d}"

        cases.append({
            "case_id": case_id,
            "assessment_id": alert["assessment_id"],
            "case_created_time": case_created_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "priority": priority,
            "status": status,
            "disposition": disposition,
            "closure_time": (
                closure_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if closure_time
                else None
            ),
            "closure_reason": closure_reason
        })

        # Link the alert to its case
        alert["case_id"] = case_id

        case_counter += 1


cases_df = pd.DataFrame(cases)

cases_df.to_csv(
    "data/synthetic/cases.csv",
    index=False
)

print("\nCases:")
print(cases_df.head())

print(f"\nTotal cases generated: {len(cases_df)}")

# -------------------------
# Investigation Generation
# -------------------------

investigations = []
investigation_counter = 1

for case in cases:

    # Not every case gets an investigation
    if random.random() < 0.85:

        start_time = datetime.strptime(
            case["case_created_time"],
            "%Y-%m-%d %H:%M:%S"
        )

        # Investigation duration varies
        duration_minutes = random.randint(10, 480)

        end_time = start_time + timedelta(
            minutes=duration_minutes
        )

        evidence_count = random.randint(0, 15)

        steps_recorded = random.randint(0, 10)

        root_cause_identified = random.random() < 0.65

        remediation_recorded = random.random() < 0.60

        template_id = random.choice([
            "TEMP-001",
            "TEMP-002",
            "TEMP-003",
            None
        ])

        notes_length = random.randint(20, 1000)

        investigations.append({
            "investigation_id": (
                f"INV-{investigation_counter:04d}"
            ),
            "case_id": case["case_id"],
            "start_time": start_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "end_time": end_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "evidence_count": evidence_count,
            "steps_recorded": steps_recorded,
            "root_cause_identified": root_cause_identified,
            "remediation_recorded": remediation_recorded,
            "template_id": template_id,
            "notes_length": notes_length
        })

        investigation_counter += 1


investigations_df = pd.DataFrame(investigations)

investigations_df.to_csv(
    "data/synthetic/investigations.csv",
    index=False
)

print("\nInvestigations:")
print(investigations_df.head())

print(
    f"\nTotal investigations generated: "
    f"{len(investigations_df)}"
)

# -------------------------
# Escalation Generation
# -------------------------

escalations = []
escalation_counter = 1

for case in cases:

    # Not every case requires escalation
    if random.random() < 0.30:

        escalation_time = datetime.strptime(
            case["case_created_time"],
            "%Y-%m-%d %H:%M:%S"
        ) + timedelta(
            minutes=random.randint(30, 1440)
        )

        escalation_level = random.choice([
            "Level 1",
            "Level 2",
            "Level 3"
        ])

        escalated_to = random.choice([
            "SOC Lead",
            "Incident Response Team",
            "Security Manager",
            "CISO Office"
        ])

        escalation_reason = random.choice([
            "High Severity Alert",
            "Critical Asset Involved",
            "Potential Security Incident",
            "Repeated Alert Pattern",
            "Investigation Requires Escalation"
        ])

        escalations.append({
            "escalation_id": (
                f"ESC-{escalation_counter:04d}"
            ),
            "case_id": case["case_id"],
            "escalated": True,
            "escalation_level": escalation_level,
            "escalated_to": escalated_to,
            "escalation_time": escalation_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "escalation_reason": escalation_reason
        })

        escalation_counter += 1


escalations_df = pd.DataFrame(escalations)

escalations_df.to_csv(
    "data/synthetic/escalations.csv",
    index=False
)

print("\nEscalations:")
print(escalations_df.head())

print(
    f"\nTotal escalations generated: "
    f"{len(escalations_df)}"
)

# -------------------------
# Monitoring Generation
# -------------------------

monitoring = []
monitoring_counter = 1

for assessment in assessments:

    assessment_id = assessment["assessment_id"]
    entity_id = assessment["entity_id"]

    # Get assets belonging to this entity
    entity_assets = [
        asset for asset in assets
        if asset["entity_id"] == entity_id
    ]

    for asset in entity_assets:

        # Each assessment represents roughly 90 days
        expected_coverage_hours = 2160

        # Observed coverage varies
        observed_coverage_hours = random.randint(
            1200,
            2160
        )

        telemetry_available = (
            observed_coverage_hours > 0
        )

        monitoring.append({
            "monitoring_id": (
                f"MON-{monitoring_counter:04d}"
            ),
            "assessment_id": assessment_id,
            "asset_id": asset["asset_id"],
            "expected_coverage_hours": (
                expected_coverage_hours
            ),
            "observed_coverage_hours": (
                observed_coverage_hours
            ),
            "telemetry_available": (
                telemetry_available
            )
        })

        monitoring_counter += 1


monitoring_df = pd.DataFrame(monitoring)

monitoring_df.to_csv(
    "data/synthetic/monitoring.csv",
    index=False
)

print("\nMonitoring:")
print(monitoring_df.head())

print(
    f"\nTotal monitoring records generated: "
    f"{len(monitoring_df)}"
)