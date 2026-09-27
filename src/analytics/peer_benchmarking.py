import pandas as pd

from src.features.feature_engineering import build_feature_dataset
from src.analytics.execution_gap_engine import detect_execution_gaps


def build_peer_metrics(case_features, execution_findings):
    """
    Build assessment-level operational metrics that can be
    compared across peer assessments.
    """

    # Total cases per assessment
    total_cases = (
        case_features
        .groupby("assessment_id")
        .size()
        .rename("total_cases")
    )

    # High/Critical cases
    high_critical_cases = (
        case_features
        .groupby("assessment_id")["is_high_critical"]
        .sum()
        .rename("high_critical_cases")
    )

    # Weak investigations
    weak_investigations = (
        case_features
        .groupby("assessment_id")["weak_investigation"]
        .sum()
        .rename("weak_investigations")
    )

    # Execution-gap findings
    execution_gap_findings = (
        execution_findings
        .groupby("assessment_id")
        .size()
        .rename("execution_gap_findings")
    )

    # Combine metrics
    metrics = pd.concat(
        [
            total_cases,
            high_critical_cases,
            weak_investigations,
            execution_gap_findings,
        ],
        axis=1
    ).fillna(0)

    # Calculate rates
    metrics["weak_investigation_rate"] = (
        metrics["weak_investigations"]
        / metrics["total_cases"]
    )

    metrics["execution_gap_rate"] = (
        metrics["execution_gap_findings"]
        / metrics["total_cases"]
    )

    return metrics.reset_index()


def detect_peer_deviations(metrics):
    """
    Detect assessments that deviate significantly from
    the peer-group average.

    A finding means 'requires review', not 'compliance failure'.
    """

    metrics = metrics.copy()

    findings = []

    # Metrics to benchmark
    benchmark_columns = [
        (
            "weak_investigation_rate",
            "Weak Investigation Rate"
        ),
        (
            "execution_gap_rate",
            "Execution Gap Rate"
        ),
    ]

    for metric_column, metric_name in benchmark_columns:

        peer_mean = metrics[metric_column].mean()
        peer_std = metrics[metric_column].std()

        # If there is no variation between peers,
        # there is no meaningful deviation to detect.
        if pd.isna(peer_std) or peer_std == 0:
            continue

        # Use 2 standard deviations as the first
        # transparent deviation threshold.
        threshold = peer_mean + (2 * peer_std)

        deviating = metrics[
            metrics[metric_column] > threshold
        ]

        for _, row in deviating.iterrows():

            deviation_ratio = (
                row[metric_column] / peer_mean
                if peer_mean > 0
                else None
            )

            findings.append(
                {
                    "assessment_id": row["assessment_id"],
                    "metric": metric_name,
                    "metric_value": round(
                        row[metric_column] * 100,
                        2
                    ),
                    "peer_average": round(
                        peer_mean * 100,
                        2
                    ),
                    "peer_std": round(
                        peer_std * 100,
                        2
                    ),
                    "deviation_threshold": round(
                        threshold * 100,
                        2
                    ),
                    "deviation_ratio": (
                        round(deviation_ratio, 2)
                        if deviation_ratio is not None
                        else None
                    ),
                    "reason": (
                        f"{metric_name} is "
                        f"{row[metric_column] * 100:.1f}% "
                        f"compared with a peer average of "
                        f"{peer_mean * 100:.1f}%."
                    ),
                    "recommended_action": (
                        "Review the assessment against "
                        "comparable entities to determine "
                        "whether the deviation indicates "
                        "a potential operational weakness."
                    ),
                }
            )

    return pd.DataFrame(findings)


def main():

    print("SAT-SA PEER BENCHMARKING")
    print("=" * 50)

    # Load feature-engineered data
    _, case_features, _ = build_feature_dataset()

    # Detect execution-gap findings
    execution_findings = detect_execution_gaps(
        case_features
    )

    # Build assessment-level metrics
    metrics = build_peer_metrics(
        case_features,
        execution_findings
    )

    print("\nAssessment Metrics:")
    print(
        metrics[
            [
                "assessment_id",
                "total_cases",
                "high_critical_cases",
                "weak_investigations",
                "execution_gap_findings",
                "weak_investigation_rate",
                "execution_gap_rate",
            ]
        ].to_string(index=False)
    )

    # Detect peer deviations
    findings = detect_peer_deviations(metrics)

    print("\n" + "=" * 50)
    print("PEER DEVIATIONS")
    print("=" * 50)

    print(
        "\nTotal peer deviation findings:",
        len(findings)
    )

    if findings.empty:
        print(
            "\nNo significant peer deviations detected."
        )
        return

    print("\nFindings:")

    print(
        findings[
            [
                "assessment_id",
                "metric",
                "metric_value",
                "peer_average",
                "deviation_threshold",
                "reason",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()