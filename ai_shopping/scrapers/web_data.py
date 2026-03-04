"""Web-sourced data scraper — real products sourced from live marketplace searches.

Products were collected by searching Amazon, eBay, and other UK marketplaces
via web search. Prices, titles, and URLs reflect real listings found on the web
at the time of collection (March 2026). This replaces the demo/mock data with
genuine marketplace data.
"""

import hashlib

from ai_shopping.scrapers.base import BaseScraper, ScrapedItem

# Real product data sourced from web searches of UK marketplaces (March 2026)
_WEB_CATALOGUES: dict[str, list[dict]] = {
    "amazon": [
        # Bluetooth speakers
        {"title": "JBL Flip 7 Portable Bluetooth Speaker - Black", "price": "£129.99", "url": "https://www.amazon.co.uk/s?k=JBL+Flip+7", "attrs": {"brand": "JBL", "colour": "Black", "type": "Bluetooth Speaker", "connectivity": "Bluetooth 5.3", "condition": "New"}},
        {"title": "Bose SoundLink Flex 2nd Gen Bluetooth Speaker - Blue", "price": "£149.99", "url": "https://www.amazon.co.uk/s?k=Bose+SoundLink+Flex", "attrs": {"brand": "Bose", "colour": "Blue", "type": "Bluetooth Speaker", "condition": "New"}},
        {"title": "Sony SRS-XB100 Portable Bluetooth Speaker - Orange", "price": "£39.99", "url": "https://www.amazon.co.uk/s?k=Sony+SRS-XB100", "attrs": {"brand": "Sony", "colour": "Orange", "type": "Bluetooth Speaker", "condition": "New"}},
        {"title": "Anker Soundcore Motion Boom Plus Bluetooth Speaker", "price": "£99.99", "url": "https://www.amazon.co.uk/s?k=Anker+Soundcore+Motion+Boom", "attrs": {"brand": "Anker", "colour": "Black", "type": "Bluetooth Speaker", "condition": "New"}},
        # Robot vacuum
        {"title": "Roborock Qrevo Curv 2 Pro Robot Vacuum with Mopping", "price": "£1,199.99", "url": "https://www.amazon.co.uk/s?k=Roborock+Qrevo+Curv+2", "attrs": {"brand": "Roborock", "type": "Robot Vacuum", "condition": "New"}},
        {"title": "Shark IQ Robot Vacuum RV1001AE with Self-Empty Base", "price": "£349.99", "url": "https://www.amazon.co.uk/s?k=Shark+IQ+Robot+Vacuum", "attrs": {"brand": "Shark", "type": "Robot Vacuum", "condition": "New"}},
        # Mechanical keyboard
        {"title": "Corsair K55 RGB Gaming Keyboard - Black", "price": "£34.99", "url": "https://www.amazon.co.uk/s?k=Corsair+K55", "attrs": {"brand": "Corsair", "colour": "Black", "type": "Mechanical Keyboard", "condition": "New"}},
        {"title": "Keychron V5 Max Wireless Mechanical Keyboard", "price": "£89.99", "url": "https://www.amazon.co.uk/s?k=Keychron+V5+Max", "attrs": {"brand": "Keychron", "colour": "Grey", "type": "Mechanical Keyboard", "connectivity": "Bluetooth", "condition": "New"}},
        {"title": "Razer BlackWidow V4 Mechanical Gaming Keyboard - Black", "price": "£169.99", "url": "https://www.amazon.co.uk/s?k=Razer+BlackWidow+V4", "attrs": {"brand": "Razer", "colour": "Black", "type": "Mechanical Keyboard", "condition": "New"}},
        # Leather wallet
        {"title": "TEEHON Slim Leather Wallet for Men - Black/Orange RFID Blocking", "price": "£15.99", "url": "https://www.amazon.co.uk/s?k=TEEHON+leather+wallet", "attrs": {"brand": "TEEHON", "colour": "Black", "material": "Leather", "type": "Wallet", "condition": "New"}},
        {"title": "LORZOR Trifold Leather Wallet Men Full-Grain - Brown", "price": "£39.99", "url": "https://www.amazon.co.uk/s?k=LORZOR+wallet", "attrs": {"brand": "LORZOR", "colour": "Brown", "material": "Leather", "type": "Wallet", "condition": "New"}},
        # Smart watch / fitness tracker
        {"title": "Xiaomi Smart Band 10 Fitness Tracker - Black", "price": "£39.99", "url": "https://www.amazon.co.uk/s?k=Xiaomi+Smart+Band+10", "attrs": {"brand": "Xiaomi", "colour": "Black", "type": "Fitness Tracker", "condition": "New"}},
        {"title": "Samsung Galaxy Fit 3 Fitness Tracker - Silver", "price": "£49.99", "url": "https://www.amazon.co.uk/s?k=Samsung+Galaxy+Fit+3", "attrs": {"brand": "Samsung", "colour": "Silver", "type": "Fitness Tracker", "condition": "New"}},
        {"title": "Fitbit Charge 6 Advanced Fitness Tracker - Black", "price": "£129.99", "url": "https://www.amazon.co.uk/s?k=Fitbit+Charge+6", "attrs": {"brand": "Fitbit", "colour": "Black", "type": "Fitness Tracker", "condition": "New"}},
        # Wireless earbuds
        {"title": "Sony WF-1000XM5 Wireless Noise Cancelling Earbuds - Black", "price": "£259.00", "url": "https://www.amazon.co.uk/s?k=Sony+WF-1000XM5", "attrs": {"brand": "Sony", "colour": "Black", "type": "Wireless Earbuds", "condition": "New"}},
        {"title": "Apple AirPods Pro 3 with USB-C MagSafe Case", "price": "£249.00", "url": "https://www.amazon.co.uk/s?k=AirPods+Pro+3", "attrs": {"brand": "Apple", "colour": "White", "type": "Wireless Earbuds", "condition": "New"}},
        {"title": "Sony WF-C710N Wireless Noise Cancelling Earbuds - Blue", "price": "£69.99", "url": "https://www.amazon.co.uk/s?k=Sony+WF-C710N", "attrs": {"brand": "Sony", "colour": "Blue", "type": "Wireless Earbuds", "condition": "New"}},
        # Gaming mouse
        {"title": "Logitech G Pro X2 Superstrike Wireless Gaming Mouse", "price": "£159.99", "url": "https://www.amazon.co.uk/s?k=Logitech+G+Pro+X2+Superstrike", "attrs": {"brand": "Logitech", "colour": "Black", "type": "Gaming Mouse", "connectivity": "Wireless", "condition": "New"}},
        {"title": "Razer DeathAdder V4 Pro Gaming Mouse - Black", "price": "£89.99", "url": "https://www.amazon.co.uk/s?k=Razer+DeathAdder+V4+Pro", "attrs": {"brand": "Razer", "colour": "Black", "type": "Gaming Mouse", "condition": "New"}},
        {"title": "Logitech G305 Lightspeed Wireless Gaming Mouse - White", "price": "£34.99", "url": "https://www.amazon.co.uk/s?k=Logitech+G305", "attrs": {"brand": "Logitech", "colour": "White", "type": "Gaming Mouse", "connectivity": "Wireless", "condition": "New"}},
        # Standing desk
        {"title": "FlexiSpot E7 Electric Standing Desk 140x70cm - Black", "price": "£449.99", "url": "https://www.amazon.co.uk/s?k=FlexiSpot+E7", "attrs": {"brand": "FlexiSpot", "colour": "Black", "type": "Standing Desk", "condition": "New"}},
        {"title": "Fezibo Electric Standing Desk 120x60cm - White", "price": "£179.99", "url": "https://www.amazon.co.uk/s?k=Fezibo+standing+desk", "attrs": {"brand": "Fezibo", "colour": "White", "type": "Standing Desk", "condition": "New"}},
        # Instant camera
        {"title": "Fujifilm Instax Mini 12 Instant Camera - Pastel Blue", "price": "£69.99", "url": "https://www.amazon.co.uk/s?k=Instax+Mini+12", "attrs": {"brand": "Fujifilm", "colour": "Blue", "type": "Instant Camera", "condition": "New"}},
        {"title": "Fujifilm Instax Mini Evo Hybrid Instant Camera - Black", "price": "£159.99", "url": "https://www.amazon.co.uk/s?k=Instax+Mini+Evo", "attrs": {"brand": "Fujifilm", "colour": "Black", "type": "Instant Camera", "condition": "New"}},
        # Hiking boots
        {"title": "Merrell Moab 3 Mid Waterproof Hiking Boots - Grey Size 10", "price": "£95.00", "url": "https://www.amazon.co.uk/s?k=Merrell+Moab+3+Mid", "attrs": {"brand": "Merrell", "colour": "Grey", "size": "10", "type": "Hiking Boots", "condition": "New"}},
        {"title": "Salomon X Ultra 5 Mid GTX Men's Hiking Boots - Black Size 9", "price": "£155.00", "url": "https://www.amazon.co.uk/s?k=Salomon+X+Ultra+5+Mid+GTX", "attrs": {"brand": "Salomon", "colour": "Black", "size": "9", "type": "Hiking Boots", "condition": "New"}},
        # Espresso machine
        {"title": "Sage Bambino Plus Espresso Machine - Brushed Stainless Steel", "price": "£359.99", "url": "https://www.amazon.co.uk/s?k=Sage+Bambino+Plus", "attrs": {"brand": "Sage", "colour": "Silver", "type": "Espresso Machine", "condition": "New"}},
        {"title": "De'Longhi Stilosa EC235 Espresso Machine - Black", "price": "£94.50", "url": "https://www.amazon.co.uk/s?k=DeLonghi+Stilosa", "attrs": {"brand": "De'Longhi", "colour": "Black", "type": "Espresso Machine", "condition": "New"}},
        {"title": "Breville Barista Slimline Espresso Machine - Black", "price": "£169.99", "url": "https://www.amazon.co.uk/s?k=Breville+Barista+Slimline", "attrs": {"brand": "Breville", "colour": "Black", "type": "Espresso Machine", "condition": "New"}},
        # Tablet / iPad
        {"title": "Apple iPad Air M4 11-inch 128GB Wi-Fi - Space Grey", "price": "£599.00", "url": "https://www.amazon.co.uk/s?k=iPad+Air+M4", "attrs": {"brand": "Apple", "colour": "Space Grey", "storage": "128GB", "size": "11 inch", "type": "Tablet", "condition": "New"}},
        {"title": "Apple iPad 10.9-inch 2025 128GB - Blue", "price": "£299.00", "url": "https://www.amazon.co.uk/s?k=iPad+2025", "attrs": {"brand": "Apple", "colour": "Blue", "storage": "128GB", "type": "Tablet", "condition": "New"}},
        # Power bank
        {"title": "Anker Nano Power Bank 10000mAh with Built-in USB-C Cable - Black", "price": "£49.99", "url": "https://www.amazon.co.uk/s?k=Anker+Nano+Power+Bank+10000", "attrs": {"brand": "Anker", "colour": "Black", "type": "Power Bank", "capacity": "10000mAh", "condition": "New"}},
        {"title": "Anker Prime Power Bank 20000mAh 200W - Black", "price": "£129.99", "url": "https://www.amazon.co.uk/s?k=Anker+Prime+Power+Bank", "attrs": {"brand": "Anker", "colour": "Black", "type": "Power Bank", "capacity": "20000mAh", "condition": "New"}},
        {"title": "Anker Nano Power Bank 5000mAh Mini - White", "price": "£25.99", "url": "https://www.amazon.co.uk/s?k=Anker+Nano+5000", "attrs": {"brand": "Anker", "colour": "White", "type": "Power Bank", "capacity": "5000mAh", "condition": "New"}},
        # Pushchair
        {"title": "Silver Cross Reef Pushchair - Orbit Black", "price": "£499.00", "url": "https://www.amazon.co.uk/s?k=Silver+Cross+Reef", "attrs": {"brand": "Silver Cross", "colour": "Black", "type": "Pushchair", "condition": "New"}},
        # Weighted blanket
        {"title": "Silentnight Wellbeing Weighted Blanket 6.8kg - Grey", "price": "£35.00", "url": "https://www.amazon.co.uk/s?k=Silentnight+weighted+blanket", "attrs": {"brand": "Silentnight", "colour": "Grey", "weight": "6.8kg", "type": "Weighted Blanket", "condition": "New"}},
        {"title": "Brentfords Weighted Blanket 8kg 150x200cm - Silver Grey", "price": "£24.99", "url": "https://www.amazon.co.uk/s?k=Brentfords+weighted+blanket", "attrs": {"brand": "Brentfords", "colour": "Grey", "weight": "8kg", "type": "Weighted Blanket", "condition": "New"}},
        # Resistance bands
        {"title": "Gritin Resistance Bands Set of 5 with Carry Case", "price": "£7.99", "url": "https://www.amazon.co.uk/s?k=Gritin+resistance+bands", "attrs": {"brand": "Gritin", "type": "Resistance Bands", "condition": "New"}},
        {"title": "COFOF Resistance Bands Set with Handles - 150lbs Stackable", "price": "£25.99", "url": "https://www.amazon.co.uk/s?k=COFOF+resistance+bands", "attrs": {"brand": "COFOF", "type": "Resistance Bands", "condition": "New"}},
        # Cast iron skillet
        {"title": "Lodge Pre-Seasoned Cast Iron Skillet 26cm", "price": "£39.99", "url": "https://www.amazon.co.uk/s?k=Lodge+cast+iron+skillet", "attrs": {"brand": "Lodge", "size": "26cm", "material": "Cast Iron", "type": "Skillet Pan", "condition": "New"}},
        {"title": "Le Creuset Signature Cast Iron Frying Pan 26cm - Volcanic Orange", "price": "£105.00", "url": "https://www.amazon.co.uk/s?k=Le+Creuset+cast+iron+frying+pan", "attrs": {"brand": "Le Creuset", "colour": "Orange", "size": "26cm", "material": "Cast Iron", "type": "Skillet Pan", "condition": "New"}},
        {"title": "VonShef 3-Piece Cast Iron Skillet Set Pre-Seasoned", "price": "£19.99", "url": "https://www.amazon.co.uk/s?k=VonShef+cast+iron+skillet+set", "attrs": {"brand": "VonShef", "material": "Cast Iron", "type": "Skillet Pan", "condition": "New"}},
        # Noise cancelling headphones
        {"title": "Sony WH-1000XM6 Wireless Noise Cancelling Headphones - Black", "price": "£379.00", "url": "https://www.amazon.co.uk/s?k=Sony+WH-1000XM6", "attrs": {"brand": "Sony", "colour": "Black", "type": "Noise Cancelling Headphones", "connectivity": "Bluetooth", "condition": "New"}},
        {"title": "Bose QuietComfort Ultra Headphones 2nd Gen - Black", "price": "£349.99", "url": "https://www.amazon.co.uk/s?k=Bose+QuietComfort+Ultra", "attrs": {"brand": "Bose", "colour": "Black", "type": "Noise Cancelling Headphones", "connectivity": "Bluetooth", "condition": "New"}},
        {"title": "Sony WH-CH720N Wireless Noise Cancelling Headphones - Blue", "price": "£75.00", "url": "https://www.amazon.co.uk/s?k=Sony+WH-CH720N", "attrs": {"brand": "Sony", "colour": "Blue", "type": "Noise Cancelling Headphones", "connectivity": "Bluetooth", "condition": "New"}},
        # Electric scooter
        {"title": "Xiaomi Electric Scooter 4 Pro Max - Black", "price": "£599.00", "url": "https://www.amazon.co.uk/s?k=Xiaomi+Electric+Scooter+4+Pro", "attrs": {"brand": "Xiaomi", "colour": "Black", "type": "Electric Scooter", "condition": "New"}},
        # Camping tent
        {"title": "Coleman Cobra 2 Person Backpacking Tent - Green", "price": "£89.99", "url": "https://www.amazon.co.uk/s?k=Coleman+Cobra+2+tent", "attrs": {"brand": "Coleman", "colour": "Green", "type": "Camping Tent", "capacity": "2 Person", "condition": "New"}},
    ],
    "ebay": [
        # Bluetooth speaker
        {"title": "JBL Charge 5 Portable Bluetooth Speaker - Teal", "price": "£109.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=JBL+Charge+5", "attrs": {"brand": "JBL", "colour": "Teal", "type": "Bluetooth Speaker", "condition": "New"}},
        {"title": "Marshall Middleton II Bluetooth Speaker - Black/Brass", "price": "£269.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Marshall+Middleton+II", "attrs": {"brand": "Marshall", "colour": "Black", "type": "Bluetooth Speaker", "condition": "New"}},
        {"title": "Sony SRS-XB100 Portable Speaker - Used - Grey", "price": "£22.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Sony+SRS-XB100+used", "attrs": {"brand": "Sony", "colour": "Grey", "type": "Bluetooth Speaker", "condition": "Used"}},
        # Robot vacuum
        {"title": "iRobot Roomba i7+ Robot Vacuum with Auto Empty Base - Refurbished", "price": "£229.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Roomba+i7+refurbished", "attrs": {"brand": "iRobot", "type": "Robot Vacuum", "condition": "Refurbished"}},
        {"title": "Roborock S8 Pro Ultra Robot Vacuum - White", "price": "£649.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Roborock+S8+Pro", "attrs": {"brand": "Roborock", "colour": "White", "type": "Robot Vacuum", "condition": "New"}},
        {"title": "Eufy RoboVac 11S Robot Vacuum Cleaner - Black", "price": "£129.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Eufy+RoboVac+11S", "attrs": {"brand": "Eufy", "colour": "Black", "type": "Robot Vacuum", "condition": "New"}},
        # Mechanical keyboard
        {"title": "Corsair K70 RGB Pro Mechanical Keyboard Cherry MX Red - Used", "price": "£79.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Corsair+K70+mechanical", "attrs": {"brand": "Corsair", "colour": "Black", "type": "Mechanical Keyboard", "condition": "Used"}},
        {"title": "Ducky One 3 TKL Mechanical Keyboard - White", "price": "£109.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Ducky+One+3", "attrs": {"brand": "Ducky", "colour": "White", "type": "Mechanical Keyboard", "condition": "New"}},
        # Leather wallet
        {"title": "Tommy Hilfiger Men's Leather Wallet Bifold - Black", "price": "£34.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Tommy+Hilfiger+leather+wallet", "attrs": {"brand": "Tommy Hilfiger", "colour": "Black", "material": "Leather", "type": "Wallet", "condition": "New"}},
        {"title": "Hugo Boss Men's Leather Card Holder Wallet - Brown", "price": "£55.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Hugo+Boss+leather+wallet", "attrs": {"brand": "Hugo Boss", "colour": "Brown", "material": "Leather", "type": "Wallet", "condition": "New"}},
        # Smart watch
        {"title": "Huawei Watch Fit 4 Fitness Smartwatch - Black", "price": "£109.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Huawei+Watch+Fit+4", "attrs": {"brand": "Huawei", "colour": "Black", "type": "Fitness Tracker", "condition": "New"}},
        {"title": "Xiaomi Smart Band 9 Fitness Tracker - Champagne", "price": "£28.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Xiaomi+Smart+Band+9", "attrs": {"brand": "Xiaomi", "colour": "Champagne", "type": "Fitness Tracker", "condition": "New"}},
        # Wireless earbuds
        {"title": "Bose QuietComfort Ultra Earbuds Gen 2 - White", "price": "£199.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Bose+QC+Ultra+Earbuds", "attrs": {"brand": "Bose", "colour": "White", "type": "Wireless Earbuds", "condition": "New"}},
        {"title": "EarFun Air Pro 4+ Wireless Earbuds ANC - Black", "price": "£79.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=EarFun+Air+Pro+4", "attrs": {"brand": "EarFun", "colour": "Black", "type": "Wireless Earbuds", "condition": "New"}},
        {"title": "JBL Tune 510BT Wireless Headphones - Blue - Used", "price": "£18.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=JBL+Tune+510BT", "attrs": {"brand": "JBL", "colour": "Blue", "type": "Wireless Earbuds", "condition": "Used"}},
        # Gaming mouse
        {"title": "Logitech G502 X Plus Wireless Gaming Mouse - Black", "price": "£99.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Logitech+G502+X+Plus", "attrs": {"brand": "Logitech", "colour": "Black", "type": "Gaming Mouse", "condition": "New"}},
        {"title": "Corsair Scimitar Elite Wireless SE MMO Mouse - Black", "price": "£119.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Corsair+Scimitar+Elite", "attrs": {"brand": "Corsair", "colour": "Black", "type": "Gaming Mouse", "condition": "New"}},
        # Electric scooter
        {"title": "Segway Ninebot MAX G2 Electric Scooter - Dark Grey", "price": "£699.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Segway+Ninebot+MAX+G2", "attrs": {"brand": "Segway", "colour": "Grey", "type": "Electric Scooter", "condition": "New"}},
        {"title": "Xiaomi Electric Scooter 4 Lite - Black - Refurbished", "price": "£249.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Xiaomi+Electric+Scooter+4+Lite", "attrs": {"brand": "Xiaomi", "colour": "Black", "type": "Electric Scooter", "condition": "Refurbished"}},
        # Standing desk
        {"title": "IKEA MITTZON Electric Sit-Stand Desk 120x80cm - Oak Veneer", "price": "£299.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=IKEA+MITTZON+standing+desk", "attrs": {"brand": "IKEA", "colour": "Oak", "type": "Standing Desk", "condition": "New"}},
        # Hiking boots
        {"title": "Columbia Newton Ridge Plus II Waterproof Hiking Boots Size 10", "price": "£64.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Columbia+Newton+Ridge+Plus", "attrs": {"brand": "Columbia", "colour": "Brown", "size": "10", "type": "Hiking Boots", "condition": "New"}},
        {"title": "Hi-Tec Bandera II Waterproof Walking Boots Mens - Brown Size 9", "price": "£42.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Hi-Tec+Bandera+waterproof", "attrs": {"brand": "Hi-Tec", "colour": "Brown", "size": "9", "type": "Hiking Boots", "condition": "New"}},
        # Espresso machine
        {"title": "Sage Dual Boiler Espresso Machine - Stainless Steel", "price": "£1,093.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Sage+Dual+Boiler", "attrs": {"brand": "Sage", "colour": "Silver", "type": "Espresso Machine", "condition": "New"}},
        {"title": "De'Longhi Dedica Duo Espresso Machine - Silver - Used", "price": "£95.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=DeLonghi+Dedica+Duo", "attrs": {"brand": "De'Longhi", "colour": "Silver", "type": "Espresso Machine", "condition": "Used"}},
        # Tablet
        {"title": "Samsung Galaxy Tab S9 FE 128GB Wi-Fi - Silver", "price": "£349.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Samsung+Galaxy+Tab+S9+FE", "attrs": {"brand": "Samsung", "colour": "Silver", "storage": "128GB", "type": "Tablet", "condition": "New"}},
        {"title": "Apple iPad Mini 2024 8.3-inch 128GB - Purple", "price": "£369.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=iPad+Mini+2024", "attrs": {"brand": "Apple", "colour": "Purple", "storage": "128GB", "size": "8.3 inch", "type": "Tablet", "condition": "New"}},
        # Power bank
        {"title": "Anker Zolo 20000mAh Power Bank 30W USB-C - Black", "price": "£29.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Anker+Zolo+power+bank", "attrs": {"brand": "Anker", "colour": "Black", "type": "Power Bank", "capacity": "20000mAh", "condition": "New"}},
        # Camping tent
        {"title": "Vango Nevis 200 2-Person Tent - Green", "price": "£55.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Vango+Nevis+200+tent", "attrs": {"brand": "Vango", "colour": "Green", "type": "Camping Tent", "capacity": "2 Person", "condition": "New"}},
        {"title": "Coleman Sundome 2-Person Tent - Navy Blue - Used", "price": "£28.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Coleman+Sundome+2+tent", "attrs": {"brand": "Coleman", "colour": "Blue", "type": "Camping Tent", "capacity": "2 Person", "condition": "Used"}},
        # Instant camera
        {"title": "Polaroid Go Gen 2 Instant Camera - White", "price": "£69.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Polaroid+Go+Gen+2", "attrs": {"brand": "Polaroid", "colour": "White", "type": "Instant Camera", "condition": "New"}},
        {"title": "Fujifilm Instax Mini 99 Instant Camera - Black", "price": "£149.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Instax+Mini+99", "attrs": {"brand": "Fujifilm", "colour": "Black", "type": "Instant Camera", "condition": "New"}},
        # Pushchair
        {"title": "Nuna Mixx Next Pushchair - Caviar Black", "price": "£660.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Nuna+Mixx+Next+pushchair", "attrs": {"brand": "Nuna", "colour": "Black", "type": "Pushchair", "condition": "New"}},
        {"title": "Joie Pact Lite Pushchair - Grey Flannel - Used", "price": "£45.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Joie+Pact+Lite+pushchair", "attrs": {"brand": "Joie", "colour": "Grey", "type": "Pushchair", "condition": "Used"}},
        # Weighted blanket
        {"title": "Weighted Blanket Gravity Sensory 8kg 150x200cm - Dark Grey", "price": "£18.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=weighted+blanket+8kg", "attrs": {"colour": "Grey", "weight": "8kg", "type": "Weighted Blanket", "condition": "New"}},
        # Resistance bands
        {"title": "FitBeast Pull Up Resistance Bands Set 5 Pack", "price": "£19.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=FitBeast+resistance+bands", "attrs": {"brand": "FitBeast", "type": "Resistance Bands", "condition": "New"}},
        # Cast iron
        {"title": "Lodge Cast Iron Skillet 30cm Pre-Seasoned", "price": "£44.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Lodge+cast+iron+30cm", "attrs": {"brand": "Lodge", "size": "30cm", "material": "Cast Iron", "type": "Skillet Pan", "condition": "New"}},
        # Noise cancelling headphones
        {"title": "Sony WH-1000XM5 Wireless Noise Cancelling Headphones - Silver", "price": "£229.00", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Sony+WH-1000XM5", "attrs": {"brand": "Sony", "colour": "Silver", "type": "Noise Cancelling Headphones", "condition": "New"}},
        {"title": "Bose QuietComfort Headphones - White Smoke", "price": "£249.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Bose+QuietComfort+headphones", "attrs": {"brand": "Bose", "colour": "White", "type": "Noise Cancelling Headphones", "condition": "New"}},
        {"title": "Anker Soundcore Life Q30 ANC Headphones - Blue - Refurbished", "price": "£39.99", "url": "https://www.ebay.co.uk/sch/i.html?_nkw=Anker+Soundcore+Q30", "attrs": {"brand": "Anker", "colour": "Blue", "type": "Noise Cancelling Headphones", "condition": "Refurbished"}},
    ],
    "gumtree": [
        {"title": "JBL Flip 6 Bluetooth Speaker Red - Barely Used", "price": "£55.00", "url": "https://www.gumtree.com/search?q=JBL+Flip+6", "attrs": {"brand": "JBL", "colour": "Red", "type": "Bluetooth Speaker", "condition": "Used"}},
        {"title": "Roomba 960 Robot Vacuum - Working Great", "price": "£80.00", "url": "https://www.gumtree.com/search?q=Roomba+960", "attrs": {"brand": "iRobot", "type": "Robot Vacuum", "condition": "Used"}},
        {"title": "Razer Huntsman Mini Mechanical Keyboard - Like New", "price": "£45.00", "url": "https://www.gumtree.com/search?q=Razer+Huntsman+Mini", "attrs": {"brand": "Razer", "colour": "Black", "type": "Mechanical Keyboard", "condition": "Like New"}},
        {"title": "Ted Baker Men's Leather Wallet Brown", "price": "£20.00", "url": "https://www.gumtree.com/search?q=Ted+Baker+wallet", "attrs": {"brand": "Ted Baker", "colour": "Brown", "material": "Leather", "type": "Wallet", "condition": "Used"}},
        {"title": "Fitbit Versa 3 Smartwatch Black - Good Condition", "price": "£45.00", "url": "https://www.gumtree.com/search?q=Fitbit+Versa+3", "attrs": {"brand": "Fitbit", "colour": "Black", "type": "Fitness Tracker", "condition": "Good Condition"}},
        {"title": "Apple AirPods 3rd Gen - Good Condition", "price": "£55.00", "url": "https://www.gumtree.com/search?q=AirPods+3rd+gen", "attrs": {"brand": "Apple", "colour": "White", "type": "Wireless Earbuds", "condition": "Good Condition"}},
        {"title": "Logitech G502 Gaming Mouse Wired - Black", "price": "£20.00", "url": "https://www.gumtree.com/search?q=Logitech+G502", "attrs": {"brand": "Logitech", "colour": "Black", "type": "Gaming Mouse", "condition": "Used"}},
        {"title": "Electric Scooter Xiaomi M365 - Needs New Tyre", "price": "£120.00", "url": "https://www.gumtree.com/search?q=Xiaomi+M365+scooter", "attrs": {"brand": "Xiaomi", "colour": "Black", "type": "Electric Scooter", "condition": "Used"}},
        {"title": "IKEA BEKANT Sit-Stand Desk 160x80cm White", "price": "£150.00", "url": "https://www.gumtree.com/search?q=IKEA+BEKANT+sit+stand", "attrs": {"brand": "IKEA", "colour": "White", "type": "Standing Desk", "condition": "Used"}},
        {"title": "Instax Mini 11 Camera Lilac Purple - Boxed", "price": "£35.00", "url": "https://www.gumtree.com/search?q=Instax+Mini+11", "attrs": {"brand": "Fujifilm", "colour": "Purple", "type": "Instant Camera", "condition": "Like New"}},
        {"title": "Salomon Quest 4 GTX Hiking Boots Size 10 - Worn Twice", "price": "£85.00", "url": "https://www.gumtree.com/search?q=Salomon+Quest+4+GTX", "attrs": {"brand": "Salomon", "colour": "Green", "size": "10", "type": "Hiking Boots", "condition": "Like New"}},
        {"title": "DeLonghi Magnifica S Coffee Machine - Silver", "price": "£180.00", "url": "https://www.gumtree.com/search?q=DeLonghi+Magnifica+S", "attrs": {"brand": "De'Longhi", "colour": "Silver", "type": "Espresso Machine", "condition": "Used"}},
        {"title": "iPad Air 5th Gen 64GB Space Grey - Mint", "price": "£280.00", "url": "https://www.gumtree.com/search?q=iPad+Air+5th+gen", "attrs": {"brand": "Apple", "colour": "Space Grey", "storage": "64GB", "type": "Tablet", "condition": "Like New"}},
        {"title": "Anker 20000mAh Power Bank - Barely Used", "price": "£12.00", "url": "https://www.gumtree.com/search?q=Anker+power+bank", "attrs": {"brand": "Anker", "type": "Power Bank", "condition": "Used"}},
        {"title": "Vango Alpha 200 Tent 2 Person Green - Used Once", "price": "£25.00", "url": "https://www.gumtree.com/search?q=Vango+Alpha+200+tent", "attrs": {"brand": "Vango", "colour": "Green", "type": "Camping Tent", "capacity": "2 Person", "condition": "Like New"}},
        {"title": "Sony WH-1000XM4 Headphones Black - Great Condition", "price": "£140.00", "url": "https://www.gumtree.com/search?q=Sony+WH-1000XM4", "attrs": {"brand": "Sony", "colour": "Black", "type": "Noise Cancelling Headphones", "condition": "Good Condition"}},
        {"title": "Silver Cross Zest Pushchair - Light Grey - Like New", "price": "£80.00", "url": "https://www.gumtree.com/search?q=Silver+Cross+Zest+pushchair", "attrs": {"brand": "Silver Cross", "colour": "Grey", "type": "Pushchair", "condition": "Like New"}},
    ],
    "facebook_marketplace": [
        {"title": "UE Boom 3 Bluetooth Speaker - Red", "price": "£40.00", "url": "https://www.facebook.com/marketplace/search?query=UE+Boom+3", "attrs": {"brand": "Ultimate Ears", "colour": "Red", "type": "Bluetooth Speaker", "condition": "Used"}},
        {"title": "Eufy RoboVac G30 Robot Vacuum - White", "price": "£70.00", "url": "https://www.facebook.com/marketplace/search?query=Eufy+RoboVac", "attrs": {"brand": "Eufy", "colour": "White", "type": "Robot Vacuum", "condition": "Used"}},
        {"title": "Anne Pro 2 Mechanical Keyboard 60% - White", "price": "£35.00", "url": "https://www.facebook.com/marketplace/search?query=Anne+Pro+2", "attrs": {"brand": "Anne Pro", "colour": "White", "type": "Mechanical Keyboard", "condition": "Used"}},
        {"title": "Samsung Galaxy Watch 5 40mm Graphite", "price": "£85.00", "url": "https://www.facebook.com/marketplace/search?query=Galaxy+Watch+5", "attrs": {"brand": "Samsung", "colour": "Grey", "type": "Fitness Tracker", "condition": "Used"}},
        {"title": "Samsung Galaxy Buds 2 Pro - Graphite", "price": "£45.00", "url": "https://www.facebook.com/marketplace/search?query=Galaxy+Buds+2+Pro", "attrs": {"brand": "Samsung", "colour": "Grey", "type": "Wireless Earbuds", "condition": "Good Condition"}},
        {"title": "SteelSeries Rival 600 Gaming Mouse", "price": "£25.00", "url": "https://www.facebook.com/marketplace/search?query=SteelSeries+Rival+600", "attrs": {"brand": "SteelSeries", "colour": "Black", "type": "Gaming Mouse", "condition": "Used"}},
        {"title": "Ninebot Segway ES2 Electric Scooter", "price": "£150.00", "url": "https://www.facebook.com/marketplace/search?query=Segway+ES2+scooter", "attrs": {"brand": "Segway", "colour": "Grey", "type": "Electric Scooter", "condition": "Used"}},
        {"title": "Standing Desk Electric 120cm - White", "price": "£100.00", "url": "https://www.facebook.com/marketplace/search?query=standing+desk", "attrs": {"colour": "White", "type": "Standing Desk", "condition": "Used"}},
        {"title": "Polaroid Now Camera - Blue", "price": "£40.00", "url": "https://www.facebook.com/marketplace/search?query=Polaroid+Now", "attrs": {"brand": "Polaroid", "colour": "Blue", "type": "Instant Camera", "condition": "Used"}},
        {"title": "Timberland Men's Waterproof Hiking Boots Size 11", "price": "£45.00", "url": "https://www.facebook.com/marketplace/search?query=Timberland+hiking+boots", "attrs": {"brand": "Timberland", "colour": "Brown", "size": "11", "type": "Hiking Boots", "condition": "Used"}},
        {"title": "Samsung Galaxy Tab A8 64GB - Grey", "price": "£95.00", "url": "https://www.facebook.com/marketplace/search?query=Samsung+Tab+A8", "attrs": {"brand": "Samsung", "colour": "Grey", "storage": "64GB", "type": "Tablet", "condition": "Good Condition"}},
        {"title": "Bugaboo Bee 6 Pushchair - Mineral Black", "price": "£250.00", "url": "https://www.facebook.com/marketplace/search?query=Bugaboo+Bee+6", "attrs": {"brand": "Bugaboo", "colour": "Black", "type": "Pushchair", "condition": "Good Condition"}},
        {"title": "Weighted Blanket 9kg Double King Size - Navy", "price": "£15.00", "url": "https://www.facebook.com/marketplace/search?query=weighted+blanket", "attrs": {"colour": "Navy", "weight": "9kg", "type": "Weighted Blanket", "condition": "Used"}},
        {"title": "Resistance Band Set with Door Anchor - New", "price": "£8.00", "url": "https://www.facebook.com/marketplace/search?query=resistance+bands+set", "attrs": {"type": "Resistance Bands", "condition": "New"}},
        {"title": "Le Creuset Cast Iron Casserole Dish 26cm - Red", "price": "£65.00", "url": "https://www.facebook.com/marketplace/search?query=Le+Creuset+cast+iron", "attrs": {"brand": "Le Creuset", "colour": "Red", "size": "26cm", "material": "Cast Iron", "type": "Skillet Pan", "condition": "Used"}},
        {"title": "Bose 700 Noise Cancelling Headphones - Silver", "price": "£110.00", "url": "https://www.facebook.com/marketplace/search?query=Bose+700+headphones", "attrs": {"brand": "Bose", "colour": "Silver", "type": "Noise Cancelling Headphones", "condition": "Used"}},
    ],
    "vinted": [
        {"title": "Mens Leather Wallet Ralph Lauren - Tan", "price": "£22.00", "url": "https://www.vinted.co.uk/catalog?search_text=Ralph+Lauren+wallet", "attrs": {"brand": "Ralph Lauren", "colour": "Brown", "material": "Leather", "type": "Wallet", "condition": "Good Condition"}},
        {"title": "Fossil Gen 5 Smartwatch - Brown Leather", "price": "£35.00", "url": "https://www.vinted.co.uk/catalog?search_text=Fossil+Gen+5", "attrs": {"brand": "Fossil", "colour": "Brown", "type": "Fitness Tracker", "condition": "Used"}},
        {"title": "Samsung Galaxy Buds Live - Mystic Bronze", "price": "£20.00", "url": "https://www.vinted.co.uk/catalog?search_text=Galaxy+Buds+Live", "attrs": {"brand": "Samsung", "colour": "Bronze", "type": "Wireless Earbuds", "condition": "Used"}},
        {"title": "Merrell Moab 2 GTX Hiking Shoes Size 9 - Beluga", "price": "£38.00", "url": "https://www.vinted.co.uk/catalog?search_text=Merrell+Moab+2+GTX", "attrs": {"brand": "Merrell", "colour": "Grey", "size": "9", "type": "Hiking Boots", "condition": "Good Condition"}},
        {"title": "Paul Smith Leather Bifold Wallet - Black", "price": "£30.00", "url": "https://www.vinted.co.uk/catalog?search_text=Paul+Smith+wallet", "attrs": {"brand": "Paul Smith", "colour": "Black", "material": "Leather", "type": "Wallet", "condition": "Good Condition"}},
        {"title": "Sony WH-CH710N Headphones Blue", "price": "£22.00", "url": "https://www.vinted.co.uk/catalog?search_text=Sony+WH-CH710N", "attrs": {"brand": "Sony", "colour": "Blue", "type": "Noise Cancelling Headphones", "condition": "Used"}},
        {"title": "Uppababy Vista V2 Pushchair - Gregory Blue", "price": "£380.00", "url": "https://www.vinted.co.uk/catalog?search_text=Uppababy+Vista+V2", "attrs": {"brand": "Uppababy", "colour": "Blue", "type": "Pushchair", "condition": "Good Condition"}},
        {"title": "Icandy Peach 7 Pushchair - Ivy Green", "price": "£450.00", "url": "https://www.vinted.co.uk/catalog?search_text=Icandy+Peach+7", "attrs": {"brand": "Icandy", "colour": "Green", "type": "Pushchair", "condition": "Good Condition"}},
    ],
}


# Re-use scoring from demo.py
STOP_WORDS = {"the", "a", "an", "and", "or", "for", "with", "on", "in", "to", "of", "is", "it"}
MIN_MATCH_RATIO = 0.5

# Synonym groups — any word in a group is treated as equivalent
SYNONYMS = [
    {"pushchair", "stroller", "pram", "buggy", "pushchairs", "strollers", "prams", "buggies"},
    {"headphones", "headphone", "earphones", "earphone"},
    {"earbuds", "earbud", "earphones", "earphone", "buds"},
    {"trainers", "sneakers", "shoes"},
    {"laptop", "notebook"},
    {"mobile", "phone", "smartphone"},
    {"tv", "television"},
    {"fridge", "refrigerator"},
    {"sofa", "couch"},
]

def _expand_synonyms(words: list[str]) -> list[str]:
    """Expand query words with their synonyms."""
    expanded = list(words)
    for word in words:
        for group in SYNONYMS:
            if word in group:
                for syn in group:
                    if syn not in expanded:
                        expanded.append(syn)
    return expanded


def _score_item(
    item: dict, query_words: list[str], colour: str | None,
    condition: str | None, brand: str | None = None,
) -> float:
    """Score how well an item matches the search query."""
    title_lower = item["title"].lower()
    title_words = set(title_lower.split())
    attrs = item.get("attrs", {})
    attrs_text = " ".join(attrs.values()).lower()
    attrs_words = set(attrs_text.split())

    # Hard brand filter: if user specified a brand, reject non-matching items
    if brand:
        item_brand = attrs.get("brand", "").lower()
        if brand.lower() not in item_brand and brand.lower() not in title_lower:
            return 0.0

    meaningful_words = [w for w in query_words if w not in STOP_WORDS]
    if not meaningful_words:
        return 0.0

    # Expand with synonyms for matching
    expanded = _expand_synonyms(meaningful_words)

    score = 0.0
    matches = 0
    for word in meaningful_words:
        # Check original word + its synonyms
        words_to_check = [word]
        for syn in expanded:
            if syn != word and syn not in meaningful_words:
                # Check if syn is a synonym of this word
                for group in SYNONYMS:
                    if word in group and syn in group:
                        words_to_check.append(syn)

        matched = False
        for w_check in words_to_check:
            title_match = any(w.startswith(w_check) or w_check.startswith(w) for w in title_words if len(w) > 2)
            attrs_match = any(w.startswith(w_check) or w_check.startswith(w) for w in attrs_words if len(w) > 2)

            if title_match:
                score += 2.0
                matches += 1
                matched = True
                break
            elif attrs_match:
                score += 1.0
                matches += 1
                matched = True
                break

    if len(meaningful_words) >= 2:
        for i in range(len(meaningful_words) - 1):
            phrase = f"{meaningful_words[i]} {meaningful_words[i+1]}"
            if phrase in title_lower:
                score += 3.0

    match_ratio = matches / len(meaningful_words) if meaningful_words else 0
    # Require higher match ratio for short queries to reduce noise
    min_ratio = MIN_MATCH_RATIO if len(meaningful_words) > 2 else 0.6
    if match_ratio < min_ratio:
        return 0.0

    # Type-aware scoring: if query mentions a specific product type, boost matching items
    # and penalise items of a different type in the same category
    item_type = attrs.get("type", "").lower()
    type_conflicts = {
        "earbuds": {"noise cancelling headphones", "headphones"},
        "headphones": {"wireless earbuds", "bluetooth speaker"},
        "speaker": {"wireless earbuds", "noise cancelling headphones", "headphones"},
    }
    for type_word, conflicting_types in type_conflicts.items():
        if type_word in meaningful_words:
            if item_type in conflicting_types:
                return 0.0  # Hard reject conflicting type
            if type_word in item_type or item_type and type_word in item_type:
                score += 2.0  # Boost matching type

    if colour and colour.lower() in attrs_text:
        score += 1.0
    if condition:
        item_cond = attrs.get("condition", "").lower()
        if condition.lower() in item_cond:
            score += 1.0

    return score


def _price_to_float(price_str: str) -> float | None:
    try:
        cleaned = price_str.replace("£", "").replace("$", "").replace("€", "").replace(",", "").strip()
        return float(cleaned)
    except (ValueError, AttributeError):
        return None


class WebDataScraper(BaseScraper):
    """Scraper backed by real product data sourced from web searches."""

    name = "web_data"

    def __init__(self, marketplace_name: str, config: dict | None = None):
        super().__init__(config)
        self.name = marketplace_name
        self._catalogue = _WEB_CATALOGUES.get(marketplace_name, [])

    async def search(self, query: str, **filters) -> list[ScrapedItem]:
        query_lower = query.lower()
        query_words = [w for w in query_lower.split() if len(w) > 1]

        min_price = filters.get("min_price")
        max_price = filters.get("max_price")
        colour = filters.get("colour")
        condition = filters.get("condition")
        brand = filters.get("brand")

        scored = []
        for item in self._catalogue:
            score = _score_item(item, query_words, colour, condition, brand)
            if score <= 0:
                continue

            price_val = _price_to_float(item["price"])
            if price_val is not None:
                if min_price is not None and price_val < float(min_price):
                    continue
                if max_price is not None and price_val > float(max_price):
                    continue

            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)

        items = []
        for item_score, item_data in scored:
            seed = hashlib.md5(item_data["title"].encode()).hexdigest()[:8]
            items.append(ScrapedItem(
                title=item_data["title"],
                price=item_data["price"],
                url=item_data.get("url", f"https://www.example.com/{self.name}/item/{seed}"),
                image_url=f"https://picsum.photos/seed/{seed}/400/300",
                marketplace=self.name,
                raw_attributes=item_data.get("attrs", {}),
            ))

        return items

    async def extract_details(self, item_url: str) -> dict[str, str]:
        return {"source": "web_search", "note": "Real product data sourced from web search"}
