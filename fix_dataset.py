import json
import csv
import difflib

# Load the "fake"/estimated JSON data
def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load CSV databases
def load_csv(filepath, name_col):
    data = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data[row[name_col].lower()] = row
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin1') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data[row[name_col].lower()] = row
    return data

def main():
    print("Loading datasets...")
    json_data = load_json('realistic_nutrition_dataset.json')
    indian_data = load_csv('Indian_Food_Nutrition_Processed.csv', 'Dish Name')
    usda_data = load_csv('USDA.csv', 'Description')
    
    verified_dataset = {}
    
    # All possible food names in the databases
    indian_names = list(indian_data.keys())
    usda_names = list(usda_data.keys())
    
    print("Finding real matches...")
    for json_key, json_val in json_data.items():
        # Clean up the JSON key for searching (e.g., 'ash_gourd_curry' -> 'ash gourd')
        search_term = json_key.replace('_', ' ')
        
        # 1. Try to find a match in the Indian Food database first (closest context)
        indian_match = difflib.get_close_matches(search_term, indian_names, n=1, cutoff=0.4)
        
        # 2. If not found, try the USDA database
        usda_match = difflib.get_close_matches(search_term, usda_names, n=1, cutoff=0.5)
        
        # 3. Update with real values if a match is found
        if indian_match:
            real_row = indian_data[indian_match[0]]
            verified_dataset[json_key] = {
                "method": "verified_real_data",
                "sources": [f"Indian_Food_Nutrition_Processed.csv - '{real_row['Dish Name']}'"],
                "nutrition": {
                    "energy_kcal": float(real_row.get('Calories (kcal)', 0) or 0),
                    "carbohydrate_g": float(real_row.get('Carbohydrates (g)', 0) or 0),
                    "protein_g": float(real_row.get('Protein (g)', 0) or 0),
                    "fat_g": float(real_row.get('Fats (g)', 0) or 0),
                    "sodium_mg": float(real_row.get('Sodium (mg)', 0) or 0)
                }
            }
        elif usda_match:
            real_row = usda_data[usda_match[0]]
            verified_dataset[json_key] = {
                "method": "verified_real_data",
                "sources": [f"USDA.csv - '{real_row['Description']}'"],
                "nutrition": {
                    "energy_kcal": float(real_row.get('Calories', 0) or 0),
                    "carbohydrate_g": float(real_row.get('Carbohydrate', 0) or 0),
                    "protein_g": float(real_row.get('Protein', 0) or 0),
                    "fat_g": float(real_row.get('TotalFat', 0) or 0),
                    "sodium_mg": float(real_row.get('Sodium', 0) or 0)
                }
            }
        else:
             # Keep the old one if no match is found, but flag it as unverified
             verified_dataset[json_key] = json_val
             verified_dataset[json_key]["method"] = "unverified_estimated_fallback"
             
    with open('verified_nutrition_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(verified_dataset, f, indent=4)
        
    print("Done! Real data saved to 'verified_nutrition_dataset.json'.")

if __name__ == "__main__":
    main()
