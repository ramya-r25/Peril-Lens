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