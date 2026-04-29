import json
import csv

# Load the JSON to see all items
with open('realistic_nutrition_dataset.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

print("=" * 80)
print("ASSAMESE FOODS IN YOUR DATASET - NEED PROPER RESEARCH")
print("=" * 80)

items = list(json_data.keys())
for i, item in enumerate(items, 1):
    print(f"{i}. {item}")

print(f"\nTotal items: {len(items)}")
print("\nNow loading available options from both CSVs...")
print("=" * 80)

# Load Indian CSV
indian_foods = []
with open('Indian_Food_Nutrition_Processed.csv', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        indian_foods.append(row['Dish Name'])

print(f"\nIndian Food CSV has {len(indian_foods)} dishes")
print("\nSample Indian dishes (first 50):")
for dish in indian_foods[:50]:
    print(f"  - {dish}")

# Load USDA CSV
usda_items = []
with open('USDA.csv', 'r', encoding='latin1') as f:
    for row in csv.DictReader(f):
        usda_items.append(row['Description'])

print(f"\n\nUSDA CSV has {len(usda_items)} items")
print("\nSample USDA items (first 30):")
for item in usda_items[:30]:
    print(f"  - {item}")

# Now create a file with recommendations
print("\n" + "=" * 80)
print("RESEARCH NEEDED: What each Assamese food actually is")
print("=" * 80)

recommendations = {
    "akhoi": "Puffed rice (search for: murmura, puffed rice)",
    "ash_gourd_curry": "Ash gourd / Bottle gourd curry (search for: petha, ash gourd, bottle gourd)",
    "bamboo_shoot_chutney": "Bamboo shoot pickle (search for: bamboo)",
    "banana_fry": "Banana chips/fritters (search for: banana)",
    "bhat_kerela_fry": "Teasel gourd fry (search for: teasel, fry)",
    "bhut_chilly": "Ghost chilli/Green chilli (search for: chilli, green pepper)",
    "bitter_gourd_fry": "Bitter melon/Karela fry (search for: bitter gourd, karela)",
    "bitter_gourd_potato_fry": "Bitter gourd with potato (search for: bitter, potato)",
    "bogori_amber": "Pickled fruits/preserves (search for: pickle, preserve)",
    "boil_dal_rice": "Rice with lentils (search for: rice, dal, khichdi)",
    "boiled_egg": "Boiled egg (search for: egg)",
    "boiled_ladies_finger": "Boiled okra/Bhindi (search for: okra, bhindi)",
    "boiled_pork": "Boiled pork (search for: pork)",
    "brinjal_chutney": "Eggplant chutney/Brinjal bharta (search for: brinjal, eggplant)",
    "brinjal_curry": "Eggplant curry (search for: brinjal curry, eggplant)",
    "brinjal_fry": "Fried eggplant (search for: brinjal fry)",
    "brooccoli_fry": "Fried broccoli (search for: broccoli)",
    "but_chutney": "Roasted gram chutney (search for: dal chutney, roasted)",
    "but_dal": "Roasted gram/Chana (search for: chana, roasted gram)",
    "but_fry": "Roasted gram fry (search for: roasted gram)",
    "but_potato_fry": "Chickpea potato fry (search for: chickpea, potato)",
    "cabbage_fry": "Fried cabbage (search for: cabbage)",
    "capsicum_pakoda": "Capsicum fritters (search for: capsicum, pakora)",
    "chicken_curry": "Chicken curry (search for: chicken curry)",
    "chicken_fry": "Fried chicken (search for: chicken fry)",
    "chilly": "Green chilli (search for: chilli, green pepper)",
    "chilly_chutney": "Chilli chutney (search for: chilli chutney)",
    "curd": "Yogurt/Curd (search for: curd, yogurt)",
    "curry_leaf_curry": "Curry leaves (search for: curry leaf)",
    "dang_bodi_fry": "Yard-long beans fry (search for: beans, yard-long)",
    "dhekia_xaak_fry": "Fiddlehead fern fry (search for: fern, fiddlehead)",
    "duck_meat_curry": "Duck curry (search for: duck)",
    "egg_curry": "Egg curry (search for: egg curry)",
    "egg_fry": "Fried egg (search for: fried egg)",
    "fabian_carrot_fry": "Beans and carrot fry (search for: beans, carrot)",
    "fabian_fry": "Broad beans fry (search for: beans fry)",
    "fish_chutney": "Fish pickle (search for: fish pickle)",
    "fish_curry": "Fish curry (search for: fish curry)",
    "fish_fry": "Fried fish (search for: fish fry)",
    "gourd_curry": "Bottle gourd curry (search for: bottle gourd, pumpkin)",
    "green_leafy_fry": "Spinach/Leafy greens fry (search for: spinach, greens)",
    "gulab_jamun": "Gulab jamun sweet (search for: gulab jamun)",
    "hyachinth_bean_fry": "Hyacinth beans (search for: beans, legume)",
    "jackfruit_curry": "Jackfruit curry (search for: jackfruit)",
    "jackfruit_milk_shake": "Jackfruit shake (search for: jackfruit)",
    "kath_alu_curry": "Yam curry (search for: yam)",
    "kharoli": "Mustard paste (search for: mustard)",
    "kolmu_xaak": "Water spinach (search for: spinach, leafy)",
    "kosu_leaf_curry": "Taro/Colocasia leaves (search for: taro, colocasia)",
    "ladies_finger_fry": "Okra fry/Bhindi (search for: okra, bhindi)",
    "lai_xaak": "Mustard greens (search for: mustard, greens)",
    "lemon": "Lemon (search for: lemon)",
    "masoor_dal": "Red lentil (search for: masoor, lentil)",
    "mati_dal": "Black gram/Urad (search for: urad, black gram)",
    "mix_fry": "Mixed vegetable fry (search for: mixed vegetable)",
    "moong_dal_curry": "Green gram curry (search for: moong, green gram)",
    "moong_masoor_dal": "Mixed lentils (search for: moong, masoor)",
    "mula_curry": "Radish curry (search for: radish)",
    "onion": "Onion (search for: onion)",
    "onion_pakoda": "Onion fritters (search for: onion pakora)",
    "ou_tenga_masoor_dal": "Elephant apple lentil (search for: elephant apple, sour)",
    "paneer_curey": "Cottage cheese curry (search for: paneer)",
    "papad": "Papad/Wafer (search for: papad)",
    "papaya_xaar": "Raw papaya (search for: papaya)",
    "payokh": "Rice pudding (search for: kheer, pudding)",
    "pickle": "Pickle/Preserve (search for: pickle, preserve)",
    "pork_curry": "Pork curry (search for: pork curry)",
    "pork_fry": "Fried pork (search for: pork fry)",
    "potato_bean_carrot_fry": "Potato beans carrot (search for: mixed vegetables)",
    "potato_bean_fry": "Potato beans fry (search for: beans, potato)",
    "potato_cauliflower_carrot_fry": "Aloo gobi with carrot (search for: aloo gobi, mixed)",
    "potato_cauliflower_fry": "Aloo gobi (search for: aloo gobi)",
    "potato_chutney": "Potato chutney (search for: potato)",
    "potato_fry": "French fries / Fried potato (search for: potato fry, french fries)",
    "potato_kunduly_fry": "Ivy gourd potato (search for: ivy gourd, potato)",
    "pudina_dhaniya_chutney": "Mint coriander chutney (search for: mint, cilantro)",
    "rice": "Rice (search for: rice, boiled)",
    "rohor_mah_curry": "Pigeon pea curry (search for: arhar, pigeon pea)",
    "salad": "Salad/Green salad (search for: salad)",
    "small_potato_fry": "Baby potato fry (search for: potato)",
    "tamul_pan": "Betel leaf/Pan (search for: betel)",
    "til_chutney": "Sesame chutney (search for: sesame)",
    "tomato_brinjal_chutney": "Tomato eggplant (search for: tomato, brinjal)",
    "tomato_chutney": "Tomato chutney (search for: tomato chutney)",
    "xaak and boot fry": "Spinach chickpea (search for: spinach, chickpea)",
    "xaak_motor_fry": "Spinach peas (search for: spinach, peas)",
    "xaak_potato_fry": "Spinach potato (search for: spinach, potato)",
}

print("\nRECOMMENDED RESEARCH MAPPING:")
for key, info in recommendations.items():
    print(f"\n{key}")
    print(f"  → {info}")
