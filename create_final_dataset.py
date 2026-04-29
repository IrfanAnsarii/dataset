import json
import csv

# kJ to kcal conversion factor (used for IFCT 2017 energy values)
KJ_TO_KCAL = 4.184

# ---------------------------------------------------------------------------
# MANUAL MAPPING
# Maps each Assamese/regional food key to its best matching entry in one of
# the three data sources (Indian Food CSV, USDA CSV, IFCT 2017 xlsx/csv).
# Only exact or clearly standard matches are included here.
# Keys that cannot be matched with confidence are absent (→ empty nutrition).
# ---------------------------------------------------------------------------
MANUAL_MAPPING = {
    # food_key: (source, exact_dish_name_in_source)
    # source values: "indian", "usda", "ifct"
    "akhoi":                      ("indian", "Murmura (Puffed rice)"),
    "ash_gourd_curry":            ("ifct",   "Ash gourd"),
    "bamboo_shoot_chutney":       ("indian", "Fermented bamboo shoot pickle (Mesu pickle)"),
    "banana_fry":                 ("indian", "Banana chips (Kele ke chips)"),
    "bhut_chilly":                ("ifct",   "Chillies, green-1"),
    "bitter_gourd_fry":           ("usda",   "balsam-pear (bitter gourd),pods,ckd,bld,drnd,wo/salt"),
    "bogori_amber":               ("indian", "Mango pickle (Aam ka achaar)"),
    "boil_dal_rice":              ("indian", "Plain khitchdi (Plain khichri/khichdi)"),
    "boiled_egg":                 ("indian", "Boiled egg (Ubla anda)"),
    "boiled_ladies_finger":       ("indian", "Okra/Lady's fingers fry (Bhindi sabzi/sabji/subji)"),
    "boiled_pork":                ("ifct",   "Pork, shoulder"),
    "brinjal_chutney":            ("indian", "Brinjal bhartha (Baingan ka bhartha)"),
    "brinjal_curry":              ("ifct",   "Brinjal-1"),
    "brinjal_fry":                ("ifct",   "Brinjal-1"),
    "brooccoli_fry":              ("indian", "Broccoli delight"),
    "but_chutney":                ("indian", "Schezwan chutney"),
    "but_dal":                    ("ifct",   "Bengal gram, dal"),
    "but_fry":                    ("indian", "Dry washed urad"),
    "cabbage_fry":                ("usda",   "cabbage,ckd,bld,drnd,wo/salt"),
    "chicken_curry":              ("indian", "Chicken curry"),
    "chilly":                     ("ifct",   "Chillies, green-1"),
    "chilly_chutney":             ("indian", "Green chutney"),
    "dhekia_xaak_fry":            ("usda",   "fiddlehead ferns,raw"),
    "duck_meat_curry":            ("usda",   "duck,domesticated,meat&skn,ckd,rstd"),
    "egg_curry":                  ("indian", "Egg curry (Anda curry)"),
    "egg_fry":                    ("indian", "Fried Egg "),
    "fabian_carrot_fry":          ("ifct",   "Carrot, orange"),
    "fish_curry":                 ("indian", "Fish curry (Machli curry)"),
    "fish_fry":                   ("indian", "Fried fish (Indian style) (Tali hui machli)"),
    "gourd_curry":                ("indian", "Stuffed bottle gourd (Stuffed ghiya/lauki)"),
    "green_leafy_fry":            ("ifct",   "Spinach"),
    "gulab_jamun":                ("indian", "Gulab Jamun with khoya"),
    "hyachinth_bean_fry":         ("usda",   "hyacinth-beans,immat seeds,ckd,bld,drnd,wo/salt"),
    "jackfruit_curry":            ("indian", "Jackfruit sabzi (Kathal ki sabzi)"),
    "kath_alu_curry":             ("ifct",   "Yam, elephant"),
    "kharoli":                    ("indian", "Khakhra"),
    "kosu_leaf_curry":            ("ifct",   "Colocasia leaves, green"),
    "ladies_finger_fry":          ("indian", "Okra/Lady's fingers fry (Bhindi sabzi/sabji/subji)"),
    "lai_xaak":                   ("ifct",   "Mustard leaves"),
    "lemon":                      ("ifct",   "Lemon, juice"),
    "masoor_dal":                 ("indian", "Whole masoor (Masoor ki dal)"),
    "mati_dal":                   ("ifct",   "Black gram, dal"),
    "moong_dal_curry":            ("indian", "Washed moong dal (Dhuli moong ki dal)"),
    "moong_masoor_dal":           ("indian", "Whole masoor (Masoor ki dal)"),
    "mula_curry":                 ("ifct",   "Radish, elongate, white skin"),
    "onion":                      ("ifct",   "Onion, big"),
    "onion_pakoda":               ("indian", "Onion pakora/pakoda (Pyaaz ke pakode)"),
    "ou_tenga_masoor_dal":        ("indian", "Whole masoor (Masoor ki dal)"),
    "paneer_curey":               ("indian", "Paneer curry"),
    "papad":                      ("indian", "Papdi"),
    "papaya_xaar":                ("indian", "Raw papaya with coconut (Papaya thoran)"),
    "payokh":                     ("indian", "Rice kheer (Chawal ki kheer)"),
    "pickle":                     ("indian", "Mango pickle (Aam ka achaar)"),
    "pork_curry":                 ("ifct",   "Pork, shoulder"),
    "pork_fry":                   ("ifct",   "Pork, chops"),
    "potato_chutney":             ("ifct",   "Potato, brown skin, big"),
    "potato_fry":                 ("ifct",   "Potato, brown skin, big"),
    "potato_kunduly_fry":         ("ifct",   "Bitter gourd, jagged, smooth ridges, elongate"),
    "pudina_dhaniya_chutney":     ("indian", "Mint and coriander chutney (Pudinay aur dhaniye ki chutney)"),
    "rice":                       ("indian", "Boiled rice (Uble chawal)"),
    "rohor_mah_curry":            ("indian", "Arhar with spinach (Arhar dal aur palak)"),
    "small_potato_fry":           ("ifct",   "Potato, brown skin, small"),
    "tamul_pan":                  ("ifct",   "Betel leaves, big (kolkata)"),
    "til_chutney":                ("usda",   "sesame seeds,whole,dried"),
    "tomato_chutney":             ("indian", "Tomato chutney (Tamatar ki chutney)"),
    "xaak and boot fry":          ("indian", "Spinach chickpeas cutlet (Palak channa dal cutlet)"),
    "xaak_potato_fry":            ("indian", "Spinach and potato (Palak aloo)"),
}

