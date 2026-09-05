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