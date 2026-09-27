import pandas as pd
import random
random.seed(42)
# --------------------------------------------------
# Synthetic assessment scenarios
# --------------------------------------------------

scenario_profiles = {
    "A-001": "healthy",
    "A-002": "execution_gap",
    "A-003": "healthy",
    "A-004": "missing_escalation",
    "A-005": "negative_space",
    "A-006": "repetitive_investigation",
    "A-007": "metric_gaming",
    "A-008": "mixed"
}
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

    # Identify the hidden scenario for this assessment
    scenario = scenario_profiles.get(
        assessment_id,
        "healthy"
    )

    # Get assets belonging to this entity
    entity_assets = [
        asset for asset in assets
        if asset["entity_id"] == entity_id
    ]

    start_date = datetime.strptime(
        assessment["period_start"],
        "%Y-%m-%d"
    )

    end_date = datetime.strptime(
        assessment["period_end"],
        "%Y-%m-%d"
    )

    # Number of days in the assessment period
    assessment_days = (
        end_date - start_date
    ).days

    for _ in range(100):

        asset = random.choice(entity_assets)

        # Default severity distribution
        severity = random.choices(
            severities,
            weights=[40, 30, 20, 10]
        )[0]

        # Execution-gap assessments contain
        # more high/critical alerts
        if scenario == "execution_gap":
            severity = random.choices(
                severities,
                weights=[25, 25, 30, 20]
            )[0]

        # Generate timestamp within the actual
        # assessment period
        alert_time = start_date + timedelta(
            days=random.randint(0, assessment_days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        # Avoid generating timestamps beyond period end
        if alert_time > end_date + timedelta(days=1) - timedelta(seconds=1):
            alert_time = end_date + timedelta(
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
# -------------------------
# -------------------------
# -------------------------
# Case Generation
# -------------------------

cases = []
case_counter = 1

# Keep track of cases created within each assessment.
# This allows related alerts to share an existing case.
assessment_cases = {}


for alert in alerts:

    # Not every alert becomes a case
    if random.random() < 0.70:

        assessment_id = alert["assessment_id"]

        scenario = scenario_profiles.get(
            assessment_id,
            "healthy"
        )

        # --------------------------------------------------
        # Try to attach the alert to an existing related case
        # --------------------------------------------------

        related_cases = []

        for existing_case in assessment_cases.get(
            assessment_id,
            []
        ):

            # Same asset is the strongest relationship.
            if existing_case["asset_id"] == alert["asset_id"]:

                existing_case_time = datetime.strptime(
                    existing_case["case_created_time"],
                    "%Y-%m-%d %H:%M:%S"
                )

                alert_time = datetime.strptime(
                    alert["timestamp"],
                    "%Y-%m-%d %H:%M:%S"
                )

                time_difference_hours = abs(
                    (alert_time - existing_case_time).total_seconds()
                    / 3600
                )

                # Related alerts occurring within 24 hours
                # can belong to the same case.
                if time_difference_hours <= 24:
                    related_cases.append(existing_case)


        # --------------------------------------------------
        # Decide whether to reuse an existing case
        # --------------------------------------------------

        if related_cases and random.random() < 0.35:

            selected_case = random.choice(
                related_cases
            )

            alert["case_id"] = selected_case["case_id"]

            continue


        # --------------------------------------------------
        # Create a new case
        # --------------------------------------------------

        case_created_time = datetime.strptime(
            alert["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )

        priority = alert["severity"]


        # ----------------------------------------
        # Default case status
        # ----------------------------------------

        status = random.choices(
            ["Closed", "Open", "In Progress"],
            weights=[75, 10, 15]
        )[0]


        # ----------------------------------------
        # Default disposition
        # ----------------------------------------

        disposition = random.choices(
            [
                "True Positive",
                "False Positive",
                "Benign",
                "Needs Review"
            ],
            weights=[35, 30, 20, 15]
        )[0]


        # Cases needing review are more likely
        # to remain open or in progress

        if disposition == "Needs Review":

            status = random.choices(
                ["Open", "In Progress", "Closed"],
                weights=[45, 40, 15]
            )[0]


        closure_time = None
        closure_reason = None


        # ----------------------------------------
        # Closed Case
        # ----------------------------------------

        if status == "Closed":

            # Default closure time
            closure_hours = random.randint(
                1,
                72
            )


            # ----------------------------------------
            # Execution Gap
            # ----------------------------------------

            if (
                scenario == "execution_gap"
                and priority in ["High", "Critical"]
            ):

                if random.random() < 0.60:

                    closure_hours = random.randint(
                        1,
                        8
                    )


            # ----------------------------------------
            # Metric Gaming
            # ----------------------------------------

            elif (
                scenario == "metric_gaming"
                and priority in ["High", "Critical"]
            ):

                if random.random() < 0.80:

                    closure_hours = random.randint(
                        1,
                        6
                    )


            # ----------------------------------------
            # Mixed Scenario
            # ----------------------------------------

            elif (
                scenario == "mixed"
                and priority in ["High", "Critical"]
            ):

                if random.random() < 0.70:

                    closure_hours = random.randint(
                        1,
                        8
                    )


            closure_time = (
                case_created_time
                + timedelta(
                    hours=closure_hours
                )
            )


            # ----------------------------------------
            # Closure Reason
            # ----------------------------------------

            if disposition == "False Positive":

                closure_reason = "False Positive"

            elif disposition == "Benign":

                closure_reason = "No Further Action"

            elif disposition == "True Positive":

                closure_reason = random.choice([
                    "Resolved",
                    "Contained"
                ])

            else:

                closure_reason = "Needs Further Review"


        # ----------------------------------------
        # Create Case Record
        # ----------------------------------------

        case_id = f"CASE-{case_counter:04d}"


        case_record = {

            "case_id": case_id,

            "assessment_id": assessment_id,

            "case_created_time": (
                case_created_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
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

            "closure_reason": closure_reason,

            # Internal field used only while generating data.
            # It will NOT be written to cases.csv.
            "asset_id": alert["asset_id"]
        }


        cases.append(case_record)


        # Store the case so later related alerts
        # can potentially join it.
        assessment_cases.setdefault(
            assessment_id,
            []
        ).append(case_record)


        # Link the alert to its case
        alert["case_id"] = case_id


        case_counter += 1


# --------------------------------------------------
# Remove internal generator-only field
# --------------------------------------------------

for case in cases:

    case.pop(
        "asset_id",
        None
    )


# Convert cases to DataFrame
cases_df = pd.DataFrame(
    cases
)


# Save cases
cases_df.to_csv(
    "data/synthetic/cases.csv",
    index=False
)


# Save alerts again after case IDs have been assigned
alerts_df = pd.DataFrame(
    alerts
)


alerts_df.to_csv(
    "data/synthetic/alerts.csv",
    index=False
)


print("\nCases:")
print(
    cases_df.head()
)


print(
    f"\nTotal cases generated: "
    f"{len(cases_df)}"
)
# Monitoring Generation
# -------------------------

monitoring = []
monitoring_counter = 1

for assessment in assessments:

    assessment_id = assessment["assessment_id"]
    entity_id = assessment["entity_id"]

    scenario = scenario_profiles.get(
        assessment_id,
        "healthy"
    )

    # Convert assessment dates to datetime
    period_start = datetime.strptime(
        assessment["period_start"],
        "%Y-%m-%d"
    )

    period_end = datetime.strptime(
        assessment["period_end"],
        "%Y-%m-%d"
    )

    # Calculate expected monitoring coverage
    expected_coverage_hours = int(
        (period_end - period_start).total_seconds() / 3600
    ) + 24

    # Get assets belonging to this entity
    entity_assets = [
        asset for asset in assets
        if asset["entity_id"] == entity_id
    ]

    for asset in entity_assets:

        # ----------------------------------------
        # Normal monitoring behavior
        # ----------------------------------------

        coverage_ratio = random.uniform(
            0.85,
            1.00
        )

        # ----------------------------------------
        # Negative-space scenario
        # ----------------------------------------
        # A-005 intentionally has poor monitoring
        # coverage for its critical asset.
        #
        # The raw data contains the evidence;
        # it does NOT contain a "negative_space"
        # label.
        # ----------------------------------------

        if scenario == "negative_space":

            if asset["criticality"] == "Critical":

                coverage_ratio = random.uniform(
                    0.15,
                    0.40
                )

            else:

                coverage_ratio = random.uniform(
                    0.70,
                    0.90
                )

        # ----------------------------------------
        # Mixed scenario
        # ----------------------------------------

        elif scenario == "mixed":

            if asset["criticality"] == "Critical":

                coverage_ratio = random.uniform(
                    0.50,
                    0.75
                )

        # Calculate observed coverage
        observed_coverage_hours = int(
            expected_coverage_hours * coverage_ratio
        )

        # Telemetry may be completely unavailable
        # in the negative-space scenario.
        if (
            scenario == "negative_space"
            and asset["criticality"] == "Critical"
        ):
            telemetry_available = random.random() < 0.35
        else:
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
# Investigation Generation
# Investigation Generation
# -------------------------

investigations = []
investigation_counter = 1

for case in cases:

    scenario = scenario_profiles.get(
        case["assessment_id"],
        "healthy"
    )

    if random.random() < 0.85:

        start_time = datetime.strptime(
            case["case_created_time"],
            "%Y-%m-%d %H:%M:%S"
        )

        # ----------------------------------------
        # Default investigation behavior
        # ----------------------------------------

        duration_minutes = random.randint(10, 480)
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

        # ----------------------------------------
        # Execution Gap
        # ----------------------------------------

        if (
            scenario == "execution_gap"
            and case["priority"] in ["High", "Critical"]
        ):

            if random.random() < 0.65:

                duration_minutes = random.randint(
                    5,
                    45
                )

                evidence_count = random.randint(
                    0,
                    3
                )

                steps_recorded = random.randint(
                    0,
                    2
                )

                root_cause_identified = (
                    random.random() < 0.15
                )

                remediation_recorded = (
                    random.random() < 0.10
                )

                notes_length = random.randint(
                    20,
                    150
                )

        # ----------------------------------------
        # Metric Gaming
        # ----------------------------------------

        elif (
            scenario == "metric_gaming"
            and case["priority"] in ["High", "Critical"]
        ):

            if random.random() < 0.70:

                duration_minutes = random.randint(
                    5,
                    30
                )

                evidence_count = random.randint(
                    1,
                    4
                )

                steps_recorded = random.randint(
                    1,
                    3
                )

                root_cause_identified = (
                    random.random() < 0.20
                )

                remediation_recorded = (
                    random.random() < 0.15
                )

                notes_length = random.randint(
                    30,
                    180
                )

                template_id = random.choice([
                    "TEMP-001",
                    "TEMP-002"
                ])

        # ----------------------------------------
        # Repetitive Investigation
        # ----------------------------------------

        elif scenario == "repetitive_investigation":

            duration_minutes = random.randint(
                10,
                40
            )

            evidence_count = random.randint(
                1,
                3
            )

            steps_recorded = random.randint(
                1,
                3
            )

            root_cause_identified = (
                random.random() < 0.20
            )

            remediation_recorded = (
                random.random() < 0.15
            )

            notes_length = random.randint(
                50,
                180
            )

            # Strong template reuse
            template_id = random.choice([
                "TEMP-001",
                "TEMP-001",
                "TEMP-001",
                "TEMP-002"
            ])

        # ----------------------------------------
        # End time
        # ----------------------------------------

        end_time = (
            start_time
            + timedelta(minutes=duration_minutes)
        )

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
            "root_cause_identified": (
                root_cause_identified
            ),
            "remediation_recorded": (
                remediation_recorded
            ),
            "template_id": template_id,
            "notes_length": notes_length
        })

        investigation_counter += 1


investigations_df = pd.DataFrame(
    investigations
)

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

    scenario = scenario_profiles.get(
        case["assessment_id"],
        "healthy"
    )

    # Default escalation probability
    escalation_probability = 0.20

    # ----------------------------------------
    # Execution Gap
    # ----------------------------------------

    if (
        scenario == "execution_gap"
        and case["priority"] in ["High", "Critical"]
    ):
        escalation_probability = 0.10

    # ----------------------------------------
    # Metric Gaming
    # ----------------------------------------

    elif (
        scenario == "metric_gaming"
        and case["priority"] in ["High", "Critical"]
    ):
        escalation_probability = 0.05

    # ----------------------------------------
    # Repetitive Investigation
    # ----------------------------------------

    elif scenario == "repetitive_investigation":

        if case["priority"] == "Critical":
            escalation_probability = 0.15

        elif case["priority"] == "High":
            escalation_probability = 0.10

    # ----------------------------------------
    # Mixed Scenario
    # ----------------------------------------

    elif scenario == "mixed":

        if case["priority"] == "Critical":
            escalation_probability = 0.50

        elif case["priority"] == "High":
            escalation_probability = 0.35

    # ----------------------------------------
    # Healthy Scenario
    # ----------------------------------------

    else:

        if case["priority"] == "Critical":
            escalation_probability = 0.60

        elif case["priority"] == "High":
            escalation_probability = 0.40

    # ----------------------------------------
    # Determine Escalation
    # ----------------------------------------

    escalated = random.random() < escalation_probability

    # Only create an escalation record
    # when the case is actually escalated
    if escalated:

        escalation_level = random.choice([
            "Level 1",
            "Level 2",
            "Level 3"
        ])

        escalated_to = random.choice([
            "SOC Manager",
            "Incident Response Team",
            "Security Lead",
            "CISO"
        ])

        escalation_time = datetime.strptime(
            case["case_created_time"],
            "%Y-%m-%d %H:%M:%S"
        ) + timedelta(
            minutes=random.randint(30, 720)
        )

        escalation_reason = random.choice([
            "High Severity",
            "Critical Asset",
            "Potential Security Incident",
            "Repeated Alert Pattern",
            "Investigation Requires Higher Review"
        ])

        escalation_id = (
            f"ESC-{escalation_counter:04d}"
        )

        escalations.append({
            "escalation_id": escalation_id,
            "case_id": case["case_id"],
            "escalated": True,
            "escalation_level": escalation_level,
            "escalated_to": escalated_to,
            "escalation_time": (
                escalation_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            ),
            "escalation_reason": escalation_reason
        })

        escalation_counter += 1


# Convert escalations to DataFrame
escalations_df = pd.DataFrame(
    escalations
)

# Save escalations
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