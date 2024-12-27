import gzip
import json
import random as rnd
from datetime import datetime, timedelta
from enum import Enum
import math
from tqdm import tqdm

class Season(Enum):
    WINTER = 90
    SPRING = 80
    SUMMER = 70
    AUTUMN = 60

def get_season(month):
    if month in [1, 2, 3]:
        return Season.WINTER
    elif month in [4, 5, 6]:
        return Season.SPRING
    elif month in [7, 8, 9]:
        return Season.SUMMER
    elif month in [10, 11, 12]:
        return Season.AUTUMN

date_format = "%d/%m/%Y"
membership_types = ["None","Silver","Gold","Platinum"]

def today():
    return datetime.today().strftime(date_format)

def random_time():
    hours = rnd.randint(0, 23)
    minutes = rnd.randint(0, 59)
    return datetime(1, 1, 1, hours, minutes, 0).strftime('%I:%M %p')

def generate_address():
    streets = ["Main St", "Second Ave", "Maple Drive", "Oak Street", "Elm St"]
    house_number = rnd.randint(100, 999)
    street_name = rnd.choice(streets)
    return f"{house_number} {street_name}"

def random_date(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, date_format)
    end_date = datetime.strptime(end_date_str, date_format)
    random_days = rnd.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).strftime(date_format)

def count_days(d1,d2):
    sd = datetime.strptime(d1, date_format)
    ed = datetime.strptime(d2, date_format)
    return (ed-sd).days

def get_cat(chances):
    arr = []
    for j in range(0,5):
        for _ in range(0,chances[j]):
            arr.append(j)
    return rnd.choice(arr)

def randomChoice(cat):
    prod = rnd.choice(cat)
    index = cat.index(prod)
    return [prod,index]

def calculate_price(base,ci,si,pi):
    return base + (ci*2) + (si*3) + (pi*1.5)

def purchase_history(date,m,g):
    categories = ["E","F","S","T","C"]
    products = [
        ["Laptop","Smartphone","Fridge","TV","AC","Computer","Cooler","Speaker","Tablet","Heater"],
        ["Table","Chair","Cabinet","Desk","Cupboard","Shelve","Stand","Soffa","Bed","Couch","Bench"],
        ["Cricket_Bat","Tennis_Ball","Season_Ball","Basket_Ball","Football","TT_Kit","Cricket_Kit","Javeline","Baseball_Kit","Hockey_Kit"],
        ["Bag","Camping_Net","Sleeping_Bag","Stove","Medical_Kit","Stick","Rope","Tools_Kit"],
        ["TShirt","Shirt","Pant","Joggers","Hoodie","Shoes","Slippers","Suit","Half_Pant"],
    ]
    prices = [
        [450, 1200, 250, 1800, 300, 500, 400, 1500, 500, 1000, 1000, 3000, 400, 800, 400, 700, 500, 1500, 500, 900],
        [150, 200, 300, 350, 450, 500, 600, 650, 750, 800, 900, 950, 1050, 1100, 1200, 1250, 1350, 1400, 1500, 1550, 1600, 1650],
        [30, 40, 60, 70, 90, 100, 120, 130, 150, 160, 180, 200, 210, 220, 240, 250, 270, 280, 300, 320],
        [100, 120, 50, 80, 80, 100, 150, 200, 200, 250, 30, 40, 40, 60, 120, 150, 80, 100],
        [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 60, 70, 80, 90, 100, 110],
    ]
    payment_methods = ["c","cc","dc","e"]
    colors = ["r", "c", "g", "b", "w", "y", "p"]
    sizes = ["S", "M", "L", "XL", "XXL"]

    season_preferences = {
        Season.WINTER: [10, 10, 20, 10, 50],
        Season.SPRING: [30, 20, 10, 25, 15],
        Season.SUMMER: [30, 10, 20, 30, 10],
        Season.AUTUMN: [ 5, 10, 20, 35, 30]
    }

    discount = {
        membership_types[0]: 100,
        membership_types[1]: 90,
        membership_types[2]: 80,
        membership_types[3]: 70
    }

    purchase = []
    for i in range(0,5):
        purchase.append({
            "name": categories[i],
            "products": [],
        })

    nproducts = math.floor(rnd.randint(3,5) * 0.0005 * count_days(date,today()))
    # print(nproducts)
    for i in range(0,nproducts):
        pur_date = random_date(date,"31/08/2024")
        season = get_season(datetime.strptime(pur_date,date_format).month)
        pref_cat = get_cat(season_preferences[season])
        prod_i = rnd.randint(0,len(products[pref_cat]) - 1)
        prod = products[pref_cat][prod_i]

        cr = randomChoice(colors)
        sz = randomChoice(sizes)
        pm = randomChoice(payment_methods)
        
        base = rnd.randint(prices[pref_cat][prod_i * 2],prices[pref_cat][(prod_i * 2) + 1])
        adj_price = calculate_price(base,cr[1],sz[1],pm[1])
        price = adj_price * (rnd.randint(discount[m] if rnd.randint(0,1) == 1 else season.value,100)) / 100

        item = {
            "n": prod,
            "p": price,
            "c": cr[0],
            "s": sz[0],
            "m": pm[0],
            "d": pur_date,
            "t": random_time(),
            "r": rnd.randint(1,5)
        }
        purchase[pref_cat]['products'].append(item)
    return purchase

