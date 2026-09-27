import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/synthetic")


# ----------------------------------------
# Load datasets
# ----------------------------------------

entities = pd.read_csv(DATA_DIR / "entities.csv")
assessments = pd.read_csv(DATA_DIR / "assessments.csv")
assets = pd.read_csv(DATA_DIR / "assets.csv")
alerts = pd.read_csv(DATA_DIR / "alerts.csv")
cases = pd.read_csv(DATA_DIR / "cases.csv")
monitoring = pd.read_csv(DATA_DIR / "monitoring.csv")
investigations = pd.read_csv(DATA_DIR / "investigations.csv")
escalations = pd.read_csv(DATA_DIR / "escalations.csv")


print("\n" + "=" * 60)
print("SAT-SA SYNTHETIC DATA VALIDATION")
print("=" * 60)


# ----------------------------------------
# 1. Record counts
# ----------------------------------------

print("\n[1] RECORD COUNTS")

datasets = {
    "Entities": entities,
    "Assessments": assessments,
    "Assets": assets,
    "Alerts": alerts,
    "Cases": cases,
    "Monitoring": monitoring,
    "Investigations": investigations,
    "Escalations": escalations
}

for name, df in datasets.items():
    print(f"{name:<20}: {len(df)}")


# ----------------------------------------
# 2. Check duplicate IDs
# ----------------------------------------

print("\n[2] DUPLICATE ID CHECK")

id_columns = {
    "Entities": (entities, "entity_id"),
    "Assessments": (assessments, "assessment_id"),
    "Assets": (assets, "asset_id"),
    "Alerts": (alerts, "alert_id"),
    "Cases": (cases, "case_id"),
    "Monitoring": (monitoring, "monitoring_id"),
    "Investigations": (investigations, "investigation_id"),
    "Escalations": (escalations, "escalation_id")
}

for name, (df, column) in id_columns.items():

    duplicates = df[column].duplicated().sum()

    if duplicates == 0:
        print(f"✓ {name}: No duplicate IDs")
    else:
        print(f"✗ {name}: {duplicates} duplicate IDs")


# ----------------------------------------
# 3. Referential integrity
# ----------------------------------------

print("\n[3] REFERENTIAL INTEGRITY")


def check_reference(
    child_df,
    child_column,
    parent_df,
    parent_column,
    relationship
):

    invalid = (
        ~child_df[child_column]
        .isin(parent_df[parent_column])
    ).sum()

    if invalid == 0:
        print(f"✓ {relationship}")
    else:
        print(
            f"✗ {relationship}: "
            f"{invalid} invalid references"
        )


check_reference(
    assessments,
    "entity_id",
    entities,
    "entity_id",
    "Assessments → Entities"
)

check_reference(
    assets,
    "entity_id",
    entities,
    "entity_id",
    "Assets → Entities"
)

check_reference(
    alerts,
    "assessment_id",
    assessments,
    "assessment_id",
    "Alerts → Assessments"
)

check_reference(
    alerts,
    "asset_id",
    assets,
    "asset_id",
    "Alerts → Assets"
)

check_reference(
    cases,
    "assessment_id",
    assessments,
    "assessment_id",
    "Cases → Assessments"
)

check_reference(
    investigations,
    "case_id",
    cases,
    "case_id",
    "Investigations → Cases"
)

check_reference(
    escalations,
    "case_id",
    cases,
    "case_id",
    "Escalations → Cases"
)

check_reference(
    monitoring,
    "assessment_id",
    assessments,
    "assessment_id",
    "Monitoring → Assessments"
)

check_reference(
    monitoring,
    "asset_id",
    assets,
    "asset_id",
    "Monitoring → Assets"
)


# ----------------------------------------
# 4. Missing values
# ----------------------------------------

print("\n[4] MISSING VALUE CHECK")

for name, df in datasets.items():

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if len(missing) == 0:

        print(f"✓ {name}: No missing values")

    else:

        print(f"\n{name}:")

        for column, count in missing.items():

            print(
                f"  {column}: {count}"
            )


# ----------------------------------------
# 5. Case status distribution
# ----------------------------------------

print("\n[5] CASE STATUS DISTRIBUTION")

print(
    cases["status"]
    .value_counts()
)


# ----------------------------------------
# 6. Case priority distribution
# ----------------------------------------

print("\n[6] CASE PRIORITY DISTRIBUTION")

print(
    cases["priority"]
    .value_counts()
)


# ----------------------------------------
# 7. Investigation quality indicators
# ----------------------------------------

print("\n[7] INVESTIGATION INDICATORS")

print(
    "Root cause identified:"
)

print(
    investigations[
        "root_cause_identified"
    ].value_counts()
)

print(
    "\nRemediation recorded:"
)

print(
    investigations[
        "remediation_recorded"
    ].value_counts()
)

print(
    "\nTemplate usage:"
)

print(
    investigations[
        "template_id"
    ].value_counts()
)


# ----------------------------------------
# 8. Monitoring coverage
# ----------------------------------------

print("\n[8] MONITORING COVERAGE")

monitoring["coverage_ratio"] = (
    monitoring["observed_coverage_hours"]
    /
    monitoring["expected_coverage_hours"]
)

print(
    monitoring[
        [
            "assessment_id",
            "asset_id",
            "expected_coverage_hours",
            "observed_coverage_hours",
            "coverage_ratio",
            "telemetry_available"
        ]
    ]
)


# ----------------------------------------
# 9. Escalation summary
# ----------------------------------------

print("\n[9] ESCALATION SUMMARY")

print(
    f"Total escalations: "
    f"{len(escalations)}"
)

print(
    "\nEscalation levels:"
)

print(
    escalations[
        "escalation_level"
    ].value_counts()
)


# ----------------------------------------
# Finished
# ----------------------------------------

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)