# Items with no reliable match in any source — nutrition will be left null
NO_MATCH_ITEMS = {
    "bhat_kerela_fry",        # Teasel gourd — not in any source
    "bitter_gourd_potato_fry",# Bitter gourd + potato combo — not in any source
    "but_potato_fry",         # Chickpea + potato combo — not in any source
    "capsicum_pakoda",        # Capsicum pakora — not in Indian/USDA/IFCT
    "chicken_fry",            # Specific chicken fry not found
    "curry_leaf_curry",       # Not in any source
    "curd",                   # Plain curd/yogurt not found as standalone dish
    "dang_bodi_fry",          # Yard-long beans fry — not in any source
    "fabian_fry",             # Beans fry — not in any source
    "fish_chutney",           # Fish pickle — not in any source
    "jackfruit_milk_shake",   # Jackfruit shake — not in any source
    "kolmu_xaak",             # Water spinach — not in any source
    "mix_fry",                # Mixed vegetable fry — not in any source
    "potato_bean_carrot_fry", # Combo — not in any source
    "potato_bean_fry",        # Combo — not in any source
    "potato_cauliflower_carrot_fry",  # Combo — not in any source
    "potato_cauliflower_fry", # Aloo gobi — not in any source
    "salad",                  # Too generic
    "tomato_brinjal_chutney", # Not in any source
    "xaak_motor_fry",         # Spinach + peas — not in any source
}


def load_csv(filename, name_col):
    """Load a CSV file keyed by name_col (case-insensitive, stripped)."""
    data = {}
    for enc in ('utf-8', 'latin1'):
        try:
            with open(filename, 'r', encoding=enc) as f:
                for row in csv.DictReader(f):
                    key = row[name_col].lower().strip()
                    data[key] = row
            break
        except UnicodeDecodeError:
            continue
    return data


