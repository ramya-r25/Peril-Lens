import pandas as pd

from src.features.feature_engineering import (
    build_feature_dataset
)


# ---------------------------------------------------------
# Operational Pattern Engine
# ---------------------------------------------------------

def detect_operational_patterns(case_features):

    findings = []

    # -----------------------------------------------------
    # Pattern 1:
    # Repetitive weak investigation pattern
    # -----------------------------------------------------

    weak_cases = case_features[
        case_features["weak_investigation"] == True
    ].copy()

    if not weak_cases.empty:

        grouped = (
            weak_cases
            .groupby("assessment_id")
            .agg(
                weak_investigation_count=(
                    "case_id",
                    "count"
                ),
                avg_evidence_count=(
                    "evidence_count",
                    "mean"
                ),
                avg_steps_recorded=(
                    "steps_recorded",
                    "mean"
                )
            )
            .reset_index()
        )

        for _, row in grouped.iterrows():

            if row["weak_investigation_count"] >= 5:

                findings.append({
                    "assessment_id":
                        row["assessment_id"],

                    "signal_type":
                        "Repetitive Weak Investigation Pattern",

                    "affected_cases":
                        int(row["weak_investigation_count"]),

                    "metric_value":
                        round(
                            row["weak_investigation_count"],
                            2
                        ),

                    "reason":
                        (
                            f"{int(row['weak_investigation_count'])} "
                            "investigations show a similar weak "
                            "evidence pattern."
                        ),

                    "recommended_action":
                        (
                            "Review representative investigation "
                            "records for repeated investigation "
                            "shortcomings."
                        )
                })


    # -----------------------------------------------------
    # Pattern 2:
    # Possible metric-driven rapid closure
    # -----------------------------------------------------

    rapid_high_critical = case_features[
        (
            case_features["is_high_critical"]
        )
        &
        (
            case_features["is_closed"]
        )
        &
        (
            case_features["closure_hours"] <= 8
        )
    ].copy()

    if not rapid_high_critical.empty:

        grouped = (
            rapid_high_critical
            .groupby("assessment_id")
            .agg(
                rapid_closure_count=(
                    "case_id",
                    "count"
                ),
                avg_closure_hours=(
                    "closure_hours",
                    "mean"
                ),
                weak_investigation_count=(
                    "weak_investigation",
                    "sum"
                )
            )
            .reset_index()
        )

        for _, row in grouped.iterrows():

            rapid_count = int(
                row["rapid_closure_count"]
            )

            weak_count = int(
                row["weak_investigation_count"]
            )

            # Require both repeated rapid closure
            # and some weak-investigation evidence.
            if (
                rapid_count >= 5
                and weak_count >= 3
            ):

                findings.append({
                    "assessment_id":
                        row["assessment_id"],

                    "signal_type":
                        "Possible Metric-Driven Rapid Closure",

                    "affected_cases":
                        rapid_count,

                    "metric_value":
                        round(
                            row["avg_closure_hours"],
                            2
                        ),

                    "reason":
                        (
                            f"{rapid_count} High/Critical cases "
                            f"were closed within 8 hours, with "
                            f"{weak_count} also showing weak "
                            "investigation evidence."
                        ),

                    "recommended_action":
                        (
                            "Review closure patterns and "
                            "investigation evidence to determine "
                            "whether closure speed may be "
                            "influencing investigation quality."
                        )
                })


    # -----------------------------------------------------
    # Pattern 3:
    # Unusually low investigation effort
    # -----------------------------------------------------

    investigated = case_features[
        case_features["investigation_duration_minutes"].notna()
    ].copy()

    if not investigated.empty:

        grouped = (
            investigated
            .groupby("assessment_id")
            .agg(
                avg_investigation_duration=(
                    "investigation_duration_minutes",
                    "mean"
                ),
                avg_evidence_score=(
                    "investigation_evidence_score",
                    "mean"
                ),
                investigation_count=(
                    "case_id",
                    "count"
                )
            )
            .reset_index()
        )

        overall_avg_duration = (
            investigated[
                "investigation_duration_minutes"
            ].mean()
        )

        for _, row in grouped.iterrows():

            # Require a reasonable sample size.
            if row["investigation_count"] < 5:
                continue

            # Flag assessments whose average investigation
            # duration is substantially below the overall
            # dataset average.
            if (
                row["avg_investigation_duration"]
                < overall_avg_duration * 0.50
            ):

                findings.append({
                    "assessment_id":
                        row["assessment_id"],

                    "signal_type":
                        "Low Investigation Effort Outlier",

                    "affected_cases":
                        int(row["investigation_count"]),

                    "metric_value":
                        round(
                            row["avg_investigation_duration"],
                            2
                        ),

                    "reason":
                        (
                            f"Average investigation duration was "
                            f"{row['avg_investigation_duration']:.1f} "
                            "minutes, substantially below the "
                            f"overall average of "
                            f"{overall_avg_duration:.1f} minutes."
                        ),

                    "recommended_action":
                        (
                            "Review representative investigations "
                            "to determine whether unusually low "
                            "investigation effort is supported by "
                            "adequate evidence."
                        )
                })


    return pd.DataFrame(findings)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    (
        alerts,
        case_features,
        monitoring
    ) = build_feature_dataset()

    findings = detect_operational_patterns(
        case_features
    )

    print("\n==========================================")
    print("SAT-SA OPERATIONAL PATTERN ENGINE")
    print("==========================================")

    print(
        "\nTotal operational-pattern findings:",
        len(findings)
    )

    if not findings.empty:

        print("\nSignal distribution:")

        print(
            findings[
                "signal_type"
            ].value_counts()
        )

        print("\nFindings:")

        print(
            findings.to_string(
                index=False
            )
        )

    else:

        print(
            "\nNo operational patterns detected."
        )