"""
Curated skincare catalog with Indian Rupee (₹) pricing, active ingredients,
skin types, concerns, and routine guidance.
"""

SEED_PRODUCTS = [
    # --- OILY / ACNE PRONE ---
    {
        "name": "Salicylic Acid 2% Gentle Cleanser",
        "brand": "The Derma Co",
        "category": "Cleanser",
        "price_inr": 299.00,
        "target_skin_type": "Oily",
        "target_concerns": "Acne, Blackheads, Oiliness",
        "key_ingredients": "2% Salicylic Acid, Witch Hazel, Allantoin",
        "description": "Penetrates deep into pores to dissolve oil, clear blackheads, and prevent active breakout formation.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "Purifying Neem Face Wash",
        "brand": "Himalaya Herbals",
        "category": "Cleanser",
        "price_inr": 165.00,
        "target_skin_type": "Oily",
        "target_concerns": "Acne, Redness, Oiliness",
        "key_ingredients": "Neem Extract, Turmeric",
        "description": "Budget-friendly antibacterial botanical wash that cools inflammation and purifies active pimples.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "AHA BHA 10% Clarifying Exfoliating Toner",
        "brand": "Minimalist",
        "category": "Toner",
        "price_inr": 399.00,
        "target_skin_type": "Oily",
        "target_concerns": "Acne, Enlarged Pores, Texture",
        "key_ingredients": "Glycolic Acid, Salicylic Acid, Aloe Vera",
        "description": "Pore-clearing exfoliant that lifts dead skin cells and balances excessive sebum secretion.",
        "budget_tier": "Budget",
        "usage_time": "PM"
    },
    {
        "name": "Green Tea Alcohol-Free Toner",
        "brand": "Plum",
        "category": "Toner",
        "price_inr": 299.00,
        "target_skin_type": "Oily",
        "target_concerns": "Oiliness, Open Pores, Redness",
        "key_ingredients": "Green Tea Leaf Extract, Glycolic Acid",
        "description": "Antioxidant-rich toner that refreshes fatigued skin and controls noon-time T-zone shine.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "Niacinamide 10% + Zinc 1% Oil Control Serum",
        "brand": "Minimalist",
        "category": "Serum",
        "price_inr": 599.00,
        "target_skin_type": "Oily",
        "target_concerns": "Acne, Pigmentation, Dark Spots, Sebum",
        "key_ingredients": "10% Niacinamide, 1% Zinc PCA, Centella Water",
        "description": "Clinically proven to balance lipid production, fade post-acne dark marks, and refine rough pores.",
        "budget_tier": "Mid",
        "usage_time": "Both"
    },
    {
        "name": "2% Salicylic Acid Face Serum",
        "brand": "Deconstruct",
        "category": "Serum",
        "price_inr": 499.00,
        "target_skin_type": "Oily",
        "target_concerns": "Acne, Blackheads, Clogged Pores",
        "key_ingredients": "2% Salicylic Acid, 3% Niacinamide",
        "description": "Fast-acting spot and pore treatment that calms angry inflamed pimples without drying the face.",
        "budget_tier": "Budget",
        "usage_time": "PM"
    },
    {
        "name": "Oil-Free Green Tea Mattifying Gel",
        "brand": "Plum",
        "category": "Moisturizer",
        "price_inr": 395.00,
        "target_skin_type": "Oily",
        "target_concerns": "Oiliness, Acne, Shine",
        "key_ingredients": "Green Tea, Glycolic Acid, Licorice Extract",
        "description": "Ultra-lightweight oil-free hydration that leaves a smooth non-sticky matte finish all day.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "72H Oil-Free Hydrating Gel",
        "brand": "Dot & Key Cica",
        "category": "Moisturizer",
        "price_inr": 445.00,
        "target_skin_type": "Oily",
        "target_concerns": "Acne, Redness, Dehydration",
        "key_ingredients": "Centella Asiatica (Cica), Niacinamide, Tea Tree",
        "description": "Cooling calms irritated acne flares while restoring skin barrier hydration.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "Ultra-Matte Dry Touch Sunscreen Gel SPF 50 PA++++",
        "brand": "Re'equil",
        "category": "Sunscreen",
        "price_inr": 699.00,
        "target_skin_type": "Oily",
        "target_concerns": "Sun Protection, Acne Prevention, Tanning",
        "key_ingredients": "Octinoxate, Titanium Dioxide, Zinc Oxide",
        "description": "Top-rated matte sunscreen for humid weather. Leaves zero white cast and no greasy shine.",
        "budget_tier": "Mid",
        "usage_time": "AM"
    },
    {
        "name": "Matte Finish Sunscreen SPF 50 PA+++",
        "brand": "Joy Revivify",
        "category": "Sunscreen",
        "price_inr": 299.00,
        "target_skin_type": "Oily",
        "target_concerns": "Sun Protection, Oiliness",
        "key_ingredients": "Broad Spectrum UV Filters, Tea Tree Oil",
        "description": "Affordable oil-control sunscreen that defends against sunburn and UV hyperpigmentation.",
        "budget_tier": "Budget",
        "usage_time": "AM"
    },

    # --- DRY / DEHYDRATED SKIN ---
    {
        "name": "Hydrating Gentle Cream Cleanser",
        "brand": "Dot & Key / CeraVe",
        "category": "Cleanser",
        "price_inr": 349.00,
        "target_skin_type": "Dry",
        "target_concerns": "Dryness, Flaking, Dullness",
        "key_ingredients": "Ceramides, Hyaluronic Acid, Oat Extract",
        "description": "Milky non-foaming wash that lifts dust while nourishing dry, tight, flaking skin.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "Kind To Skin Refreshing Facial Wash",
        "brand": "Simple",
        "category": "Cleanser",
        "price_inr": 299.00,
        "target_skin_type": "Dry",
        "target_concerns": "Sensitivity, Dryness",
        "key_ingredients": "Pro-Vitamin B5, Vitamin E, Triple Purified Water",
        "description": "100% soap-free cleanser that leaves skin feeling soft, calm, and supple.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "Hyaluronic & Polyglutamic Acid Hydrating Mist",
        "brand": "Minimalist",
        "category": "Toner",
        "price_inr": 399.00,
        "target_skin_type": "Dry",
        "target_concerns": "Dryness, Fine Lines, Tightness",
        "key_ingredients": "Multi-Weight Hyaluronic Acid, PGA, Glycerin",
        "description": "Deeply quenches dehydrated skin layers, boosting bounce and elasticity.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "Hyaluronic Acid 2% + B5 Plumping Serum",
        "brand": "Minimalist",
        "category": "Serum",
        "price_inr": 599.00,
        "target_skin_type": "Dry",
        "target_concerns": "Dehydration, Dullness, Fine Lines",
        "key_ingredients": "2% Hyaluronic Acid, Vitamin B5 (Panthenol)",
        "description": "Water-based hydration magnet providing multi-level skin moisture replenishment.",
        "budget_tier": "Mid",
        "usage_time": "Both"
    },
    {
        "name": "Ceramide & Hyaluronic Barrier Relief Cream",
        "brand": "Dr. Sheth's",
        "category": "Moisturizer",
        "price_inr": 499.00,
        "target_skin_type": "Dry",
        "target_concerns": "Dryness, Barrier Damage, Flakiness",
        "key_ingredients": "Ceramide Complex, Hyaluronic Acid, Shea Butter",
        "description": "Rich barrier repair cream specifically tailored to soothe Indian dry skin conditions.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "Deep Nourishing Cold Cream with Vitamin E",
        "brand": "Joy / Nivea Soft",
        "category": "Moisturizer",
        "price_inr": 199.00,
        "target_skin_type": "Dry",
        "target_concerns": "Severe Dryness, Rough Texture",
        "key_ingredients": "Jojoba Oil, Vitamin E, Glycerin",
        "description": "High-value rich moisturizer for thirsty skin in need of immediate softness.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "Dewy Sunscreen SPF 50+ with Hyaluronic Acid",
        "brand": "Aqualogica Radiance+",
        "category": "Sunscreen",
        "price_inr": 399.00,
        "target_skin_type": "Dry",
        "target_concerns": "Sun Protection, Dehydration, Tanning",
        "key_ingredients": "Watermelon Extract, Hyaluronic Acid, UV Filters",
        "description": "Luminous dewy sun guard that quenches skin while deflecting intense UV radiation.",
        "budget_tier": "Budget",
        "usage_time": "AM"
    },

    # --- COMBINATION SKIN ---
    {
        "name": "Rice Water Bright Foaming Cleanser",
        "brand": "Dot & Key / Face Shop",
        "category": "Cleanser",
        "price_inr": 375.00,
        "target_skin_type": "Combination",
        "target_concerns": "Uneven Oil, Dullness, Large Pores",
        "key_ingredients": "Fermented Rice Water, Moringa Oil, Vitamin E",
        "description": "Harmonizes oily forehead and nose while pampering normal-to-dry cheek areas.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "Centella Asiatica Soothing Mist Toner",
        "brand": "Plum Cica",
        "category": "Toner",
        "price_inr": 380.00,
        "target_skin_type": "Combination",
        "target_concerns": "T-Zone Oil, Redness, Dehydrated Cheeks",
        "key_ingredients": "Cica Leaf Extract, Green Tea, Glycerin",
        "description": "Restores pH equilibrium across contrasting facial zones without sticky after-feel.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "Vitamin C 10% Glow & Radiance Serum",
        "brand": "Deconstruct",
        "category": "Serum",
        "price_inr": 599.00,
        "target_skin_type": "Combination",
        "target_concerns": "Pigmentation, Dark Spots, Uneven Tone",
        "key_ingredients": "10% Ethyl Ascorbic Acid, 0.5% Ferulic Acid",
        "description": "Fades tanning, dark spots, and dullness across the face while protecting against photo-damage.",
        "budget_tier": "Mid",
        "usage_time": "AM"
    },
    {
        "name": "Hydro Boost Water Gel Cream",
        "brand": "Neutrogena / Ponds Super Light",
        "category": "Moisturizer",
        "price_inr": 450.00,
        "target_skin_type": "Combination",
        "target_concerns": "Oiliness, Dehydration, Pores",
        "key_ingredients": "Hyaluronic Acid, Vitamin E, Amino Acids",
        "description": "Featherweight water gel that absorbs in seconds, providing ideal moisture to mixed zones.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "1% Hyaluronic Sunscreen Aqua Gel SPF 50 PA++++",
        "brand": "The Derma Co",
        "category": "Sunscreen",
        "price_inr": 499.00,
        "target_skin_type": "Combination",
        "target_concerns": "Sun Protection, Dark Spots, Greasiness",
        "key_ingredients": "1% Hyaluronic Acid, Vitamin E, Titanium Dioxide",
        "description": "Non-greasy, fragrance-free broad spectrum sunscreen that shields against UV and blue light.",
        "budget_tier": "Budget",
        "usage_time": "AM"
    },

    # --- NORMAL SKIN / HEALTHY BARRIER ---
    {
        "name": "Gentle Skin Cleanser for All Skin Types",
        "brand": "Cetaphil",
        "category": "Cleanser",
        "price_inr": 330.00,
        "target_skin_type": "Normal",
        "target_concerns": "Maintenance, Cleanliness",
        "key_ingredients": "Niacinamide, Panthenol, Glycerin",
        "description": "Dermatologist-recommended everyday gentle formula that respects the skin acid mantle.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "Rosewater & Aloe Vera Facial Toner",
        "brand": "Khadi Natural",
        "category": "Toner",
        "price_inr": 180.00,
        "target_skin_type": "Normal",
        "target_concerns": "Hydration, Freshness",
        "key_ingredients": "Pure Damask Rose Water, Aloe Barbadensis",
        "description": "Classic gentle botanical toner that balances and tightens skin naturally.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "10% Vitamin C + Niacinamide Brightening Serum",
        "brand": "Minimalist",
        "category": "Serum",
        "price_inr": 699.00,
        "target_skin_type": "Normal",
        "target_concerns": "Glow, Dark Spots, Preventive Care",
        "key_ingredients": "10% Vitamin C, 1% Centella, Bio-ferments",
        "description": "Antioxidant shield that imparts a lit-from-within clarity and youthful bounce.",
        "budget_tier": "Mid",
        "usage_time": "AM"
    },
    {
        "name": "Vitamin E Nourishing Daily Day Cream",
        "brand": "The Body Shop / Plum",
        "category": "Moisturizer",
        "price_inr": 480.00,
        "target_skin_type": "Normal",
        "target_concerns": "Hydration, Softness, Radiance",
        "key_ingredients": "Natural Vitamin E, Wheatgerm Oil, Raspberry Extract",
        "description": "Smooth everyday moisturizer locking in comfort and environmental defense.",
        "budget_tier": "Budget",
        "usage_time": "Both"
    },
    {
        "name": "Invisible Fluid Sunscreen SPF 50 PA++++",
        "brand": "Minimalist",
        "category": "Sunscreen",
        "price_inr": 399.00,
        "target_skin_type": "Normal",
        "target_concerns": "Sun Protection, Photoaging",
        "key_ingredients": "New Generation UV Filters, Aloe Water",
        "description": "Invisible, non-sticky sunscreen fluid designed for daily broad spectrum UV shield.",
        "budget_tier": "Budget",
        "usage_time": "AM"
    },

    # --- PIGMENTATION & DARK SPOTS SPECIALIZED ---
    {
        "name": "Alpha Arbutin 2% + Hyaluronic Acid Dark Spot Serum",
        "brand": "Minimalist",
        "category": "Serum",
        "price_inr": 549.00,
        "target_skin_type": "All",
        "target_concerns": "Pigmentation, Dark Spots, Melasma, Blemishes",
        "key_ingredients": "2% Alpha Arbutin, 1% Hyaluronic Acid",
        "description": "Clinically proven to inhibit tyrosinase activity, visibly reducing hyperpigmentation and brown spots.",
        "budget_tier": "Mid",
        "usage_time": "Both"
    },
    {
        "name": "Kojic Acid 2% Face Cream for Dark Spots",
        "brand": "The Derma Co",
        "category": "Moisturizer",
        "price_inr": 449.00,
        "target_skin_type": "All",
        "target_concerns": "Pigmentation, Dark Spots, Sun Spots",
        "key_ingredients": "2% Kojic Acid, 1% L-Ascorbic Acid, Niacinamide",
        "description": "Fades localized dark patches, post-inflammatory pigmentation, and age marks.",
        "budget_tier": "Budget",
        "usage_time": "PM"
    },
    {
        "name": "Glycolic Acid 8% Glowing Exfoliant Toner",
        "brand": "Minimalist",
        "category": "Toner",
        "price_inr": 499.00,
        "target_skin_type": "All",
        "target_concerns": "Pigmentation, Texture, Dullness",
        "key_ingredients": "8% Glycolic Acid, Bamboo Water",
        "description": "Resurfaces skin overnight, melting away discolored dead skin layers.",
        "budget_tier": "Budget",
        "usage_time": "PM"
    }
]

