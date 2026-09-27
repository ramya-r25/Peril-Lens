import pandas as pd
from pathlib import Path

BASE = Path("data/synthetic")

FILES = {
    "entities": "entities.csv",
    "assessments": "assessments.csv",
    "assets": "assets.csv",
    "alerts": "alerts.csv",
    "cases": "cases.csv",
    "investigations": "investigations.csv",
    "escalations": "escalations.csv",
    "monitoring": "monitoring.csv",
}

REQUIRED = {
    "entities": ["entity_id", "entity_name", "sector", "entity_size"],
    "assessments": ["assessment_id", "entity_id", "period_start", "period_end", "submission_date"],
    "assets": ["asset_id", "entity_id", "asset_name", "asset_type", "criticality",
               "business_function", "expected_monitoring"],
    "alerts": ["alert_id", "assessment_id", "asset_id", "timestamp", "severity",
               "alert_category", "source", "acknowledged", "acknowledgement_time", "case_id"],
    "cases": ["case_id", "assessment_id", "case_created_time", "priority", "status",
              "disposition", "closure_time", "closure_reason"],
    "investigations": ["investigation_id", "case_id", "start_time", "end_time",
                       "evidence_count", "steps_recorded", "root_cause_identified",
                       "remediation_recorded", "template_id", "notes_length"],
    "escalations": ["escalation_id", "case_id", "escalated", "escalation_level",
                    "escalated_to", "escalation_time", "escalation_reason"],
    "monitoring": ["monitoring_id", "assessment_id", "asset_id",
                   "expected_coverage_hours", "observed_coverage_hours",
                   "telemetry_available"],
}

def load():
    data = {}
    for name, filename in FILES.items():
        path = BASE / filename
        if not path.exists():
            print(f"[MISSING] {path}")
            continue
        data[name] = pd.read_csv(path)
    return data

def check_ids(data):
    print("\n--- ID CHECKS ---")
    for name, df in data.items():
        id_col = next((c for c in df.columns if c.endswith("_id") and c in
                       ["entity_id","assessment_id","asset_id","alert_id","case_id",
                        "investigation_id","escalation_id","monitoring_id"]), None)
        if id_col:
            dup = df[id_col].duplicated().sum()
            null = df[id_col].isna().sum()
            print(f"{name:16} {id_col:20} duplicates={dup:4} nulls={null:4}")

def check_schema(data):
    print("\n--- SCHEMA CHECKS ---")
    for name, required in REQUIRED.items():
        if name not in data:
            continue
        missing = [c for c in required if c not in data[name].columns]
        print(f"{name:16} " + ("PASS" if not missing else f"MISSING: {missing}"))

def check_relationships(data):
    print("\n--- REFERENTIAL INTEGRITY ---")

    checks = [
        ("assessments.entity_id", "assessments", "entity_id", "entities", "entity_id"),
        ("assets.entity_id", "assets", "entity_id", "entities", "entity_id"),
        ("alerts.assessment_id", "alerts", "assessment_id", "assessments", "assessment_id"),
        ("alerts.asset_id", "alerts", "asset_id", "assets", "asset_id"),
        ("alerts.case_id", "alerts", "case_id", "cases", "case_id"),
        ("cases.assessment_id", "cases", "assessment_id", "assessments", "assessment_id"),
        ("investigations.case_id", "investigations", "case_id", "cases", "case_id"),
        ("escalations.case_id", "escalations", "case_id", "cases", "case_id"),
        ("monitoring.assessment_id", "monitoring", "assessment_id", "assessments", "assessment_id"),
        ("monitoring.asset_id", "monitoring", "asset_id", "assets", "asset_id"),
    ]

    for label, child, child_col, parent, parent_col in checks:
        if child not in data or parent not in data:
            continue
        values = data[child][child_col].dropna()
        bad = (~values.isin(data[parent][parent_col])).sum()
        print(f"{label:32} " + ("PASS" if bad == 0 else f"FAIL: {bad} orphan(s)"))

