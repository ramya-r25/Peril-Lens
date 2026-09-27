import pandas as pd

from src.features.feature_engineering import (
    build_feature_dataset
)

from src.analytics.execution_gap_engine import (
    detect_execution_gaps
)


# ---------------------------------------------------------
# Build assessment-level supervisory indicators
# ---------------------------------------------------------

def build_supervisory_indicators(findings):

    if findings.empty:
        return pd.DataFrame()

    # -----------------------------------------------------
    # Basic aggregation
    # -----------------------------------------------------

    summary = (
        findings
        .groupby("assessment_id")
        .agg(
            total_findings=(
                "case_id",
                "count"
            ),

            unique_affected_cases=(
                "case_id",
                "nunique"
            )
        )
        .reset_index()
    )

    # -----------------------------------------------------
    # Count individual signal types
    # -----------------------------------------------------

    signal_counts = (
        findings
        .pivot_table(
            index="assessment_id",
            columns="signal_type",
            values="case_id",
            aggfunc="count",
            fill_value=0
        )
        .reset_index()
    )

    # Make sure expected columns exist
    expected_signals = [
        "Weak Investigation",
        "Rapid Closure + Weak Investigation",
        "Critical Case Closed Without Escalation"
    ]

    for signal in expected_signals:

        if signal not in signal_counts.columns:
            signal_counts[signal] = 0

    signal_counts = signal_counts.rename(
        columns={
            "Weak Investigation":
                "weak_investigation_findings",

            "Rapid Closure + Weak Investigation":
                "rapid_closure_findings",

            "Critical Case Closed Without Escalation":
                "critical_no_escalation_findings"
        }
    )

    # -----------------------------------------------------
    # Merge signal counts
    # -----------------------------------------------------

    summary = summary.merge(
        signal_counts[
            [
                "assessment_id",
                "weak_investigation_findings",
                "rapid_closure_findings",
                "critical_no_escalation_findings"
            ]
        ],
        on="assessment_id",
        how="left"
    )

    # -----------------------------------------------------
    # Supervisory attention level
    # -----------------------------------------------------

    def classify_attention(row):

        score = 0

        # Weak investigations
        score += min(
            row["weak_investigation_findings"],
            5
        )

        # Rapid closure + weak investigation
        score += (
            row["rapid_closure_findings"] * 2
        )

        # Critical cases without escalation
        score += (
            row["critical_no_escalation_findings"] * 2
        )

        if score >= 15:
            return "High"

        elif score >= 7:
            return "Medium"

        return "Low"

    summary["attention_level"] = (
        summary.apply(
            classify_attention,
            axis=1
        )
    )

    # -----------------------------------------------------
    # Generate human-readable rationale
    # -----------------------------------------------------

    def generate_rationale(row):

        reasons = []

        if row["weak_investigation_findings"] > 0:

            reasons.append(
                f"{int(row['weak_investigation_findings'])} "
                "weak investigation signal(s)"
            )

        if row["rapid_closure_findings"] > 0:

            reasons.append(
                f"{int(row['rapid_closure_findings'])} "
                "rapid closure signal(s)"
            )

        if row["critical_no_escalation_findings"] > 0:

            reasons.append(
                f"{int(row['critical_no_escalation_findings'])} "
                "critical case(s) closed without escalation"
            )

        return "; ".join(reasons)

    summary["rationale"] = (
        summary.apply(
            generate_rationale,
            axis=1
        )
    )

    return summary


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    (
        alerts,
        case_features,
        monitoring
    ) = build_feature_dataset()

    findings = detect_execution_gaps(
        case_features
    )

    supervisory_summary = (
        build_supervisory_indicators(
            findings
        )
    )

    print("\n==========================================")
    print("SAT-SA SUPERVISORY INDICATORS")
    print("==========================================")

    print("\nAssessment-level summary:")

    print(
        supervisory_summary.to_string(
            index=False
        )
    )

    print("\nAttention distribution:")

    print(
        supervisory_summary[
            "attention_level"
        ].value_counts()
    )