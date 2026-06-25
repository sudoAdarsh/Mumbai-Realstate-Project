import json
import pandas as pd
import glob
import os

# Configuration
FOLDER_PATH = "navi_mumbai_scraped_data" # Change this for other cities
OUTPUT_FILE = "final_dataset_navi_mumbai.csv"

def get_fields(item):
    """Your existing logic wrapped in a function"""
    return {
        "project_name": item.get("prjname", "Unkown"),
        "price": item.get("price"),
        "area": item.get("carpetArea", None),
        "bedrooms": item.get("bedroomD"),
        "bathrooms": item.get("bathD"),
        "locality": item.get("lmtDName"),
        "city": item.get("ctName"),
        "lat": float(item.get("ltcoordGeo").split(',')[0]) if item.get("ltcoordGeo") else None,
        "long": float(item.get("ltcoordGeo").split(',')[1]) if item.get("ltcoordGeo") else None,
        "furnished": item.get("furnishedD"),
        "type": item.get("propTypeD"),
        "rera": 1 if item.get("isRera") == "Y" else 0,
        "amenities": len(item.get("psmAmenDesc", [])),
        "landmarks": len(item.get("landmarkDetails", [])),
        "transaction": item.get("transactionTypeD"),
        "possesion_by": item.get("possStatusD"),
        "parking": item.get("parkingD", None),
        "developers": item.get("devName", "Unknown"),
    }

# 1. Get all json files in the folder
file_list = glob.glob(os.path.join(FOLDER_PATH, "*.json"))

extracted_data = []

# 2. Loop through every file found
for file_path in file_list:
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            # Ensure we are looking at the correct key
            result_list = data.get("resultList", [])
            
            # Loop through all items in the list (not just 30)
            for item in result_list:
                extracted_data.append(get_fields(item))
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

# 3. Create Master DataFrame
df = pd.DataFrame(extracted_data)

# 4. Save to CSV
df.to_csv(OUTPUT_FILE, index=False)

# 5. Summary
print(f"Successfully processed {len(df)} properties.")
print(df.info())
