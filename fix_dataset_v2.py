import json
import csv
import difflib

# Manual mappings for Assamese/regional dish names to standard Indian/USDA terms
TRANSLATIONS = {
    "akhoi": "puffed rice",
    "ash_gourd_curry": "ash gourd",
    "bamboo_shoot_chutney": "bamboo shoot pickle",
    "banana_fry": "banana chips",
    "bhat_kerela_fry": "teasel gourd",
    "bhut_chilly": "green chilli",
    "bitter_gourd_fry": "bitter gourd",
    "bitter_gourd_potato_fry": "bitter gourd potato",
    "bogori_amber": "fruit pickle",
    "boil_dal_rice": "rice with dal",
    "boiled_egg": "boiled egg",
    "boiled_ladies_finger": "okra",
    "boiled_pork": "pork",
    "brinjal_chutney": "brinjal bharta",
    "brinjal_curry": "brinjal curry",
    "brinjal_fry": "brinjal fry",
    "brooccoli_fry": "broccoli",
    "but_chutney": "channa dal chutney",
    "but_dal": "channa dal",
    "but_fry": "roasted gram",
    "but_potato_fry": "chickpea potato",
    "cabbage_fry": "cabbage fry",
    "capsicum_pakoda": "capsicum pakora",
    "chicken_curry": "chicken curry",
    "chicken_fry": "chicken fry",
    "chilly": "green chilli",
    "chilly_chutney": "chilli chutney",
    "curd": "curd",
    "curry_leaf_curry": "curry leaves",
    "dang_bodi_fry": "yard long beans",
    "dhekia_xaak_fry": "fiddlehead fern",
    "duck_meat_curry": "duck meat",
    "egg_curry": "egg curry",
    "egg_fry": "fried egg",
    "fabian_carrot_fry": "carrot fry",
    "fabian_fry": "beans fry",
    "fish_chutney": "fish pickle",
    "fish_curry": "fish curry",
    "fish_fry": "fish fry",
    "gourd_curry": "bottle gourd curry",
    "green_leafy_fry": "spinach fry",
    "gulab_jamun": "gulab jamun",
    "hyachinth_bean_fry": "hyacinth beans",
    "jackfruit_curry": "jackfruit curry",
    "jackfruit_milk_shake": "jackfruit shake",
    "kath_alu_curry": "yam curry",
    "kharoli": "mustard paste",
    "kolmu_xaak": "water spinach",
    "kosu_leaf_curry": "colocasia leaves",
    "ladies_finger_fry": "bhindi fry",
    "lai_xaak": "mustard greens",
    "lemon": "lemon",
    "masoor_dal": "masoor dal",
    "mati_dal": "black gram dal",
    "mix_fry": "mixed vegetable fry",
    "moong_dal_curry": "moong dal",
    "moong_masoor_dal": "moong masoor dal",
    "mula_curry": "radish curry",
    "onion": "onion",
    "onion_pakoda": "onion pakora",
    "ou_tenga_masoor_dal": "elephant apple dal",
    "paneer_curey": "paneer curry",
    "papad": "papad",
    "papaya_xaar": "raw papaya",
    "payokh": "rice kheer",
    "pickle": "mango pickle",
    "pork_curry": "pork curry",
    "pork_fry": "pork fry",
    "potato_bean_carrot_fry": "potato bean carrot",
    "potato_bean_fry": "potato beans",
    "potato_cauliflower_carrot_fry": "aloo gobi carrot",
    "potato_cauliflower_fry": "aloo gobi",
    "potato_chutney": "potato mash",
    "potato_fry": "french fries",
    "potato_kunduly_fry": "ivy gourd potato",
    "pudina_dhaniya_chutney": "mint coriander chutney",
    "rice": "boiled rice",
    "rohor_mah_curry": "arhar dal",
    "salad": "green salad",
    "small_potato_fry": "baby potato fry",
    "tamul_pan": "betel leaf",
    "til_chutney": "sesame chutney",
    "tomato_brinjal_chutney": "tomato brinjal",
    "tomato_chutney": "tomato chutney",
    "xaak and boot fry": "spinach chickpea",
    "xaak_motor_fry": "spinach peas",
    "xaak_potato_fry": "spinach potato"
}

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_csv(filepath, name_col):
    data = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                data[row[name_col].lower()] = row
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin1') as f:
            for row in csv.DictReader(f):
                data[row[name_col].lower()] = row
    return data

def find_best_match(search_term, db_keys):
    matches = difflib.get_close_matches(search_term, db_keys, n=1, cutoff=0.4)
    if matches:
        return matches[0]
    
    # Try subset matching
    for key in db_keys:
        if any(word in key for word in search_term.split()):
            return key
    return None

def main():
    json_data = load_json('realistic_nutrition_dataset.json')
    indian_data = load_csv('Indian_Food_Nutrition_Processed.csv', 'Dish Name')
    usda_data = load_csv('USDA.csv', 'Description')
    
    indian_names = list(indian_data.keys())
    usda_names = list(usda_data.keys())
    
    verified_dataset = {}
    
    for json_key, json_val in json_data.items():
        translated_term = TRANSLATIONS.get(json_key, json_key.replace('_', ' '))
        
        match_indian = find_best_match(translated_term, indian_names)
        
        if match_indian:
            real_row = indian_data[match_indian]
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
        else:
            match_usda = find_best_match(translated_term, usda_names)
            if match_usda:
                real_row = usda_data[match_usda]
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
                 verified_dataset[json_key] = json_val
                 verified_dataset[json_key]["method"] = "unverified_estimated_fallback"
                 
    with open('verified_nutrition_dataset_accurate.json', 'w', encoding='utf-8') as f:
        json.dump(verified_dataset, f, indent=4)
        
if __name__ == "__main__":
    main()
