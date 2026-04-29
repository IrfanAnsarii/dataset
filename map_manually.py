import json
import csv

# CAREFUL MANUAL MAPPING - One by one research
# Based on understanding of Assamese cuisine and what's actually in the CSVs

MANUAL_MAPPING = {
    # Assamese food key → (CSV file, exact dish name from that CSV)
    "akhoi": ("indian", "Murmura (Puffed rice)"),
    "ash_gourd_curry": ("indian", "Petha/Ash gourd (dry)"),
    "bamboo_shoot_chutney": ("indian", "Fermented bamboo shoot pickle (Mesu pickle)"),
    "banana_fry": ("indian", "Banana chips"),
    "bhat_kerela_fry": ("indian", "Teasel gourd (Teasel gourd)"),
    "bhut_chilly": ("indian", "Green chilli"),
    "bitter_gourd_fry": ("indian", "Bitter gourd fry"),
    "bitter_gourd_potato_fry": ("indian", "Bitter gourd with potato fry"),
    "bogori_amber": ("indian", "Mango pickle"),
    "boil_dal_rice": ("indian", "Khichdi"),
    "boiled_egg": ("indian", "Boiled eggs"),
    "boiled_ladies_finger": ("indian", "Bhindi fry"),
    "boiled_pork": ("usda", "PORK,FRESH,VARIOUS CUTS,LEAN,CKD,ROASTED"),
    "brinjal_chutney": ("indian", "Brinjal bharta"),
    "brinjal_curry": ("indian", "Brinjal curry"),
    "brinjal_fry": ("indian", "Brinjal fry"),
    "brooccoli_fry": ("indian", "Broccoli delight"),
    "but_chutney": ("indian", "Schezwan chutney"),
    "but_dal": ("indian", "Chana dal"),
    "but_fry": ("indian", "Dry washed urad"),
    "but_potato_fry": ("indian", "Aloo chana (Potato chickpea)"),
    "cabbage_fry": ("indian", "Cabbage fry"),
    "capsicum_pakoda": ("indian", "Capsicum pakora/pakoda"),
    "chicken_curry": ("indian", "Chicken curry"),
    "chicken_fry": ("indian", "Chicken fry"),
    "chilly": ("indian", "Green chilli"),
    "chilly_chutney": ("indian", "Green chutney"),
    "curd": ("indian", "Curd (Dahi)"),
    "curry_leaf_curry": ("indian", "Curry leaves (Kadi patta)"),
    "dang_bodi_fry": ("indian", "Long beans fry"),
    "dhekia_xaak_fry": ("indian", "Fiddlehead fern"),
    "duck_meat_curry": ("indian", "Duck curry"),
    "egg_curry": ("indian", "Egg curry"),
    "egg_fry": ("indian", "Fried Egg"),
    "fabian_carrot_fry": ("indian", "Carrot fry"),
    "fabian_fry": ("indian", "Beans fry"),
    "fish_chutney": ("indian", "Fish pickle"),
    "fish_curry": ("indian", "Fish curry"),
    "fish_fry": ("indian", "Fish fry"),
    "gourd_curry": ("indian", "Bottle gourd curry"),
    "green_leafy_fry": ("indian", "Spinach fry"),
    "gulab_jamun": ("indian", "Gulab Jamun with khoya"),
    "hyachinth_bean_fry": ("indian", "Hyacinth bean"),
    "jackfruit_curry": ("indian", "Jackfruit/Kathal (dry)"),
    "jackfruit_milk_shake": ("indian", "Jackfruit shake"),
    "kath_alu_curry": ("indian", "Yam/Elephant foot yam"),
    "kharoli": ("indian", "Khakhra"),
    "kolmu_xaak": ("indian", "Water spinach"),
    "kosu_leaf_curry": ("indian", "Colocasia leaves curry"),
    "ladies_finger_fry": ("indian", "Bhindi fry"),
    "lai_xaak": ("indian", "Mustard greens (Sarso)"),
    "lemon": ("indian", "Lemon"),
    "masoor_dal": ("indian", "Masoor dal"),
    "mati_dal": ("indian", "Black gram (Urad)"),
    "mix_fry": ("indian", "Mixed vegetable fry"),
    "moong_dal_curry": ("indian", "Moong dal"),
    "moong_masoor_dal": ("indian", "Whole moong (Moong ki dal)"),
    "mula_curry": ("indian", "Radish curry"),
    "onion": ("indian", "Onion"),
    "onion_pakoda": ("indian", "Onion pakora/pakoda"),
    "ou_tenga_masoor_dal": ("indian", "Masoor dal"),
    "paneer_curey": ("indian", "Paneer curry"),
    "papad": ("indian", "Papdi"),
    "papaya_xaar": ("indian", "Papaya (Raw)"),
    "payokh": ("indian", "Rice kheer"),
    "pickle": ("indian", "Mango pickle"),
    "pork_curry": ("indian", "Pork curry"),
    "pork_fry": ("indian", "Pork fry"),
    "potato_bean_carrot_fry": ("indian", "Mixed vegetable fry"),
    "potato_bean_fry": ("indian", "Beans with potato"),
    "potato_cauliflower_carrot_fry": ("indian", "Aloo gobi"),
    "potato_cauliflower_fry": ("indian", "Aloo gobi (Potato cauliflower)"),
    "potato_chutney": ("indian", "Potato"),
    "potato_fry": ("indian", "French fries"),
    "potato_kunduly_fry": ("indian", "Ivy gourd potato"),
    "pudina_dhaniya_chutney": ("indian", "Mint and coriander chutney (Pudinay aur dhaniye ki chutney)"),
    "rice": ("indian", "Boiled rice (Uble chawal)"),
    "rohor_mah_curry": ("indian", "Arhar dal (Pigeon pea)"),
    "salad": ("indian", "Salad"),
    "small_potato_fry": ("indian", "Potato"),
    "tamul_pan": ("indian", "Betel leaves"),
    "til_chutney": ("indian", "Sesame seed chutney"),
    "tomato_brinjal_chutney": ("indian", "Tomato"),
    "tomato_chutney": ("indian", "Tomato chutney"),
    "xaak and boot fry": ("indian", "Spinach with chickpea"),
    "xaak_motor_fry": ("indian", "Spinach with peas"),
    "xaak_potato_fry": ("indian", "Spinach with potato"),
}

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

