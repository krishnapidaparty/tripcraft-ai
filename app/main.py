import time
import os
import json
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import openai
from pydantic import BaseModel

# Chat model
class ChatMessage(BaseModel):
    message: str

# Load environment variables
load_dotenv()

app = FastAPI()
START_TIME = time.time()
REQ_COUNT = {"total": 0}

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_tripadvisor_reviews(destination: str, style: str) -> list:
    """
    Generate realistic TripAdvisor-style reviews for a destination
    """
    try:
        client = openai.OpenAI()
        prompt = f"""
        Generate 3 realistic TripAdvisor reviews for {destination} that would appeal to {style} travelers.
        
        Each review should include:
        1. A realistic username
        2. A star rating (4-5 stars for positive reviews)
        3. A review title
        4. A detailed review (2-3 sentences)
        5. A helpful tip or recommendation
        
        Format as JSON:
        {{
            "reviews": [
                {{
                    "username": "Traveler123",
                    "rating": 5,
                    "title": "Amazing experience!",
                    "review": "Detailed review text...",
                    "tip": "Helpful tip for future travelers"
                }}
            ]
        }}
        
        Make the reviews authentic and specific to {destination} and {style} travel preferences.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a travel expert who creates authentic TripAdvisor-style reviews."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.8
        )
        
        content = response.choices[0].message.content.strip()
        
        # Extract JSON
        start = content.find('{')
        end = content.rfind('}') + 1
        json_str = content[start:end]
        data = json.loads(json_str)
        
        return data.get('reviews', [])
        
    except Exception as e:
        # Fallback reviews
        return [
            {
                "username": "AdventureSeeker",
                "rating": 5,
                "title": "Perfect for adventure lovers!",
                "review": f"Absolutely loved {destination}! The activities were perfectly suited for adventure travelers. The local guides were knowledgeable and the experiences were unforgettable.",
                "tip": "Book activities in advance during peak season"
            },
            {
                "username": "TravelExplorer",
                "rating": 4,
                "title": "Great destination with amazing experiences",
                "review": f"{destination} exceeded my expectations. The combination of natural beauty and adventure activities made this trip truly special.",
                "tip": "Don't forget to bring comfortable hiking shoes"
            },
            {
                "username": "Wanderlust2024",
                "rating": 5,
                "title": "Bucket list destination!",
                "review": f"One of the best trips I've ever taken. {destination} offers everything an adventure seeker could want - from thrilling activities to stunning landscapes.",
                "tip": "Try the local cuisine and interact with locals for authentic experiences"
            }
        ]

def get_restaurant_links(restaurant_name: str, destination: str) -> dict:
    """
    Generate restaurant website links and booking options
    """
    # Clean restaurant name for URL generation
    clean_name = restaurant_name.replace(" ", "+").replace("&", "and")
    
    # Special cases for well-known restaurants
    special_restaurants = {
        "locavore": {
            "website": "https://www.locavore.co.id/",
            "menu": "https://www.locavore.co.id/menu",
            "booking": "https://www.locavore.co.id/reservations",
            "reviews": "https://www.tripadvisor.com/Restaurant_Review-g297700-d1074565-Reviews-Locavore-Bali.html",
            "maps": "https://www.google.com/maps/place/Locavore/@-8.5067,115.2625,15z/"
        },
        "noma": {
            "website": "https://noma.dk/",
            "menu": "https://noma.dk/menu",
            "booking": "https://noma.dk/reservations",
            "reviews": "https://www.tripadvisor.com/Restaurant_Review-g189541-d739042-Reviews-Noma-Copenhagen_Zealand.html",
            "maps": "https://www.google.com/maps/place/Noma/@55.6828,12.6007,15z/"
        },
        "el bulli": {
            "website": "https://elbulli.com/",
            "menu": "https://elbulli.com/menu",
            "booking": "https://elbulli.com/reservations",
            "reviews": "https://www.tripadvisor.com/Restaurant_Review-g187499-d739041-Reviews-El_Bulli-Roses_Costa_Brava_Province_of_Girona_Catalonia.html",
            "maps": "https://www.google.com/maps/place/El+Bulli/@42.2489,3.2234,15z/"
        }
    }
    
    # Check if it's a special restaurant
    restaurant_lower = restaurant_name.lower()
    for special_name, links in special_restaurants.items():
        if special_name in restaurant_lower:
            return links
    
    # Default links for other restaurants
    return {
        "website": f"https://www.google.com/search?q={clean_name}+{destination}+restaurant+website",
        "menu": f"https://www.google.com/search?q={clean_name}+{destination}+menu",
        "booking": f"https://www.opentable.com/search?q={clean_name}+{destination}",
        "reviews": f"https://www.tripadvisor.com/RestaurantSearch?q={clean_name}+{destination}",
        "maps": f"https://www.google.com/maps/search/{clean_name}+{destination}"
    }

@app.middleware("http")
async def count_requests(request, call_next):
    REQ_COUNT["total"] += 1
    return await call_next(request)

@app.get("/metrics.json")
async def metrics_json():
    return {
        "uptime_sec": round(time.time() - START_TIME, 1),
        "requests": REQ_COUNT["total"]
    }

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/recommend", response_class=HTMLResponse)
async def recommend_destinations(
    request: Request,
    budget: str = Form(...),
    style: str = Form(...),
    duration: str = Form(...)
):
    try:
        # Create a structured prompt for OpenAI
        prompt = f"""
        Based on the following travel preferences, suggest 3 perfect destinations:

        Budget: {budget}
        Travel Style: {style}
        Trip Duration: {duration}

        For each destination, provide:
        1. Destination name
        2. Brief description (2-3 sentences) explaining why it's perfect for these preferences
        3. Estimated cost range for this trip duration
        4. Booking links for hotels, flights, and activities

        Format your response as JSON with this structure:
        {{
            "destinations": [
                {{
                    "name": "Destination Name",
                    "description": "Why this destination is perfect...",
                    "cost": "Estimated cost range",
                    "booking_links": {{
                        "hotels": "https://www.booking.com/searchresults.html?ss=Destination+Name",
                        "flights": "https://www.expedia.com/Flights-Search?leg1=from:Anywhere,to:Destination+Name",
                        "activities": "https://www.viator.com/Destination-Name/d98-ttd"
                    }}
                }}
            ]
        }}

        Make sure the destinations are realistic for the budget and duration specified.
        For booking links, use the actual destination name in the URLs.
        """

        # Call OpenAI API
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a travel expert who provides personalized destination recommendations. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Parse the response
        import json
        content = response.choices[0].message.content.strip()
        
        # Try to extract JSON from the response
        try:
            # Find JSON in the response
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            data = json.loads(json_str)
            
            destinations = data.get('destinations', [])
        except:
            # Fallback if JSON parsing fails
            destinations = [
                {
                    "name": "Bali, Indonesia",
                    "description": "Perfect for your preferences with beautiful beaches, rich culture, and affordable luxury.",
                    "cost": "$800-1500",
                    "booking_links": {
                        "hotels": "https://www.booking.com/searchresults.html?ss=Bali+Indonesia",
                        "flights": "https://www.expedia.com/Flights-Search?leg1=from:Anywhere,to:Bali+Indonesia",
                        "activities": "https://www.viator.com/Bali-attractions/d98-ttd"
                    }
                },
                {
                    "name": "Porto, Portugal", 
                    "description": "A charming European city with great food, wine, and cultural experiences.",
                    "cost": "$1000-1800",
                    "booking_links": {
                        "hotels": "https://www.booking.com/searchresults.html?ss=Porto+Portugal",
                        "flights": "https://www.expedia.com/Flights-Search?leg1=from:Anywhere,to:Porto+Portugal",
                        "activities": "https://www.viator.com/Porto-attractions/d4611-ttd"
                    }
                },
                {
                    "name": "Costa Rica",
                    "description": "Adventure paradise with rainforests, beaches, and eco-tourism opportunities.",
                    "cost": "$1200-2000",
                    "booking_links": {
                        "hotels": "https://www.booking.com/searchresults.html?ss=Costa+Rica",
                        "flights": "https://www.expedia.com/Flights-Search?leg1=from:Anywhere,to:Costa+Rica",
                        "activities": "https://www.viator.com/Costa-Rica-attractions/d32-ttd"
                    }
                }
            ]

        # Render the results
        return templates.TemplateResponse(
            "results.html", 
            {
                "request": request, 
                "destinations": destinations,
                "budget": budget,
                "style": style,
                "duration": duration
            }
        )

    except Exception as e:
        # Return error message
        return f"""
        <div class="error">
            <h3>Oops! Something went wrong</h3>
            <p>We couldn't generate recommendations right now. Please try again.</p>
            <p><small>Error: {str(e)}</small></p>
        </div>
        """

@app.post("/generate-itinerary", response_class=HTMLResponse)
async def generate_itinerary(
    request: Request,
    destination: str = Form(...),
    budget: str = Form(...),
    style: str = Form(...),
    duration: str = Form(...)
):
    try:
        # Create a detailed itinerary prompt
        prompt = f"""
        Create a detailed day-by-day travel itinerary for {destination} based on these preferences:
        
        Budget: {budget}
        Travel Style: {style}
        Trip Duration: {duration}
        
        For each day, provide:
        1. Day number and theme
        2. Morning activity (with time and location)
        3. Afternoon activity (with time and location)
        4. Evening activity (with time and location)
        5. Recommended restaurants for meals (include restaurant names and brief descriptions)
        6. Estimated daily cost
        
        Format your response as JSON with this structure:
        {{
            "destination": "{destination}",
            "summary": "Brief overview of the trip",
            "itinerary": [
                {{
                    "day": 1,
                    "theme": "Day theme",
                    "morning": "Activity with time and location",
                    "afternoon": "Activity with time and location", 
                    "evening": "Activity with time and location",
                    "meals": {{
                        "breakfast": "Restaurant name and description",
                        "lunch": "Restaurant name and description", 
                        "dinner": "Restaurant name and description"
                    }},
                    "cost": "Estimated daily cost"
                }}
            ],
            "total_cost": "Total estimated cost for the trip"
        }}
        
        Make the itinerary realistic for the budget and duration. Include specific restaurant names and brief descriptions.
        """

        # Call OpenAI API
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a travel expert who creates detailed, personalized itineraries. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        # Parse the response
        import json
        content = response.choices[0].message.content.strip()
        
        try:
            # Find JSON in the response
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            data = json.loads(json_str)
            
            itinerary_data = data
        except:
            # Fallback itinerary
            itinerary_data = {
                "destination": destination,
                "summary": f"A wonderful {duration} trip to {destination} perfect for {style} travelers.",
                "itinerary": [
                    {
                        "day": 1,
                        "theme": "Arrival & Exploration",
                        "morning": "9:00 AM - Arrive and check into hotel",
                        "afternoon": "2:00 PM - Explore the city center and main attractions",
                        "evening": "7:00 PM - Dinner at a local restaurant",
                        "meals": {
                            "breakfast": "Hotel breakfast buffet - Start your day with a variety of local and international options",
                            "lunch": "Local Cafe - Authentic local cuisine in a charming setting",
                            "dinner": "Traditional Restaurant - Experience local flavors and atmosphere"
                        },
                        "cost": "$150-200"
                    },
                    {
                        "day": 2,
                        "theme": "Cultural Immersion",
                        "morning": "9:00 AM - Visit museums and historical sites",
                        "afternoon": "2:00 PM - Guided tour of the city",
                        "evening": "7:00 PM - Evening entertainment",
                        "meals": {
                            "breakfast": "Hotel breakfast - Continental breakfast with local specialties",
                            "lunch": "Museum Cafe - Light lunch with cultural ambiance",
                            "dinner": "Fine Dining Restaurant - Upscale dining experience with local cuisine"
                        },
                        "cost": "$200-250"
                    }
                ],
                "total_cost": "$800-1200"
            }

        # Get TripAdvisor reviews
        reviews = get_tripadvisor_reviews(destination, style)
        
        # Generate restaurant links for each day
        for day in itinerary_data.get('itinerary', []):
            if isinstance(day.get('meals'), dict):
                for meal_type, meal_info in day['meals'].items():
                    # Extract restaurant name from meal info
                    restaurant_name = meal_info.split(' - ')[0] if ' - ' in meal_info else meal_info.split(': ')[-1] if ': ' in meal_info else meal_info
                    day['meals'][meal_type] = {
                        'description': meal_info,
                        'restaurant': restaurant_name,
                        'links': get_restaurant_links(restaurant_name, destination)
                    }
        
        # Render the itinerary
        return templates.TemplateResponse(
            "itinerary.html", 
            {
                "request": request, 
                "itinerary": itinerary_data,
                "reviews": reviews
            }
        )

    except Exception as e:
        return f"""
        <div class="error">
            <h3>Couldn't generate itinerary</h3>
            <p>Please try again. Error: {str(e)}</p>
        </div>
        """

@app.post("/chat")
async def chat_with_ai(chat_message: ChatMessage, request: Request):
    """
    AI chatbot endpoint for travel-related questions
    """
    try:
        # Get any context from the request (like current destination)
        context = ""
        
        # Create a travel-focused prompt
        prompt = f"""
        You are a helpful AI travel assistant. The user asked: "{chat_message.message}"
        
        Please provide a helpful, informative response about travel. You can help with:
        - Travel planning advice
        - Destination recommendations
        - Travel tips and best practices
        - Cultural information
        - Budget planning
        - Safety tips
        - Transportation advice
        - Accommodation suggestions
        - Food and dining recommendations
        - General travel questions
        
        Keep your response conversational, friendly, and informative. If the question is not travel-related, politely redirect to travel topics.
        
        Context: {context}
        """
        
        # Call OpenAI API
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable and friendly AI travel assistant. Provide helpful, accurate, and engaging responses about travel topics. Keep responses conversational and informative."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        return JSONResponse(content={"response": ai_response})
        
    except Exception as e:
        return JSONResponse(
            content={"response": "I'm sorry, I'm having trouble connecting right now. Please try again in a moment."},
            status_code=500
        )