people = [
    {"name": "Olivia", "gender": "f"},
    {"name": "Liam", "gender": "m"},
    {"name": "Emma", "gender": "f"},
    {"name": "Noah", "gender": "m"},
    {"name": "Ava", "gender": "f"},
    {"name": "Elijah", "gender": "m"},
    {"name": "Sophia", "gender": "f"},
    {"name": "Lucas", "gender": "m"},
    {"name": "Isabella", "gender": "f"},
    {"name": "Mason", "gender": "m"},
    {"name": "Mia", "gender": "f"},
    {"name": "James", "gender": "m"},
    {"name": "Amelia", "gender": "f"},
    {"name": "Ethan", "gender": "m"},
    {"name": "Harper", "gender": "f"},
    {"name": "Benjamin", "gender": "m"},
    {"name": "Evelyn", "gender": "f"},
    {"name": "Alexander", "gender": "m"},
    {"name": "Abigail", "gender": "f"},
    {"name": "Michael", "gender": "m"},
    {"name": "Emily", "gender": "f"},
    {"name": "Daniel", "gender": "m"},
    {"name": "Charlotte", "gender": "f"},
    {"name": "Matthew", "gender": "m"},
    {"name": "Elizabeth", "gender": "f"}
]
surnames = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris"]

doms = ["gmail","yahoo","outlook","hotmail","aol","icloud","mail","protonmail","zoho","yandex"]
extensions = ["in","com","co","au","cn","us"]

states = [
    {
        "state_name": "California",
        "cities": [
            {"city_name": "Los Angeles", "postal_code": "90001", "address": generate_address()},
            {"city_name": "San Francisco", "postal_code": "94102", "address": generate_address()},
            {"city_name": "San Diego", "postal_code": "92101", "address": generate_address()},
            {"city_name": "Sacramento", "postal_code": "94203", "address": generate_address()},
            {"city_name": "Fresno", "postal_code": "93701", "address": generate_address()}
        ]
    },
    {
        "state_name": "Texas",
        "cities": [
            {"city_name": "Houston", "postal_code": "77001", "address": generate_address()},
            {"city_name": "Dallas", "postal_code": "75201", "address": generate_address()},
            {"city_name": "Austin", "postal_code": "73301", "address": generate_address()},
            {"city_name": "San Antonio", "postal_code": "78201", "address": generate_address()},
            {"city_name": "Fort Worth", "postal_code": "76101", "address": generate_address()}
        ]
    },
    {
        "state_name": "Florida",
        "cities": [
            {"city_name": "Miami", "postal_code": "33101", "address": generate_address()},
            {"city_name": "Orlando", "postal_code": "32801", "address": generate_address()},
            {"city_name": "Tampa", "postal_code": "33601", "address": generate_address()},
            {"city_name": "Jacksonville", "postal_code": "32099", "address": generate_address()},
            {"city_name": "Tallahassee", "postal_code": "32301", "address": generate_address()}
        ]
    },
    {
        "state_name": "New York",
        "cities": [
            {"city_name": "New York", "postal_code": "10001", "address": generate_address()},
            {"city_name": "Buffalo", "postal_code": "14201", "address": generate_address()},
            {"city_name": "Rochester", "postal_code": "14602", "address": generate_address()},
            {"city_name": "Albany", "postal_code": "12201", "address": generate_address()},
            {"city_name": "Syracuse", "postal_code": "13201", "address": generate_address()}
        ]
    },
    {
        "state_name": "Illinois",
        "cities": [
            {"city_name": "Chicago", "postal_code": "60601", "address": generate_address()},
            {"city_name": "Aurora", "postal_code": "60502", "address": generate_address()},
            {"city_name": "Naperville", "postal_code": "60540", "address": generate_address()},
            {"city_name": "Joliet", "postal_code": "60431", "address": generate_address()},
            {"city_name": "Springfield", "postal_code": "62701", "address": generate_address()}
        ]
    }
]

for i in tqdm(range(10000)):
    name = rnd.randint(0, 24)
    surname = surnames[rnd.randint(0, 24)]
    state = states[rnd.randint(0, 4)]
    city = state["cities"][rnd.randint(0, 4)]
    date = random_date('01/01/1980', '31/12/2010')
    membership = rnd.choice(membership_types)
    history = purchase_history(date,membership,people[name]['gender'])
    all_dates = [prod['d'] for cat in history for prod in cat['products']]
    
    customer = {
        "i": i + 1,
        "n": f"{people[name]['name']} {surname}",
        "e": f"{people[name]['name']}{'.' + surname if rnd.randint(0, 10) < 5 else ''}{rnd.randint(100, 999)}@{doms[rnd.randint(0, 9)]}.{extensions[rnd.randint(0, 5)]}",
        "p": f"{rnd.randint(1, 9)}{''.join([str(rnd.randint(0, 9)) for _ in range(9)])}",
        "a": f"{city['address']}, {city['city_name']}, {city['postal_code']}, {state['state_name']}",
        "d": date,
        "g": people[name]['gender'],
        "b": [
            {"Category": cat["name"], "Products": cat["products"]} for cat in history
        ],
        "m": membership,
        "f": max(history, key=lambda obj: len(obj["products"]))["name"],
        "x": sorted(all_dates, key=lambda x: datetime.strptime(x, date_format))[-1],
        "l": random_date(sorted(all_dates, key=lambda x: datetime.strptime(x, date_format))[-1], today())
    }

    # for i in range(0,5): print(f"{customer['b'][i]['Category']} : {len(customer['b'][i]['Products'])}")

    with gzip.open(f"../CustomersDataset/c{i+1}.json.gz", 'wt', encoding='utf-8') as file:
        json.dump(customer, file, separators=(',', ':'), ensure_ascii=False)

""" 

i : Id
n : Name
e : Email
p : Phone
a : Address
d : DOB
g : Gender
b : Buys [Array of categories where each product in each category has following data]
    n : Name
    p : Price
    c : Color
    s : Size
    m : Payment Method
    d : Date
    t : Time
    r : Rating
m : Membership
f : Favorite
x : Last Purchase
l : Last Login
    
"""