def check_dates(data):
    print("\n--- DATE / TIME CHECKS ---")

    if "assessments" in data:
        a = data["assessments"].copy()
        a["period_start"] = pd.to_datetime(a["period_start"], errors="coerce")
        a["period_end"] = pd.to_datetime(a["period_end"], errors="coerce")
        a["submission_date"] = pd.to_datetime(a["submission_date"], errors="coerce")
        bad_period = (a["period_end"] < a["period_start"]).sum()
        bad_submit = (a["submission_date"] < a["period_end"]).sum()
        print(f"Assessment date order:       {'PASS' if bad_period == 0 else f'{bad_period} bad'}")
        print(f"Submission after period end: {'PASS' if bad_submit == 0 else f'{bad_submit} bad'}")

    if "alerts" in data and "assessments" in data:
        alerts = data["alerts"].copy()
        assessments = data["assessments"].copy()
        alerts["timestamp"] = pd.to_datetime(alerts["timestamp"], errors="coerce")
        assessments["period_start"] = pd.to_datetime(assessments["period_start"], errors="coerce")
        assessments["period_end"] = pd.to_datetime(assessments["period_end"], errors="coerce")

        merged = alerts.merge(
            assessments[["assessment_id", "period_start", "period_end"]],
            on="assessment_id", how="left"
        )
        bad = ((merged["timestamp"] < merged["period_start"]) |
               (merged["timestamp"] > merged["period_end"] + pd.Timedelta(days=1))).sum()
        print(f"Alert timestamps in assessment period: {'PASS' if bad == 0 else f'{bad} outside'}")

def check_value_ranges(data):
    print("\n--- VALUE / RANGE CHECKS ---")

    if "monitoring" in data:
        m = data["monitoring"].copy()
        m["expected_coverage_hours"] = pd.to_numeric(m["expected_coverage_hours"], errors="coerce")
        m["observed_coverage_hours"] = pd.to_numeric(m["observed_coverage_hours"], errors="coerce")
        bad = ((m["expected_coverage_hours"] <= 0) |
               (m["observed_coverage_hours"] < 0) |
               (m["observed_coverage_hours"] > m["expected_coverage_hours"])).sum()
        print(f"Monitoring coverage ranges: {'PASS' if bad == 0 else f'{bad} invalid'}")

    if "investigations" in data:
        i = data["investigations"].copy()
        for col in ["evidence_count", "steps_recorded", "notes_length"]:
            i[col] = pd.to_numeric(i[col], errors="coerce")
        bad = ((i["evidence_count"] < 0) |
               (i["steps_recorded"] < 0) |
               (i["notes_length"] < 0)).sum()
        print(f"Investigation numeric ranges: {'PASS' if bad == 0 else f'{bad} invalid'}")

def distribution_summary(data):
    print("\n--- DATASET SIZE / DISTRIBUTION ---")
    for name, df in data.items():
        print(f"{name:16}: {len(df):6} rows")

    if "assessments" in data:
        print("\nAssessments per entity:")
        print(data["assessments"].groupby("entity_id").size().to_string())

    if "alerts" in data:
        print("\nAlerts per assessment:")
        print(data["alerts"].groupby("assessment_id").size().to_string())

    if "cases" in data:
        print("\nCases per assessment:")
        print(data["cases"].groupby("assessment_id").size().to_string())

    if "alerts" in data:
        print("\nAlert severity:")
        print(data["alerts"]["severity"].value_counts().to_string())

    if "cases" in data:
        print("\nCase status:")
        print(data["cases"]["status"].value_counts().to_string())

def case_relationship_summary(data):
    print("\n--- CASE / ALERT RELATIONSHIP ---")
    if "alerts" not in data or "cases" not in data:
        return

    alerts = data["alerts"]
    cases = data["cases"]

    linked = alerts["case_id"].dropna()
    unique_linked = linked.nunique()
    multi_alert_cases = linked.value_counts()
    multi = (multi_alert_cases > 1).sum()

    print(f"Alerts linked to cases:       {len(linked)} / {len(alerts)}")
    print(f"Unique linked cases:          {unique_linked}")
    print(f"Cases with 2+ alerts:         {multi}")

    if len(cases):
        investigations = data.get("investigations")
        if investigations is not None:
            print(f"Cases with investigation:     {investigations['case_id'].nunique()} / {len(cases)}")

def null_summary(data):
    print("\n--- MISSING VALUE SUMMARY ---")
    for name, df in data.items():
        nonzero = df.isna().sum()
        nonzero = nonzero[nonzero > 0]
        if len(nonzero):
            print(f"\n{name}:")
            print(nonzero.to_string())
        else:
            print(f"{name}: no missing values")

def main():
    print("SAT-SA FINAL DATASET AUDIT")
    print("=" * 60)

    data = load()

    if len(data) != len(FILES):
        print("\nSTOP: one or more expected CSV files are missing.")
        return

    check_schema(data)
    check_ids(data)
    check_relationships(data)
    check_dates(data)
    check_value_ranges(data)
    distribution_summary(data)
    case_relationship_summary(data)
    null_summary(data)

    print("\n" + "=" * 60)
    print("AUDIT COMPLETE")
    print("Do NOT freeze the dataset yet.")
    print("Review this output first; then we will decide exactly what to change.")

if __name__ == "__main__":
    main()
