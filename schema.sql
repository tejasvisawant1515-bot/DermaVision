-- DermaVisionAI Database Schema
-- Compatible with MySQL 5.7+, MySQL 8.0+, MariaDB, and phpMyAdmin

CREATE DATABASE IF NOT EXISTS `dermavision_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `dermavision_db`;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `full_name` VARCHAR(100) NOT NULL,
    `age` INT DEFAULT NULL,
    `gender` VARCHAR(20) DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Products Table
CREATE TABLE IF NOT EXISTS `products` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(150) NOT NULL,
    `brand` VARCHAR(100) NOT NULL,
    `category` VARCHAR(50) NOT NULL, -- Cleanser, Toner, Serum, Moisturizer, Sunscreen
    `price_inr` DECIMAL(10, 2) NOT NULL,
    `target_skin_type` VARCHAR(50) NOT NULL, -- Oily, Dry, Normal, Combination, All
    `target_concerns` VARCHAR(255) NOT NULL, -- Acne, Pigmentation, Dark Spots, Redness, etc.
    `key_ingredients` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `image_url` VARCHAR(255) DEFAULT NULL,
    `budget_tier` VARCHAR(30) NOT NULL, -- Budget (<=500), Mid (501-1200), Premium (>1200)
    `usage_time` VARCHAR(30) NOT NULL DEFAULT 'Both', -- AM, PM, Both
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Analysis History Table
CREATE TABLE IF NOT EXISTS `analysis_history` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT DEFAULT NULL,
    `original_image` VARCHAR(255) NOT NULL,
    `analyzed_image` VARCHAR(255) DEFAULT NULL,
    `skin_type` VARCHAR(50) NOT NULL,
    `primary_concerns` VARCHAR(255) NOT NULL,
    `sebum_score` FLOAT DEFAULT 0.0,
    `acne_score` FLOAT DEFAULT 0.0,
    `pigmentation_score` FLOAT DEFAULT 0.0,
    `dark_spots_score` FLOAT DEFAULT 0.0,
    `texture_score` FLOAT DEFAULT 0.0,
    `redness_score` FLOAT DEFAULT 0.0,
    `selected_budget` DECIMAL(10, 2) DEFAULT 1000.00,
    `recommended_products_json` LONGTEXT,
    `routine_json` LONGTEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. User Delivery Addresses Table
CREATE TABLE IF NOT EXISTS `addresses` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT DEFAULT NULL,
    `full_name` VARCHAR(100) NOT NULL,
    `phone` VARCHAR(20) NOT NULL,
    `address_line1` VARCHAR(255) NOT NULL,
    `address_line2` VARCHAR(255) DEFAULT '',
    `city` VARCHAR(100) NOT NULL,
    `state` VARCHAR(100) NOT NULL,
    `pincode` VARCHAR(20) NOT NULL,
    `is_default` INT DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Shopping Cart Items Table
CREATE TABLE IF NOT EXISTS `cart_items` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT DEFAULT NULL,
    `session_id` VARCHAR(100) DEFAULT NULL,
    `product_id` INT NOT NULL,
    `quantity` INT DEFAULT 1,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`product_id`) REFERENCES `products`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Orders and Online Payment Table
CREATE TABLE IF NOT EXISTS `orders` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `order_number` VARCHAR(50) NOT NULL UNIQUE,
    `user_id` INT DEFAULT NULL,
    `delivery_name` VARCHAR(100) NOT NULL,
    `delivery_phone` VARCHAR(20) NOT NULL,
    `delivery_address` TEXT NOT NULL,
    `delivery_city` VARCHAR(100) NOT NULL,
    `delivery_state` VARCHAR(100) NOT NULL,
    `delivery_pincode` VARCHAR(20) NOT NULL,
    `subtotal` DECIMAL(10, 2) NOT NULL,
    `shipping_fee` DECIMAL(10, 2) DEFAULT 0.00,
    `discount` DECIMAL(10, 2) DEFAULT 0.00,
    `total_amount` DECIMAL(10, 2) NOT NULL,
    `payment_method` VARCHAR(50) NOT NULL, -- UPI, Credit/Debit Card, Net Banking, COD
    `payment_status` VARCHAR(30) DEFAULT 'Paid', -- Paid, Pending, Failed
    `payment_id` VARCHAR(100) DEFAULT NULL,
    `order_status` VARCHAR(30) DEFAULT 'Confirmed', -- Confirmed, Processing, Shipped, Delivered
    `items_json` LONGTEXT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==========================================================
-- SEED DATA: High-Quality Skincare Products Catalog in INR ₹
-- ==========================================================

INSERT INTO `products` (`name`, `brand`, `category`, `price_inr`, `target_skin_type`, `target_concerns`, `key_ingredients`, `description`, `budget_tier`, `usage_time`) VALUES
-- Oily & Acne-Prone
('Salicylic Acid 2% Gentle Foaming Cleanser', 'The Derma Co', 'Cleanser', 349.00, 'Oily', 'Acne, Blackheads, Enlarged Pores', '2% Salicylic Acid, Witch Hazel, Allantoin', 'Deeply unclogs pores and washes away excess sebum without stripping moisture.', 'Budget', 'Both'),
('Aha Bha 10% Clarifying Toner', 'Minimalist', 'Toner', 399.00, 'Oily', 'Acne, Texture, Clogged Pores', 'Glycolic Acid, Salicylic Acid, Aloe Vera', 'Exfoliates dead skin cells, clears congested pores, and balances oil production.', 'Budget', 'PM'),
('Niacinamide 10% + Zinc 1% Serum', 'Minimalist', 'Serum', 599.00, 'Oily', 'Acne, Sebum, Pigmentation, Blemishes', '10% Niacinamide, 1% Zinc PCA, Aloe Barbadensis Leaf Juice', 'Regulates sebum secretion, reduces blemishes, and visibly shrinks pore size.', 'Mid', 'Both'),
('Oil-Free Mattifying Gel Moisturizer', 'Plum Green Tea', 'Moisturizer', 470.00, 'Oily', 'Acne, Oiliness', 'Green Tea Extract, Niacinamide, Hyaluronic Acid', 'Ultra-lightweight oil-free hydration with green tea antioxidants to fight acne bacteria.', 'Budget', 'Both'),
('Ultra-Matte Dry Touch Sunscreen Gel SPF 50 PA++++', 'Re\'equil', 'Sunscreen', 780.00, 'Oily', 'Sun Protection, Acne Prevention', 'Hybrid UV Filters, Physalis Angulata Extract', 'Velvet matte finish that prevents sweat and oil build-up with zero white cast.', 'Mid', 'AM'),

-- Dry & Dehydrated Skin
('Hydrating Cream-to-Foam Gentle Cleanser', 'CeraVe / Dot & Key', 'Cleanser', 395.00, 'Dry', 'Dryness, Flakiness, Sensitive Barrier', '3 Essential Ceramides, Hyaluronic Acid, Amino Acids', 'Cleanses and hydrates the skin barrier without disrupting the natural moisture balance.', 'Budget', 'Both'),
('Rosewater & Polyglutamic Acid Hydrating Toner', 'Simple Kind To Skin', 'Toner', 320.00, 'Dry', 'Dryness, Tightness, Dullness', 'Pro-Vitamin B5, Chamomile, Allantoin', 'Instantly restores pH balance and quenches dehydrated skin cells.', 'Budget', 'Both'),
('Hyaluronic Acid 2% + Polyglutamic Acid Plumping Serum', 'Minimalist', 'Serum', 599.00, 'Dry', 'Dehydration, Fine Lines, Dullness', 'Multi-Molecular Hyaluronic Acid, Polyglutamic Acid', 'Pulls moisture deep into skin layers, restoring plump elasticity and dewy glow.', 'Mid', 'Both'),
('Ceramide & Hyaluronic Acid Barrier Repair Cream', 'Dr. Sheth\'s', 'Moisturizer', 499.00, 'Dry', 'Dryness, Damaged Barrier, Flaking', '1% Ceramide Complex, Vitamin E, Shea Butter', 'Fortifies weakened skin lipid layers, offering 72-hour deep nourishment.', 'Budget', 'Both'),
('Dewy Sunscreen SPF 50+ with Hyaluronic Acid & Watermelon', 'Aqualogica', 'Sunscreen', 449.00, 'Dry', 'Sun Protection, Dehydration', 'Titanium Dioxide, Zinc Oxide, Watermelon Extracts, Hyaluronic Acid', 'Ultra-moisturizing sun screen with fresh dewy finish and intense UV defense.', 'Budget', 'AM'),

-- Combination Skin (T-zone oily, cheeks normal/dry)
('Rice Water & Niacinamide Balancing Foaming Face Wash', 'The Face Shop / Dot & Key', 'Cleanser', 380.00, 'Combination', 'Uneven Oil, Dullness, Pores', 'Rice Water Extract, Niacinamide, Soapwort', 'Harmonizes oil across the forehead and nose while pampering dry cheek zones.', 'Budget', 'Both'),
('Centella Asiatica (Cica) Calming Hydrating Mist Toner', 'Plum Cica & Hyaluronic', 'Toner', 390.00, 'Combination', 'Redness, Uneven Texture', 'Cica Leaf Water, Green Tea, Glycerin', 'Soothes inflammation on the T-zone while hydrating normal cheek contours.', 'Budget', 'Both'),
('Vitamin C 10% Glow & Spot Reduction Serum', 'Deconstruct', 'Serum', 699.00, 'Combination', 'Pigmentation, Dark Spots, Uneven Tone', '10% 3-O-Ethyl Ascorbic Acid, 0.5% Ferulic Acid', 'Brightens stubborn hyperpigmentation and shields against oxidative environmental stress.', 'Mid', 'AM'),
('Light Gel-Cream Balancing Moisturizer with Hyaluronic Acid', 'Neutrogena Hydro Boost', 'Moisturizer', 850.00, 'Combination', 'Dehydration, Oil Control', 'Hyaluronic Acid, Trehalose, Olive Extract', 'Water-like cooling gel that absorbs instantly without greasy residue.', 'Mid', 'Both'),
('Clear Water-Fluid Sunscreen SPF 50 PA+++', 'The Derma Co 1% Hyaluronic', 'Sunscreen', 499.00, 'Combination', 'Sun Protection, Dark Spots', 'Hyaluronic Acid, Vitamin E, UV Filters', 'Lightweight fluid sunscreen that leaves zero oily sheen on T-zone.', 'Budget', 'AM'),

-- Normal Skin & Anti-Aging / Glow
('Gentle Skin Cleanser', 'Cetaphil', 'Cleanser', 330.00, 'Normal', 'Daily Maintenance, Cleanliness', 'Niacinamide, Panthenol, Hydrating Glycerin', 'Clinically proven gentle non-irritating formula for maintaining healthy skin balance.', 'Budget', 'Both'),
('Rosehip & Squalane Restorative Face Elixir', 'Suganda', 'Serum', 750.00, 'Normal', 'Glow, Radiance, Texture', 'Pure Plant Squalane, Rosehip Seed Oil', 'Restores natural radiance, softness, and resilience to well-balanced skin.', 'Mid', 'PM'),
('Daily Vitamin Vitamin E Hydrating Moisturizer', 'The Body Shop / Plum', 'Moisturizer', 550.00, 'Normal', 'Hydration, Vitality', 'Vitamin E, Wheatgerm Oil, Bio-Ferments', 'Protects against environmental pollution while maintaining smooth all-day bounce.', 'Mid', 'Both'),
('Fluid Sunscreen SPF 50 PA++++', 'Bake Beauty / Minimalist', 'Sunscreen', 399.00, 'Normal', 'UV Protection, Photoaging', 'Broad Spectrum Filters, Aloe Vera Extract', 'Feather-light daily sunscreen protecting against UVA/UVB rays.', 'Budget', 'AM'),

-- Pigmentation, Dark Spots & Melasma Special Focus
('Alpha Arbutin 2% + Kojic Acid Dark Spot Serum', 'Minimalist', 'Serum', 549.00, 'All', 'Pigmentation, Dark Spots, Melasma', '2% Alpha Arbutin, 1% Kojic Acid, Hyaluronic Acid', 'Potent depigmenting active that reduces melanin synthesis and evens stubborn discoloration.', 'Mid', 'Both'),
('Tranexamic 3% Overnight Dark Spot Corrector', 'Minimalist / Foxtale', 'Serum', 649.00, 'All', 'Pigmentation, Post-Acne Marks, PIH', '3% Tranexamic Acid, Mandelic Acid, Hydroxyphenoxy Propionic Acid', 'Targeted treatment for post-inflammatory erythema and melasma.', 'Mid', 'PM'),
('Glycolic Acid 8% Glowing Exfoliating Toner', 'Minimalist', 'Toner', 499.00, 'All', 'Dullness, Dark Spots, Roughness', '8% Glycolic Acid, Bamboo Water', 'Loosens dead hyperpigmented epidermal cells to unveil luminous skin beneath.', 'Budget', 'PM'),

-- Budget-Friendly Complete Routine Picks (< ₹500 individual products)
('Charcoal Detox Pore Cleanser', 'Garnier Men / Himalaya Herbals', 'Cleanser', 199.00, 'Oily', 'Excess Sebum, Dirt, Blackheads', 'Activated Charcoal, Tea Tree Oil, Menthol', 'Absorbs grime and clarifies oily pores affordably.', 'Budget', 'Both'),
('Purifying Neem Face Wash', 'Himalaya Herbals', 'Cleanser', 160.00, 'Oily', 'Acne, Pimples, Redness', 'Neem Leaf Extract, Turmeric', 'Ancient herbal formula that prevents recurring pimples and soothes inflammation.', 'Budget', 'Both'),
('Purifying Aloe Vera Moisturizing Gel', 'Khadi Natural / WOW', 'Moisturizer', 249.00, 'All', 'Mild Dryness, Redness', '99% Pure Organic Aloe Vera, Vitamin E', 'Refreshing non-sticky soothing hydration for sensitive or irritated skin.', 'Budget', 'Both'),
('Matte Finish Daily Sunscreen SPF 30', 'Joy Revivify / Lotus Herbals', 'Sunscreen', 275.00, 'All', 'Sun Protection, Tanning', 'Carrot Seed Oil, Zinc Oxide', 'Reliable daily protection against sun tanning and pigmentation on a budget.', 'Budget', 'AM');
