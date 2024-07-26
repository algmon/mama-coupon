import requests
import json
import random

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

model = "llama3"

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

print(json.dumps(json.loads(json_data["response"]), indent=2))
