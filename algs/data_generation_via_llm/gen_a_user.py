import requests
import json
import random
import mysql.connector

def gen_a_user():
    # step 1: gen a user

    interests = [
        "Technology",
        "Gaming",
        "Travel",
        "Fitness",
        "Health & Wellness",
        "Fashion",
        "Food & Cooking",
        "Music",
        "Movies & TV Shows",
        "Books & Literature",
        "Photography",
        "Art & Design",
        "Sports",
        "Outdoor Activities",
        "DIY & Crafts",
        "Home & Garden",
        "Pets & Animals",
        "Business & Finance",
        "Education",
        "Science",
        "History",
        "Politics",
        "Social Issues",
        "Environment",
        "Automotive",
        "Parenting",
        "Relationships",
        "Spirituality & Religion",
        "Technology Gadgets",
        "Investment & Stocks",
        "Real Estate",
        "Entrepreneurship",
        "Marketing",
        "Writing & Blogging",
        "Public Speaking",
        "Self-Improvement",
        "Mindfulness & Meditation",
        "Fitness & Nutrition",
        "Beauty & Skincare",
        "Travel & Adventure",
        "Cultural Events",
        "Virtual Reality",
        "Artificial Intelligence",
        "E-sports",
        "Board Games",
        "Wine & Spirits",
        "Coffee & Tea",
        "Baking",
        "Vegan & Vegetarian",
        "Luxury Lifestyle",
        "Minimalism",
        "Sustainable Living",
        "Volunteer Work",
        "Collectibles & Antiques",
        "Astrology",
        "Comics & Anime",
        "Languages & Linguistics",
        "Architecture",
        "Urban Exploration",
        "Adventure Sports"
    ]

    countries = [
        "United States",
        "China",
        "United Kingdom",
        "Japan",
        "India",
        "Brazil",
        "the Netherlands",
        "Germany",
        "Mexico",
        "Canada",
        "France",
        "Australia",
        "Singapore",
    ]

    interest_tag_1 = random.choice(interests)
    interest_tag_2 = random.choice(interests)
    interest_tag_3 = random.choice(interests)
    interest_tag_4 = random.choice(interests)
    interest_tag_5 = random.choice(interests)
    country = random.choice(countries)

    model = "llama2"

    prompt = f"generate one realistically believable sample data set of a person's username, password, email, phone, gender, age, occupation, annual_income, self_intro, address in {country}, 5 interest tags are {interest_tag_1}, {interest_tag_2}, {interest_tag_3}, {interest_tag_4} and {interest_tag_5}. Do not use common names. Respond using JSON. Key names should have no backslashes, values should use plain ascii with no special characters. The generated email domain name should be suanfamama.com. For example, wei@suanfamama.com. The generated password should always be Lovesuanfamama"

    data = {
        "prompt": prompt,
        "model": model,
        "format": "json",
        "stream": False,
        "options": {"temperature": 2.5, "top_p": 0.99, "top_k": 100},
    }

    print(f"Generating a user in {country}")
    response = requests.post("http://localhost:11434/api/generate", json=data, stream=False)
    json_data = json.loads(response.text)
    '''
    # the sample generated user profile
    {
    "username": "AureliaDujardin",
    "password": "Lovesuanfamama",
    "email": "aurelia.dujardin@suanfamama.com",
    "phone": "+33215565600",
    "gender": "female",
    "age": 38,
    "occupation": "Marketing Manager",
    "annual_income": 80000,
    "self_intro": "Curious about the mysteries of the universe and the best board games. Enjoy exploring spirituality and sharing experiences with fellow seekers.",
    "address": {
        "street": "Rue des \u00c9toiles",
        "city": "Lyon",
        "region": "Rh\u00f4ne-Alpes",
        "postal_code": 69000,
        "country": "France"
    },
    "interests": [
        "Board Games",
        "Wine & Spirits",
        "Astrology",
        "Spirituality & Religion",
        "Volunteer Work"
    ]
    }
    '''
    print(json.dumps(json.loads(json_data["response"]), indent=2))

def store_a_user():
    # step2: put the user info into a database
    '''
    # the sample database schema
    username
    password_hash
    email
    phone
    gender
    age
    occupation
    annual_income
    description
    address
    interests
    '''
    # Load configuration from config.json
    with open('config.json') as f:
        config = json.load(f)

    # Establish the connection
    connection = mysql.connector.connect(**config['database3'])

    cursor = connection.cursor()

    # Sample query
    cursor.execute("SELECT DATABASE()")

    # Fetch the result
    result = cursor.fetchone()
    print(f"Connected to database: {result[0]}")

    # TODO: Store the user info

    # Close the connection
    cursor.close()
    connection.close()

def add_columns_to_db_table():
    """
    Adds new columns to the user table in the database
    """
    # Load configuration from config.json
    with open('config.json') as f:
        config = json.load(f)

    # Establish the connection
    connection = mysql.connector.connect(**config['database2'])
    cursor = connection.cursor()

    # Sample query
    cursor.execute("SELECT DATABASE()")

    # Fetch the result
    result = cursor.fetchone()
    print(f"Connected to database: {result[0]}")

    # Define the SQL statements to add columns
    sql_statements = [
        "ALTER TABLE users ADD COLUMN address_street VARCHAR(255)",
        "ALTER TABLE users ADD COLUMN address_city VARCHAR(255)",
        "ALTER TABLE users ADD COLUMN address_region VARCHAR(255)",
        "ALTER TABLE users ADD COLUMN address_postal_code VARCHAR(20)",
        "ALTER TABLE users ADD COLUMN address_country VARCHAR(50)",
        "ALTER TABLE users ADD COLUMN interest_1 VARCHAR(255)",
        "ALTER TABLE users ADD COLUMN interest_2 VARCHAR(255)",
        "ALTER TABLE users ADD COLUMN interest_3 VARCHAR(255)",
        "ALTER TABLE users ADD COLUMN interest_4 VARCHAR(255)",
        "ALTER TABLE users ADD COLUMN interest_5 VARCHAR(255)"
    ]

    # Execute each SQL statement
    for statement in sql_statements:
        cursor.execute(statement)
        connection.commit()

    print("Columns added successfully!")

    # Close the connection
    cursor.close()
    connection.close()

if __name__ == "__main__":
    #gen_a_user()
    #add_columns_to_db_table()
    store_a_user()