# Cleaning final master dataset
import pandas as pd

df = pd.read_csv("mumbai_real_estate_dataset.csv")


def map_possession(val):
    if not isinstance(val, str):
        return 0  # Handle NaNs/non-strings as 0 (Everything else)

    val_lower = val.lower().strip()
    if "ready" in val_lower or "immediately" in val_lower:
        return 1
    elif "under construction" in val_lower:
        return 0.5
    else:
        return 0


residential = [
    "Apartment",
    "Builder Floor Apartment",
    "Residential Plot",
    "Residential House",
    "Studio Apartment",
    "Villa",
    "Penthouse",
    "Farm House",
]
commercial = [
    "Commercial Shop",
    "Commercial Office Space",
    "Commercial Showroom",
    "Office in IT Park/ SEZ",
    "Warehouse/ Godown",
    "Commercial Land",
]
industrial = [
    "Industrial Building",
    "Industrial Shed",
    "Industrial Land",
    "Agricultural Land",
]


# Function to map type
def map_type(val):
    if val in residential:
        return 1
    elif val in commercial:
        return 2
    elif val in industrial:
        return 3
    else:
        return 0


furnished_mapping = {"Unfurnished": 0, "Semi-Furnished": 0.5, "Furnished": 1}


df["transaction"] = (
    df["transaction"].replace({"Rent": "Resale", "Other": "Resale"}).fillna("Resale")
)

df["possesion_by"] = df["possesion_by"].apply(map_possession)


df["type"] = df["type"].apply(map_type)


# print(df['type'].unique())
print(df.isnull().sum())
