import pandas as pd


# ---------------------------------------------------------
# Load synthetic datasets
# ---------------------------------------------------------

def load_data():
    alerts = pd.read_csv(
        "data/synthetic/alerts.csv"
    )

    cases = pd.read_csv(
        "data/synthetic/cases.csv"
    )

    investigations = pd.read_csv(
        "data/synthetic/investigations.csv"
    )

    escalations = pd.read_csv(
        "data/synthetic/escalations.csv"
    )

    monitoring = pd.read_csv(
        "data/synthetic/monitoring.csv"
    )

    return (
        alerts,
        cases,
        investigations,
        escalations,
        monitoring
    )


# ---------------------------------------------------------
# Case-level features
# ---------------------------------------------------------

def create_case_features(cases):
    cases = cases.copy()

    # Convert timestamps
    cases["case_created_time"] = pd.to_datetime(
        cases["case_created_time"]
    )

    cases["closure_time"] = pd.to_datetime(
        cases["closure_time"]
    )

    # Calculate closure time in hours
    cases["closure_hours"] = (
        (
            cases["closure_time"]
            - cases["case_created_time"]
        )
        .dt.total_seconds()
        / 3600
    )

    # High/Critical indicator
    cases["is_high_critical"] = (
        cases["priority"].isin(
            ["High", "Critical"]
        )
    )

    # Closed indicator
    cases["is_closed"] = (
        cases["status"] == "Closed"
    )

    return cases


# ---------------------------------------------------------
# Investigation-level features
# ---------------------------------------------------------

def create_investigation_features(investigations):
    investigations = investigations.copy()

    investigations["start_time"] = pd.to_datetime(
        investigations["start_time"]
    )

    investigations["end_time"] = pd.to_datetime(
        investigations["end_time"]
    )

    # Investigation duration
    investigations["investigation_duration_minutes"] = (
        (
            investigations["end_time"]
            - investigations["start_time"]
        )
        .dt.total_seconds()
        / 60
    )

    # Investigation evidence score
    investigations["investigation_evidence_score"] = (
        investigations["evidence_count"]
        + investigations["steps_recorded"]
    )

    # Weak investigation indicator
    investigations["weak_investigation"] = (
        (investigations["evidence_count"] <= 3)
        &
        (investigations["steps_recorded"] <= 3)
        &
        (~investigations["root_cause_identified"])
        &
        (~investigations["remediation_recorded"])
    )

    return investigations


# ---------------------------------------------------------
# Case + Investigation features
# ---------------------------------------------------------

def combine_case_investigation_features(
    cases,
    investigations
):

    merged = cases.merge(
        investigations,
        on="case_id",
        how="left",
        suffixes=("", "_investigation")
    )

    return merged


# ---------------------------------------------------------
# Escalation features
# ---------------------------------------------------------

def create_escalation_features(
    cases,
    escalations
):

    escalation_counts = (
        escalations
        .groupby("case_id")
        .size()
        .reset_index(
            name="escalation_count"
        )
    )

    cases = cases.merge(
        escalation_counts,
        on="case_id",
        how="left"
    )

    cases["escalation_count"] = (
        cases["escalation_count"]
        .fillna(0)
    )

    cases["was_escalated"] = (
        cases["escalation_count"] > 0
    )

    return cases


# ---------------------------------------------------------
# Main feature pipeline
# ---------------------------------------------------------

def build_feature_dataset():

    (
        alerts,
        cases,
        investigations,
        escalations,
        monitoring
    ) = load_data()

    # Case features
    cases = create_case_features(
        cases
    )

    # Investigation features
    investigations = create_investigation_features(
        investigations
    )

    # Combine case + investigation data
    case_features = combine_case_investigation_features(
        cases,
        investigations
    )

    # Add escalation features
    case_features = create_escalation_features(
        case_features,
        escalations
    )

    return (
        alerts,
        case_features,
        monitoring
    )


# ---------------------------------------------------------
# Run pipeline
# ---------------------------------------------------------

if __name__ == "__main__":

    (
        alerts,
        case_features,
        monitoring
    ) = build_feature_dataset()

    print("\n==========================================")
    print("SAT-SA FEATURE ENGINEERING")
    print("==========================================")

    print("\nCase Features:")
    print(
        case_features.head()
    )

    print(
        "\nTotal case-feature records:",
        len(case_features)
    )

    print(
        "\nWeak investigations:",
        case_features[
            "weak_investigation"
        ].sum()
    )

    print(
        "\nHigh/Critical cases:",
        case_features[
            "is_high_critical"
        ].sum()
    )

    print(
        "\nEscalated cases:",
        case_features[
            "was_escalated"
        ].sum()
    )