# Initialize default IDs for SEED_PRODUCTS
for _idx, _p in enumerate(SEED_PRODUCTS, start=1):
    if 'id' not in _p:
        _p['id'] = _idx


def generate_recommendations(skin_type, concerns, budget_limit=1000.0):
    """
    Intelligent recommendation engine:
    1. Selects core routine: Cleanser, Moisturizer, Sunscreen (essential 3 steps).
    2. If budget permits, adds targeted Treatment Serum or Toner for detected concerns.
    3. Respects total user budget (e.g. ₹500, ₹1000, ₹2000, ₹3000).
    4. Generates step-by-step AM and PM routine schedule.
    """
    budget_limit = float(budget_limit)
    concerns_lower = [c.lower() for c in concerns] if isinstance(concerns, list) else [concerns.lower()]

    # Filter candidate products suitable for this skin type or "All"
    candidates = []
    for p in SEED_PRODUCTS:
        p_skin = p['target_skin_type']
        if p_skin == skin_type or p_skin == 'All' or (skin_type == 'Combination' and p_skin in ['Oily', 'Normal']):
            # Calculate match score based on concern alignment
            score = 1.0
            p_concerns = p['target_concerns'].lower()
            for c in concerns_lower:
                if any(word in p_concerns for word in c.split()):
                    score += 2.0
            candidates.append({**p, 'relevance': score})

    # Group by category
    categories = ['Cleanser', 'Moisturizer', 'Sunscreen', 'Serum', 'Toner']
    cat_products = {cat: [] for cat in categories}
    for p in candidates:
        cat = p['category']
        if cat in cat_products:
            cat_products[cat].append(p)

    # Sort each category by relevance descending and price ascending
    for cat in categories:
        cat_products[cat].sort(key=lambda x: (-x['relevance'], x['price_inr']))

    # Mandatory products: Cleanser, Moisturizer, Sunscreen
    selected = []
    total_cost = 0.0

    # 1. Pick best Cleanser
    cleansers = cat_products.get('Cleanser', [])
    if cleansers:
        # If tight budget (<700), pick the cheapest high relevance
        if budget_limit <= 700:
            c = min(cleansers, key=lambda x: x['price_inr'])
        else:
            c = cleansers[0]
        selected.append(c)
        total_cost += c['price_inr']

    # 2. Pick best Moisturizer
    moisturizers = cat_products.get('Moisturizer', [])
    if moisturizers:
        if budget_limit <= 700:
            m = min(moisturizers, key=lambda x: x['price_inr'])
        else:
            m = moisturizers[0]
        selected.append(m)
        total_cost += m['price_inr']

    # 3. Pick Sunscreen (crucial for all dermatology advice)
    sunscreens = cat_products.get('Sunscreen', [])
    if sunscreens:
        if budget_limit <= 700:
            s = min(sunscreens, key=lambda x: x['price_inr'])
        else:
            s = sunscreens[0]
        selected.append(s)
        total_cost += s['price_inr']

    # 4. If budget allows, add targeted Serum
    serums = cat_products.get('Serum', [])
    if serums:
        best_serum = serums[0]
        if (total_cost + best_serum['price_inr'] <= budget_limit * 1.15) or len(selected) < 3:
            selected.append(best_serum)
            total_cost += best_serum['price_inr']

    # 5. If budget still has room, add Toner
    toners = cat_products.get('Toner', [])
    if toners and (total_cost + toners[0]['price_inr'] <= budget_limit * 1.15):
        selected.append(toners[0])
        total_cost += toners[0]['price_inr']

    # Sync IDs with database if accessible
    try:
        from database import db_manager
        db_items = db_manager.get_all_products()
        name_id_map = {item['name']: item['id'] for item in db_items}
        for prod in selected:
            if prod['name'] in name_id_map:
                prod['id'] = name_id_map[prod['name']]
    except Exception:
        pass

    # Generate personalized routine
    routine = generate_routine_schedule(skin_type, concerns, selected)

    return {
        "products": selected,
        "total_cost": round(total_cost, 2),
        "budget_limit": budget_limit,
        "within_budget": total_cost <= budget_limit,
        "routine": routine
    }


