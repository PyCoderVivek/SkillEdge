from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

# Load API key from settings
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def chatbot_page(request):
    """Render the chatbot page."""
    return render(request, "ChatBot/chatbot.html")

@csrf_exempt  # TEMPORARY: Remove this in production
def chatbot_api(request):
    """Handle user messages and return chatbot response."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message")

            if user_message:
                response = model.generate_content(user_message)
                return JsonResponse({"reply": response.text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
