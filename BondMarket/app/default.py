import os

doc_path = os.path.expanduser('~\\Documents')

SETTINGS = {
    "app_settings":
        {"appearance": "dark",
         "file_path": f"{doc_path}\\BondMarket 5.0\\Data\\data.pkl",
         "currency": "\u20ac"
         },
    "table_settings":
        {"sort_argument": "Amount up",
         "table_index": 0,
         "month": "05",
         "year": "2022",
         "key": ""
         },
    "debts_settings":
        {}
}