def generate_routine_schedule(skin_type, concerns, products):
    """Generates structured AM (Morning) & PM (Night) routines with clinical step instructions."""
    am_steps = []
    pm_steps = []

    # Map product categories to steps
    cleansers = [p for p in products if p['category'] == 'Cleanser']
    toners = [p for p in products if p['category'] == 'Toner']
    serums = [p for p in products if p['category'] == 'Serum']
    moisturizers = [p for p in products if p['category'] == 'Moisturizer']
    sunscreens = [p for p in products if p['category'] == 'Sunscreen']

    # AM Routine
    step_num = 1
    if cleansers:
        am_steps.append({
            "step": step_num,
            "phase": "Cleanse",
            "name": cleansers[0]['name'],
            "brand": cleansers[0]['brand'],
            "instructions": "Wash face with lukewarm water. Massage gently in circular motions for 45-60 seconds, then pat dry with a clean towel.",
            "tip": "Avoid harsh scrubbing on active blemishes."
        })
        step_num += 1

    if toners and toners[0].get('usage_time') in ['AM', 'Both']:
        am_steps.append({
            "step": step_num,
            "phase": "Tone & Hydrate",
            "name": toners[0]['name'],
            "brand": toners[0]['brand'],
            "instructions": "Gently pat into skin using clean palms. Do not rub with cotton pads.",
            "tip": "Apply to slightly damp skin for maximal penetration."
        })
        step_num += 1

    if serums and serums[0].get('usage_time') in ['AM', 'Both']:
        am_steps.append({
            "step": step_num,
            "phase": "Target & Treat",
            "name": serums[0]['name'],
            "brand": serums[0]['brand'],
            "instructions": "Dispense 3-4 drops directly onto face. Press gently into forehead, cheeks, and neck.",
            "tip": "Vitamin C / Niacinamide boosts your skin's daytime environmental defense."
        })
        step_num += 1

    if moisturizers:
        am_steps.append({
            "step": step_num,
            "phase": "Moisturize & Lock",
            "name": moisturizers[0]['name'],
            "brand": moisturizers[0]['brand'],
            "instructions": "Apply a dime-sized amount evenly to seal hydration and protect skin barrier.",
            "tip": "Let absorb for 2 minutes before applying sunscreen."
        })
        step_num += 1

    if sunscreens:
        am_steps.append({
            "step": step_num,
            "phase": "Sun Protection (Essential)",
            "name": sunscreens[0]['name'],
            "brand": sunscreens[0]['brand'],
            "instructions": "Apply the 'two-finger rule' amount generously 15 minutes before stepping into daylight.",
            "tip": "Reapply every 2-3 hours if sweating or outdoors."
        })

    # PM Routine
    step_num = 1
    if cleansers:
        pm_steps.append({
            "step": step_num,
            "phase": "Purify & Wash",
            "name": cleansers[0]['name'],
            "brand": cleansers[0]['brand'],
            "instructions": "Thoroughly cleanse away environmental pollution, sunscreen, and excess sebum accumulated throughout the day.",
            "tip": "Double cleanse if wearing heavy makeup or waterproof sunscreen."
        })
        step_num += 1

    if toners and toners[0].get('usage_time') in ['PM', 'Both']:
        pm_steps.append({
            "step": step_num,
            "phase": "Exfoliate & Tone",
            "name": toners[0]['name'],
            "brand": toners[0]['brand'],
            "instructions": "Apply gently to rebalance dermal pH and encourage cellular turnover overnight.",
            "tip": "If using AHA/BHA chemical exfoliants, limit to 2-3 nights per week initially."
        })
        step_num += 1

    if serums:
        pm_steps.append({
            "step": step_num,
            "phase": "Active Repair Treatment",
            "name": serums[0]['name'],
            "brand": serums[0]['brand'],
            "instructions": "Apply 3-4 drops across face. Night is the peak dermal repair cycle for active ingredients.",
            "tip": "Target areas with visible dark spots, acne marks, or hyperpigmentation."
        })
        step_num += 1

    if moisturizers:
        pm_steps.append({
            "step": step_num,
            "phase": "Barrier Recovery Cream",
            "name": moisturizers[0]['name'],
            "brand": moisturizers[0]['brand'],
            "instructions": "Apply a generous layer to nourish skin cells and prevent trans-epidermal water loss (TEWL) during sleep.",
            "tip": "Ensure pillowcase is clean cotton or satin to reduce nocturnal friction."
        })

    return {
        "morning": am_steps,
        "night": pm_steps
    }
