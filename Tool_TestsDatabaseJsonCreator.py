import json
LAB_DATABASE = {
    "urea": {
        "aliases": ["u", "urea", "uera", "b.u", "b.urea", "b.uera"],
        "display": "b.Urea",
        "high": 45,
        "low": 15,
        "unit": "mg/dl",
    },
    "creatinine": {
        "aliases": ["cr", "creatinine", "crea", "creat","s.cr", "s.creatinine", "s.crea", "s.creat"],
        "display": "Creatinine",
        "high": 1.3,
        "low": 0.7,
        "unit": "mg/dl",
    },
    "sodium": {
        "aliases": ["na", "sodium","s.na", "s.sodium"],
        "display": "Sodium",
        "high": 145,
        "low": 135,
        "unit": "mmol/l",
    },
    "potassium": {
        "aliases": ["k", "potassium", "serum_k"],
        "display": "Potassium",
        "high": 5.0,
        "low": 3.5,
        "unit": "mmol/l",
    },
    "hba1c": {
        "aliases": ["a1c", "hba1c", "hb_a1c"],
        "display": "HbA1c",
        "high": 6.5,
        "low": 4.0,
        "unit": "%",
    },
}

with open("InvestigationDatabase.json","w") as f:
    json.dump(LAB_DATABASE,f,indent=4)