def load_ifct(filename):
    """Load IFCT 2017 CSV keyed by 'name' column (case-insensitive, stripped).
    Returns dict mapping lowercase name → row dict with standard column keys."""
    data = {}
    for enc in ('utf-8', 'latin1'):
        try:
            with open(filename, 'r', encoding=enc) as f:
                for row in csv.DictReader(f):
                    # Strip BOM from keys that may have it
                    clean_row = {k.lstrip('\ufeff'): v for k, v in row.items()}
                    name = clean_row.get('name', '').strip()
                    if name:
                        data[name.lower()] = clean_row
            break
        except UnicodeDecodeError:
            continue
    return data


def load_ifct(filename):
    """Load IFCT 2017 CSV keyed by 'name' column (case-insensitive, stripped).
    Returns dict mapping lowercase name → row dict with standard column keys."""
    data = {}
    for enc in ('utf-8', 'latin1'):
        try:
            with open(filename, 'r', encoding=enc) as f:
                for row in csv.DictReader(f):
                    # Strip BOM from keys that may have it
                    clean_row = {k.lstrip('\ufeff'): v for k, v in row.items()}
                    name = clean_row.get('name', '').strip()
                    if name:
                        data[name.lower()] = clean_row
            break
        except UnicodeDecodeError:
            continue
    return data


def safe_float(val):
    try:
        return float(val) if val is not None and val != '' else None
    except (TypeError, ValueError):
        return None


def nutrition_from_indian(row):
    return {
        "energy_kcal":    safe_float(row.get('Calories (kcal)')),
        "carbohydrate_g": safe_float(row.get('Carbohydrates (g)')),
        "protein_g":      safe_float(row.get('Protein (g)')),
        "fat_g":          safe_float(row.get('Fats (g)')),
        "sodium_mg":      safe_float(row.get('Sodium (mg)')),
        "fiber_g":        safe_float(row.get('Fibre (g)')),
        "free_sugar_g":   safe_float(row.get('Free Sugar (g)')),
        "calcium_mg":     safe_float(row.get('Calcium (mg)')),
        "iron_mg":        safe_float(row.get('Iron (mg)')),
        "vitamin_c_mg":   safe_float(row.get('Vitamin C (mg)')),
        "folate_mcg":     safe_float(row.get('Folate (µg)')),
    }


def nutrition_from_usda(row):
    return {
        "energy_kcal":    safe_float(row.get('Calories')),
        "carbohydrate_g": safe_float(row.get('Carbohydrate')),
        "protein_g":      safe_float(row.get('Protein')),
        "fat_g":          safe_float(row.get('TotalFat')),
        "sodium_mg":      safe_float(row.get('Sodium')),
        "fiber_g":        None,
        "free_sugar_g":   None,
        "calcium_mg":     safe_float(row.get('Calcium')),
        "iron_mg":        safe_float(row.get('Iron')),
        "vitamin_c_mg":   safe_float(row.get('VitaminC')),
        "folate_mcg":     None,
    }


def nutrition_from_ifct(row):
    # IFCT energy (enerc) is in kJ; convert to kcal (÷ 4.184)
    enerc_kj = safe_float(row.get('enerc'))
    energy_kcal = round(enerc_kj / KJ_TO_KCAL, 2) if enerc_kj is not None else None
    return {
        "energy_kcal":    energy_kcal,
        "carbohydrate_g": safe_float(row.get('choavldf')),
        "protein_g":      safe_float(row.get('protcnt')),
        "fat_g":          safe_float(row.get('fatce')),
        "sodium_mg":      safe_float(row.get('na')),
        "fiber_g":        safe_float(row.get('fibtg')),
        "free_sugar_g":   None,
        "calcium_mg":     safe_float(row.get('ca')),
        "iron_mg":        safe_float(row.get('fe')),
        "vitamin_c_mg":   safe_float(row.get('vitc')),
        "folate_mcg":     safe_float(row.get('folsum')),
    }


