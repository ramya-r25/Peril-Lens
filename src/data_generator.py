import pandas as pd


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