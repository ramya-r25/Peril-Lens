import pandas as pd

from src.features.feature_engineering import build_feature_dataset


def detect_negative_space(monitoring, assets):
    """
    Detect potential negative-space conditions in SOC monitoring data.

    The engine does not declare a compliance failure.
    It identifies evidence that may require supervisory review.
    """

    monitoring = monitoring.copy()
    assets = assets.copy()

    # Merge monitoring data with asset information
    merged = monitoring.merge(
        assets[
            [
                "asset_id",
                "asset_name",
                "criticality",
                "expected_monitoring",
            ]
        ],
        on="asset_id",
        how="left",
    )

    # Calculate monitoring coverage
    merged["coverage_ratio"] = (
        merged["observed_coverage_hours"]
        / merged["expected_coverage_hours"]
    )

    # Prevent invalid values
    merged["coverage_ratio"] = merged["coverage_ratio"].clip(lower=0)

    merged["coverage_percent"] = (
        merged["coverage_ratio"] * 100
    ).round(2)

    findings = []

    # ---------------------------------------------------------
    # Signal 1: Low monitoring coverage
    # ---------------------------------------------------------

    low_coverage = merged[
        (merged["criticality"] == "Critical")
        & (merged["expected_monitoring"] == True)
        & (merged["coverage_ratio"] < 0.50)
    ]

    for _, row in low_coverage.iterrows():

        findings.append(
            {
                "assessment_id": row["assessment_id"],
                "asset_id": row["asset_id"],
                "asset_name": row["asset_name"],
                "criticality": row["criticality"],
                "signal_type": "Low Monitoring Coverage",
                "expected_coverage_hours": row[
                    "expected_coverage_hours"
                ],
                "observed_coverage_hours": row[
                    "observed_coverage_hours"
                ],
                "coverage_percent": row["coverage_percent"],
                "telemetry_available": row[
                    "telemetry_available"
                ],
                "reason": (
                    f"Critical asset has only "
                    f"{row['coverage_percent']:.1f}% "
                    f"observed monitoring coverage against "
                    f"expected monitoring."
                ),
                "recommended_action": (
                    "Review whether the observed monitoring "
                    "coverage is adequate and investigate "
                    "potential monitoring blind spots."
                ),
            }
        )

    # ---------------------------------------------------------
    # Signal 2: Telemetry unavailable
    # ---------------------------------------------------------

    telemetry_unavailable = merged[
        (merged["criticality"] == "Critical")
        & (merged["expected_monitoring"] == True)
        & (merged["telemetry_available"] == False)
    ]

    for _, row in telemetry_unavailable.iterrows():

        findings.append(
            {
                "assessment_id": row["assessment_id"],
                "asset_id": row["asset_id"],
                "asset_name": row["asset_name"],
                "criticality": row["criticality"],
                "signal_type": "Telemetry Unavailable",
                "expected_coverage_hours": row[
                    "expected_coverage_hours"
                ],
                "observed_coverage_hours": row[
                    "observed_coverage_hours"
                ],
                "coverage_percent": row["coverage_percent"],
                "telemetry_available": row[
                    "telemetry_available"
                ],
                "reason": (
                    "Monitoring is expected for this critical "
                    "asset, but telemetry availability is "
                    "reported as unavailable."
                ),
                "recommended_action": (
                    "Review telemetry availability and determine "
                    "whether the absence represents a potential "
                    "monitoring blind spot."
                ),
            }
        )

    return pd.DataFrame(findings)


def main():

    print("SAT-SA NEGATIVE SPACE DETECTION")
    print("=" * 50)

    # Load existing feature pipeline data
    _, _, monitoring = build_feature_dataset()

    # Load asset information
    assets = pd.read_csv("data/synthetic/assets.csv")

    # Detect negative-space conditions
    findings = detect_negative_space(
        monitoring,
        assets
    )

    print("\nTotal negative-space findings:", len(findings))

    if findings.empty:
        print("\nNo potential negative-space conditions detected.")
        return

    print("\nSignal distribution:")
    print(
        findings["signal_type"]
        .value_counts()
    )

    print("\nFindings by assessment:")
    print(
        findings.groupby("assessment_id")
        .size()
        .sort_values(ascending=False)
    )

    print("\nSample findings:")
    print(
        findings[
            [
                "assessment_id",
                "asset_id",
                "asset_name",
                "signal_type",
                "coverage_percent",
                "telemetry_available",
                "reason",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()