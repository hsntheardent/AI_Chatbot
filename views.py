from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 
from difflib import SequenceMatcher
import json
import os
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"
KNOWLEDGE_FILE = os.path.join("app", "knowledge.json")  

def load_knowledge_base(): # function define
    """Load pre-written website info or FAQs from JSON file"""# Triple quotes """ ... """ ke andar jo likha hai, wo docstring kehlata hai,short description dena → “ye function kya karta hai”
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f: 
            return json.load(f)
    return {} # Matlab agar JSON file exist na kare, to function empty dictionary return kare
knowledge_base = load_knowledge_base()


def similar(a, b):
    """Return a similarity ratio between 0 and 1"""
    return SequenceMatcher(None, a, b).ratio()# Python ka built-in tool from difflib ::Purpose: Do sequences (strings) ke beech similarity measure karna


def search_knowledge_base(question, threshold=0.65):
    """
    Smart knowledge search:
    1️⃣ Keyword-based instant detection
    2️⃣ Fuzzy matching (SequenceMatcher)
    3️⃣ Multiple keyword fallback (priority-based)
    """ 
    question_lower = question.lower().strip()
    best_match = None
    highest_score = 0

    keywords = {
        "about": "about store",
        "store": "about store",
        "product": "damaged product",
        "products": "product categories",
        "categories": "product categories",
        "shirts": "shirts collection",
        "shirt": "shirts collection",
        "pants": "pants collection",
        "trousers": "pants collection",
        "jeans": "pants collection",
        "shoes": "shoes collection",
        "footwear": "shoes collection",
        "materials": "materials and quality",
        "quality": "materials and quality",
        "size": "size and fitting",
        "fitting": "size and fitting",
        "wash": "washing instructions",
        "washing": "washing instructions",
        "new arrivals": "new arrivals",
        "new": "new arrivals",
        "best sellers": "best sellers",
        "bestsellers": "best sellers",
        "shipping": "shipping policy",
        "delivery": "delivery charges",
        "express": "express delivery",
        "track": "order tracking",
        "tracking": "order tracking",
        "delay": "delayed order",
        "payment": "payment methods",
        "cod": "cod charges",
        "return": "return policy",
        "exchange": "exchange policy",
        "refund": "refund policy",
        "pickup": "return pickup",
        "cancel": "order cancellation",
        "order": "how to order",
        "account": "account creation",
        "gift": "gift wrapping",
        "bulk": "bulk or wholesale order",
        "wholesale": "bulk or wholesale order",
        "discount": "discount offers",
        "offers": "discount offers",
        "newsletter": "newsletter subscription",
        "timings": "store timings",
        "contact": "contact support",
        "support": "customer support",
        "privacy": "security and privacy",
        "security": "security and privacy",
        "warranty": "product warranty",
        "track order": "how to track order",
        "out of stock": "out of stock products",
        "international": "international shipping",
        "how to contact": "how to contact",
        "shirt sizes": "shirt sizes",
        "pant sizes": "pant sizes",
        "availability": "size availability",
        "size chart": "size chart",
        "fit": "fit types",
        "fabric": "fabric types",
        "cotton": "cotton fabric",
        "denim": "denim fabric",
        "linen": "linen fabric",
        "polyester": "polyester fabric",
        "stretch": "stretch jeans",
        "formal pants": "formal pants",
        "casual pants": "casual pants",
        "jeans colors": "jeans colors",
        "shirt colors": "shirt colors",
        "color variation": "color variation",
        "stock": "stock availability",
        "restock": "restock update",
        "sale": "sale section",
        "discount percentage": "discount percentage",
        "clearance": "clearance sale",
        "price": "price range",
        "premium": "premium collection",
        "casual": "casual wear",
        "formal": "formal wear",
        "party": "party wear",
        "embroidered": "embroidered shirts",
        "plain": "plain shirts",
        "printed": "printed shirts",
        "checked": "checked shirts",
        "half sleeves": "half sleeves",
        "full sleeves": "full sleeves",
        "collar": "collar types",
        "button": "button quality",
        "stitching": "stitching quality",
        "waist": "waist size",
        "inseam": "inseam length",
        "stretch pants": "stretch pants",
        "durability": "fabric durability",
        "care": "washing care",
        "ironing": "ironing instructions",
        "shrinkage": "shrinkage",
        "breathable": "breathable fabric",
        "color fading": "color fading",
        "made in pakistan": "made in pakistan",
        "imported": "imported fabric",
        "eco": "eco friendly",
        "sizes": "available sizes",
        "plus size": "plus size",
        "youth": "youth sizes",
        "kids": "kids wear",
        "women": "women collection",
        "men": "men collection",
        "unisex": "unisex products",
        "hoodies": "hoodies",
        "winter": "winter wear",
        "summer": "summer wear",
        "sportswear": "sportswear",
        "joggers": "joggers",
        "cargo": "cargo pants",
        "tshirt": "t shirts",
        "t-shirts": "t shirts",
        "polo": "polo shirts",
        "round neck": "round neck",
        "v neck": "v neck",
        "printed t shirts": "printed t shirts",
        "plain t shirts": "plain t shirts",
        "black shirt": "black shirt",
        "white shirt": "white shirt",
        "blue jeans": "blue jeans",
        "black jeans": "black jeans",
        "ripped jeans": "ripped jeans",
        "chinos": "chinos",
        "formal trousers": "formal trousers",
        "belt": "belt loops",
        "pockets": "pockets",
        "zipper": "zipper quality",
        "origin": "product origin",
        "in stock": "in stock",
        "limited": "limited edition",
        "ready": "ready to ship",
        "pre order": "pre order"
    }

    for word, key in keywords.items():
        if word in question_lower and key in knowledge_base:
            return knowledge_base[key]

    for key, answer in knowledge_base.items():
        score = similar(question_lower, key.lower())
        if score > highest_score:
            highest_score = score
            best_match = answer

    if highest_score >= threshold:
        return best_match

    return None



def ask_ollama(user_input):
    """Query Ollama's local model and return the response text"""
    # ✅ Add instruction to avoid movies/pop culture references
    instruction = (
        "Reply in a normal, casual tone. "
        "Do NOT include any pop culture, movie, or song references. "
        "Just answer naturally."
    )
    final_prompt = f"{instruction}\nUser: {user_input}"
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": final_prompt, "stream": False},
            timeout=60
        )
        if response.status_code != 200:
            return f"⚠️ Model error ({response.status_code}): {response.text}"
        data = response.json()
        return data.get("response", "No response from model.")
    except requests.exceptions.RequestException as e:
        return f"⚠️ Error connecting to Ollama: {str(e)}"



def chat_view(request):
    """Render chatbot UI"""
    return render(request, "chatbot.html")


# 1
@csrf_exempt
def chat(request):
    """Handle AJAX chat requests from frontend"""
    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request method."}, status=405)
    try:
        data = json.loads(request.body)
        question = data.get("message", "").strip()
    except Exception:
        return JsonResponse({"reply": "Invalid JSON payload."}, status=400)
    if not question:
        return JsonResponse({"reply": "Please type a message."})
    answer = search_knowledge_base(question)
    if not answer:
        answer = ask_ollama(question)
    return JsonResponse({"reply": answer})