def empty_nutrition():
    return {
        "energy_kcal":    None,
        "carbohydrate_g": None,
        "protein_g":      None,
        "fat_g":          None,
        "sodium_mg":      None,
        "fiber_g":        None,
        "free_sugar_g":   None,
        "calcium_mg":     None,
        "iron_mg":        None,
        "vitamin_c_mg":   None,
        "folate_mcg":     None,
    }


def lookup(name, data_dict):
    """Return (matched_key, row) if found; else (None, None).
    Tries exact match, then case-insensitive substring containment."""
    key = name.lower().strip()
    if key in data_dict:
        return key, data_dict[key]
    # Substring: the target name is contained in a data key or vice versa
    for k in data_dict:
        if key in k or k in key:
            return k, data_dict[k]
    return None, None


# ---------------------------------------------------------------------------
# Load data sources
# ---------------------------------------------------------------------------
print("Loading data sources...")
indian_data = load_csv('Indian_Food_Nutrition_Processed.csv', 'Dish Name')
usda_data   = load_csv('USDA.csv', 'Description')
ifct_data   = load_ifct('ifct2017_compositions.csv')
print(f"  Indian Food: {len(indian_data)} items")
print(f"  USDA:        {len(usda_data)} items")
print(f"  IFCT 2017:   {len(ifct_data)} items")

with open('realistic_nutrition_dataset.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# ---------------------------------------------------------------------------
# Build the verified dataset
# ---------------------------------------------------------------------------
verified_dataset = {}
summary = {"exact_match": 0, "no_match": 0}

for json_key in json_data:
    mapping = MANUAL_MAPPING.get(json_key)

    if mapping is None:
        # No manual mapping → no match
        verified_dataset[json_key] = {
            "method": "no_match",
            "sources": [],
            "nutrition": empty_nutrition(),
        }
        summary["no_match"] += 1
        continue

    source, dish_name = mapping

    if source == "indian":
        matched_key, row = lookup(dish_name, indian_data)
        if row is not None:
            verified_dataset[json_key] = {
                "method": "exact_match",
                "sources": [f"Indian_Food_Nutrition_Processed.csv - '{row['Dish Name']}'"],
                "nutrition": nutrition_from_indian(row),
            }
            summary["exact_match"] += 1
        else:
            verified_dataset[json_key] = {
                "method": "no_match",
                "sources": [],
                "nutrition": empty_nutrition(),
            }
            summary["no_match"] += 1

    elif source == "usda":
        matched_key, row = lookup(dish_name, usda_data)
        if row is not None:
            verified_dataset[json_key] = {
                "method": "exact_match",
                "sources": [f"USDA.csv - '{row['Description']}'"],
                "nutrition": nutrition_from_usda(row),
            }
            summary["exact_match"] += 1
        else:
            verified_dataset[json_key] = {
                "method": "no_match",
                "sources": [],
                "nutrition": empty_nutrition(),
            }
            summary["no_match"] += 1

    elif source == "ifct":
        matched_key, row = lookup(dish_name, ifct_data)
        if row is not None:
            verified_dataset[json_key] = {
                "method": "exact_match",
                "sources": [f"ifct2017_compositions.csv - '{row.get('name', dish_name)}'"],
                "nutrition": nutrition_from_ifct(row),
            }
            summary["exact_match"] += 1
        else:
            verified_dataset[json_key] = {
                "method": "no_match",
                "sources": [],
                "nutrition": empty_nutrition(),
            }
            summary["no_match"] += 1

# ---------------------------------------------------------------------------
# Save output
# ---------------------------------------------------------------------------
with open('verified_nutrition_dataset_final.json', 'w', encoding='utf-8') as f:
    json.dump(verified_dataset, f, indent=4, ensure_ascii=False)

print("\n" + "=" * 80)
print("FINAL DATASET MAPPING COMPLETE")
print("=" * 80)
print(f"Total items:       {len(verified_dataset)}")
print(f"Exact/std matches: {summary['exact_match']}")
print(f"No match (empty):  {summary['no_match']}")
print(f"\nSaved to: verified_nutrition_dataset_final.json")
print("=" * 80)
