
import pandas as pd

from src.features.feature_engineering import (
    build_feature_dataset
)

from src.analytics.execution_gap_engine import (
    detect_execution_gaps
)

from src.analytics.negative_space_engine import (
    detect_negative_space
)

from src.analytics.peer_benchmarking import (
    build_peer_metrics,
    detect_peer_deviations
)

from src.anomaly_detection.operational_pattern_engine import (
    detect_operational_patterns
)


# ---------------------------------------------------------
# Supervisory Prioritization Engine
# ---------------------------------------------------------

def build_prioritization_queue():
    """
    Combine analytical findings into an assessment-level
    supervisory prioritization queue.

    The score is a transparent prototype and does not represent
    a final compliance or risk judgment.
    """

    # ---------------------------------------------------------
    # 1. Load feature-engineered data
    # ---------------------------------------------------------

    (
        _,
        case_features,
        monitoring
    ) = build_feature_dataset()

    assets = pd.read_csv(
        "data/synthetic/assets.csv"
    )

    # ---------------------------------------------------------
    # 2. Generate analytical findings
    # ---------------------------------------------------------

    # Execution-gap findings
    execution_findings = detect_execution_gaps(
        case_features
    )

    # Negative-space findings
    negative_space_findings = detect_negative_space(
        monitoring,
        assets
    )

    # Peer benchmarking
    peer_metrics = build_peer_metrics(
        case_features,
        execution_findings
    )

    peer_findings = detect_peer_deviations(
        peer_metrics
    )

    # Operational-pattern findings
    operational_findings = detect_operational_patterns(
        case_features
    )

    # ---------------------------------------------------------
    # 3. Create assessment list
    # ---------------------------------------------------------

    assessments = pd.read_csv(
        "data/synthetic/assessments.csv"
    )

    queue = assessments[
        [
            "assessment_id",
            "entity_id"
        ]
    ].drop_duplicates().copy()

    # ---------------------------------------------------------
    # 4. Count evidence by assessment
    # ---------------------------------------------------------

    execution_counts = (
        execution_findings
        .groupby("assessment_id")
        .size()
        .rename(
            "execution_gap_findings"
        )
    )

    negative_space_counts = (
        negative_space_findings
        .groupby("assessment_id")
        .size()
        .rename(
            "negative_space_findings"
        )
    )

    peer_counts = (
        peer_findings
        .groupby("assessment_id")
        .size()
        .rename(
            "peer_deviation_findings"
        )
    )

    operational_counts = (
        operational_findings
        .groupby("assessment_id")
        .size()
        .rename(
            "operational_pattern_findings"
        )
    )

    # ---------------------------------------------------------
    # Merge analytical evidence
    # ---------------------------------------------------------

    queue = queue.merge(
        execution_counts,
        on="assessment_id",
        how="left"
    )

    queue = queue.merge(
        negative_space_counts,
        on="assessment_id",
        how="left"
    )

    queue = queue.merge(
        peer_counts,
        on="assessment_id",
        how="left"
    )

    queue = queue.merge(
        operational_counts,
        on="assessment_id",
        how="left"
    )

    # Missing findings mean no finding was detected.
    queue = queue.fillna(0)

    # ---------------------------------------------------------
    # 5. Calculate transparent priority score
    # ---------------------------------------------------------

    # -----------------------------------------------------
    # Execution-gap score
    #
    # Each finding contributes 1 point.
    # Maximum contribution = 10 points.
    # -----------------------------------------------------

    queue["execution_score"] = (
        queue[
            "execution_gap_findings"
        ]
        .clip(upper=10)
    )

    # -----------------------------------------------------
    # Negative-space score
    #
    # Each negative-space finding contributes 5 points.
    # Maximum contribution = 10 points.
    # -----------------------------------------------------

    queue["negative_space_score"] = (
        queue[
            "negative_space_findings"
        ]
        * 5
    ).clip(upper=10)

    # -----------------------------------------------------
    # Peer-deviation score
    #
    # Each peer deviation contributes 4 points.
    # Maximum contribution = 8 points.
    # -----------------------------------------------------

    queue["peer_deviation_score"] = (
        queue[
            "peer_deviation_findings"
        ]
        * 4
    ).clip(upper=8)

    # -----------------------------------------------------
    # Operational-pattern score
    #
    # Each detected operational pattern contributes
    # 3 points.
    #
    # Maximum contribution = 6 points.
    # -----------------------------------------------------

    queue["operational_pattern_score"] = (
        queue[
            "operational_pattern_findings"
        ]
        * 3
    ).clip(upper=6)

    # -----------------------------------------------------
    # Final prototype priority score
    # -----------------------------------------------------

    queue["priority_score"] = (
        queue["execution_score"]
        + queue["negative_space_score"]
        + queue["peer_deviation_score"]
        + queue["operational_pattern_score"]
    )

    # ---------------------------------------------------------
    # 6. Convert score into review priority
    # ---------------------------------------------------------

    def assign_priority(score):

        if score >= 15:
            return "High"

        elif score >= 7:
            return "Medium"

        return "Low"

    queue["review_priority"] = (
        queue["priority_score"]
        .apply(assign_priority)
    )

    # ---------------------------------------------------------
    # 7. Build human-readable rationale
    # ---------------------------------------------------------

    def build_rationale(row):

        reasons = []

        if row[
            "execution_gap_findings"
        ] > 0:

            reasons.append(
                f"{int(row['execution_gap_findings'])} "
                "execution-gap finding(s)"
            )

        if row[
            "negative_space_findings"
        ] > 0:

            reasons.append(
                f"{int(row['negative_space_findings'])} "
                "negative-space finding(s)"
            )

        if row[
            "peer_deviation_findings"
        ] > 0:

            reasons.append(
                f"{int(row['peer_deviation_findings'])} "
                "peer deviation finding(s)"
            )

        if row[
            "operational_pattern_findings"
        ] > 0:

            reasons.append(
                f"{int(row['operational_pattern_findings'])} "
                "operational-pattern finding(s)"
            )

        if not reasons:

            return (
                "No significant analytical findings detected."
            )

        return "; ".join(
            reasons
        ) + "."

    queue["rationale"] = queue.apply(
        build_rationale,
        axis=1
    )

    # ---------------------------------------------------------
    # 8. Sort highest-priority assessments first
    # ---------------------------------------------------------

    queue = queue.sort_values(
        by=[
            "priority_score",
            "assessment_id"
        ],
        ascending=[
            False,
            True
        ]
    ).reset_index(
        drop=True
    )

    # Create review rank
    queue["review_rank"] = (
        queue.index + 1
    )

    return queue


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print(
        "SAT-SA PRIORITIZATION / REVIEW QUEUE"
    )

    print(
        "=" * 55
    )

    queue = build_prioritization_queue()

    print(
        "\nSupervisory Review Queue:"
    )

    print(
        queue[
            [
                "review_rank",
                "assessment_id",
                "entity_id",
                "execution_gap_findings",
                "negative_space_findings",
                "peer_deviation_findings",
                "operational_pattern_findings",
                "priority_score",
                "review_priority",
                "rationale",
            ]
        ].to_string(
            index=False
        )
    )

    print(
        "\n" + "=" * 55
    )

    print(
        "\nPriority Distribution:"
    )

    print(
        queue[
            "review_priority"
        ].value_counts()
    )

    print(
        "\nHighest-priority assessment:"
    )

    top = queue.iloc[0]

    print(
        f"\n{top['assessment_id']} "
        f"({top['review_priority']} Priority)"
    )

    print(
        f"Score: {top['priority_score']}"
    )

    print(
        f"Reason: {top['rationale']}"
    )

    print(
        "\nNOTE:"
        "\nThe priority score is a transparent prototype "
        "for supervisory review prioritization."
        "\nIt does not represent a final compliance judgment."
    )


if __name__ == "__main__":
    main()

