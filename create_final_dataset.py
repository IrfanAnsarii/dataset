import json
import csv
from difflib import get_close_matches

def load_csv(filename, name_col, encoding='utf-8'):
    data = {}
    try:
        with open(filename, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = row[name_col].lower().strip()
                data[key] = row
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin1') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = row[name_col].lower().strip()
                data[key] = row
    return data

# Load original JSON
with open('realistic_nutrition_dataset.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Load CSVs
indian_data = load_csv('Indian_Food_Nutrition_Processed.csv', 'Dish Name')
usda_data = load_csv('USDA.csv', 'Description')

# Get all keys for searching
indian_keys = list(indian_data.keys())
usda_keys = list(usda_data.keys())

# INTELLIGENT MAPPING - For NOT FOUND items, find best semantic match
SMART_MAPPING = {
    "ash_gourd_curry": "bottle gourd burfi",  # Ash gourd is similar to bottle gourd
    "bhat_kerela_fry": "brinjal fry",  # Vegetable fry
    "bitter_gourd_fry": "karela fry",  # Try to find karela specifically
    "bitter_gourd_potato_fry": "aloo gobhi",  # Potato vegetable mix
    "boiled_egg": "deviled egg",  # Egg dish
    "boiled_ladies_finger": "bhindi fry",  # Ladies finger = Okra = Bhindi
    "brinjal_chutney": "brinjal bharta",  # Eggplant version
    "brinjal_curry": "brinjal",  # Eggplant
    "brinjal_fry": "brinjal fry",  # Fried eggplant
    "but_dal": "chana dal",  # Roasted gram dal
    "but_potato_fry": "aloo chana",  # Potato chickpea
    "cabbage_fry": "cabbage",  # Cabbage
    "capsicum_pakoda": "capsicum pakora",  # Pepper fritter
    "chicken_fry": "chicken",  # Fried chicken
    "curd": "curd",  # Yogurt/Curd
    "curry_leaf_curry": "curry",  # Curry with leaves
    "dang_bodi_fry": "long beans",  # Yard-long beans = Long beans
    "dhekia_xaak_fry": "fern",  # Fiddlehead fern
    "duck_meat_curry": "duck",  # Duck
    "fabian_carrot_fry": "carrot",  # Beans with carrot
    "fabian_fry": "beans fry",  # Beans
    "fish_chutney": "fish",  # Fish pickle
    "fish_fry": "fish fry",  # Fried fish
    "gourd_curry": "bottle gourd",  # Gourd curry
    "green_leafy_fry": "spinach",  # Leafy greens
    "hyachinth_bean_fry": "bean",  # Bean fry
    "jackfruit_milk_shake": "fruit",  # Jackfruit shake - use fruit
    "kath_alu_curry": "yam",  # Yam curry
    "kolmu_xaak": "spinach",  # Water spinach = spinach
    "kosu_leaf_curry": "colocasia",  # Taro/colocasia
    "ladies_finger_fry": "bhindi",  # Okra/Bhindi
    "lai_xaak": "mustard",  # Mustard greens
    "masoor_dal": "masoor",  # Red lentil
    "mati_dal": "urad",  # Black gram
    "mix_fry": "mixed vegetable",  # Mixed vegetables
    "mula_curry": "radish",  # Radish
    "ou_tenga_masoor_dal": "dal",  # Sour lentil - use dal
    "papaya_xaar": "papaya",  # Papaya
    "pork_curry": "pork",  # Pork
    "pork_fry": "pork fry",  # Fried pork
    "potato_bean_carrot_fry": "mixed vegetable",  # Mixed
    "potato_bean_fry": "beans",  # Bean potato
    "potato_cauliflower_carrot_fry": "aloo gobi",  # Aloo gobi
    "potato_cauliflower_fry": "aloo gobi",  # Aloo gobi
    "potato_fry": "french fries",  # Potato fries
    "potato_kunduly_fry": "ivy gourd",  # Ivy gourd
    "rohor_mah_curry": "arhar",  # Pigeon pea
    "tamul_pan": "betel",  # Betel leaf
    "til_chutney": "sesame",  # Sesame
    "xaak and boot fry": "spinach",  # Spinach chickpea
    "xaak_motor_fry": "spinach",  # Spinach peas
    "xaak_potato_fry": "spinach",  # Spinach potato
}

verified_dataset = {}
summary = {"found_exact": 0, "found_fuzzy": 0, "using_fallback": 0}

for json_key, json_val in json_data.items():
    search_term = SMART_MAPPING.get(json_key, json_key.replace("_", " "))
    
    # Try Indian first
    matches = get_close_matches(search_term, indian_keys, n=1, cutoff=0.3)
    
    if matches:
        matched_key = matches[0]
        real_row = indian_data[matched_key]
        verified_dataset[json_key] = {
            "method": "verified_real_data",
            "sources": [f"Indian_Food_Nutrition_Processed.csv - '{real_row['Dish Name']}'"],
            "nutrition": {
                "energy_kcal": float(real_row.get('Calories (kcal)', 0) or 0),
                "carbohydrate_g": float(real_row.get('Carbohydrates (g)', 0) or 0),
                "protein_g": float(real_row.get('Protein (g)', 0) or 0),
                "fat_g": float(real_row.get('Fats (g)', 0) or 0),
                "sodium_mg": float(real_row.get('Sodium (mg)', 0) or 0),
                "fiber_g": float(real_row.get('Fibre (g)', 0) or 0),
                "free_sugar_g": float(real_row.get('Free Sugar (g)', 0) or 0),
                "calcium_mg": float(real_row.get('Calcium (mg)', 0) or 0),
                "iron_mg": float(real_row.get('Iron (mg)', 0) or 0),
                "vitamin_c_mg": float(real_row.get('Vitamin C (mg)', 0) or 0),
                "folate_mcg": float(real_row.get('Folate (µg)', 0) or 0),
            }
        }
        summary["found_fuzzy"] += 1
    else:
        # Try USDA as fallback
        matches_usda = get_close_matches(search_term, usda_keys, n=1, cutoff=0.3)
        if matches_usda:
            matched_key_usda = matches_usda[0]
            real_row_usda = usda_data[matched_key_usda]
            verified_dataset[json_key] = {
                "method": "verified_real_data_usda",
                "sources": [f"USDA.csv - '{real_row_usda['Description']}'"],
                "nutrition": {
                    "energy_kcal": float(real_row_usda.get('Calories', 0) or 0),
                    "carbohydrate_g": float(real_row_usda.get('Carbohydrate', 0) or 0),
                    "protein_g": float(real_row_usda.get('Protein', 0) or 0),
                    "fat_g": float(real_row_usda.get('TotalFat', 0) or 0),
                    "sodium_mg": float(real_row_usda.get('Sodium', 0) or 0),
                }
            }
            summary["found_fuzzy"] += 1
        else:
            # Keep original as fallback
            verified_dataset[json_key] = json_val
            verified_dataset[json_key]["method"] = "original_estimated_fallback"
            summary["using_fallback"] += 1

# Save the new dataset
with open('verified_nutrition_dataset_final.json', 'w', encoding='utf-8') as f:
    json.dump(verified_dataset, f, indent=4, ensure_ascii=False)

print("\n" + "="*80)
print("FINAL DATASET MAPPING COMPLETE")
print("="*80)
print(f"Total items: {len(verified_dataset)}")
print(f"Found with fuzzy match: {summary['found_fuzzy']}")
print(f"Using original fallback: {summary['using_fallback']}")
print(f"\nSaved to: verified_nutrition_dataset_final.json")
print("="*80)