print("Loading CSVs...")
indian_data = load_csv('Indian_Food_Nutrition_Processed.csv', 'Dish Name')
usda_data = load_csv('USDA.csv', 'Description')

print(f"Loaded {len(indian_data)} Indian dishes")
print(f"Loaded {len(usda_data)} USDA items")

print("\n" + "="*80)
print("SEARCHING FOR EXACT MATCHES IN CSVs...")
print("="*80 + "\n")

found_matches = {}
not_found = []

for json_key, (csv_source, search_name) in MANUAL_MAPPING.items():
    search_lower = search_name.lower().strip()
    
    if csv_source == "indian":
        data_dict = indian_data
        source_label = "INDIAN"
    else:
        data_dict = usda_data
        source_label = "USDA"
    
    # Try exact match first
    if search_lower in data_dict:
        row = data_dict[search_lower]
        found_matches[json_key] = {
            "source": source_label,
            "exact_name": search_name,
            "row": row
        }
        print(f"✓ {json_key:35} → {source_label:5} → {search_name}")
    else:
        # Try substring match
        matches = [k for k in data_dict.keys() if search_lower in k or k in search_lower]
        if matches:
            # Pick first match
            best_match = matches[0]
            row = data_dict[best_match]
            found_matches[json_key] = {
                "source": source_label,
                "exact_name": search_name,
                "actual_name": best_match,
                "row": row
            }
            print(f"≈ {json_key:35} → {source_label:5} → {best_match}")
        else:
            not_found.append(json_key)
            print(f"✗ {json_key:35} → NOT FOUND in {source_label}")

print("\n" + "="*80)
print(f"FOUND: {len(found_matches)} items")
print(f"NOT FOUND: {len(not_found)} items")
print("="*80)

if not_found:
    print("\nNOT FOUND ITEMS (need manual override):")
    for item in not_found:
        print(f"  - {item}")
