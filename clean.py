# Cleaning final master dataset
import pandas as pd

df = pd.read_csv("mumbai_real_estate_dataset.csv")

# POSSESION
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

df["possesion_by"] = df["possesion_by"].apply(map_possession)



# TYPE
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


def map_type(val):
    if val in residential:
        return 1
    elif val in commercial:
        return 2
    elif val in industrial:
        return 3
    else:
        return 0

df["type"] = df["type"].apply(map_type)



# FURNISHED
furnished_mapping = {"Unfurnished": 0, "Semi-Furnished": 0.5, "Furnished": 1}

df['furnished'] = df['furnished'].map(furnished_mapping).fillna(0)



# TRANSACTION
df["transaction"] = (
    df["transaction"].replace({"Rent": "Resale", "Other": "Resale"}).fillna("Resale")

)

df['transaction'] = df["transaction"].map({"Resale": 0, "New Property": 1})



# PRICE
lower_limit = 1300000
upper_limit = 200000000

df = df[(df['price'] >= lower_limit) & (df['price'] <= upper_limit)].copy()


# BEDROOM & BATHROOM
df['bedrooms'] = pd.to_numeric(df['bedrooms'], errors='coerce')
df['bathrooms'] = pd.to_numeric(df['bathrooms'], errors='coerce')

df['area_bucket'] = pd.cut(df['area'], bins=[0, 500, 1000, 2000, 50000], labels=[0, 1, 2, 3])
bedroom_medians = df.groupby(['area_bucket', 'type'])['bedrooms'].transform('median')
bathroom_medians = df.groupby(['area_bucket', 'type'])['bathrooms'].transform('median')


df['bedrooms'] = df['bedrooms'].fillna(bedroom_medians)
df['bathrooms'] = df['bathrooms'].fillna(bathroom_medians)

df['bedrooms'] = df['bedrooms'].fillna(df['bedrooms'].median())
df['bathrooms'] = df['bathrooms'].fillna(df['bathrooms'].median())
df = df.drop(columns="area_bucket")



# PARKING
df = df.drop(columns='parking',)


# LAT & LONG
df = df.dropna(subset=['lat', 'long'])


# ENCODING CITY, LOCALITY, PROJECT NAME, DEVELOPER
cols_to_encode = ['project_name', 'locality', 'city', 'developers']

for col in cols_to_encode:
    target_mapping = df.groupby(col)['price'].mean()
    df[f'{col}_encoded'] = df[col].map(target_mapping)


# MISSING AREA
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

imputer = IterativeImputer(random_state=42)

numeric_cols = df.select_dtypes(include=['number']).columns

df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

df.to_csv("mumbai_real_estate_cleaned.csv", index=False)

print(df.info())
print(df.isnull().sum())
print(len(df))