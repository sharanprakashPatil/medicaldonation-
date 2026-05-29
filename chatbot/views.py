import json
import difflib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .faq_data import FAQ, GREETINGS, DEFAULT_RESPONSE

@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)
    try:
        body = json.loads(request.body)
        message = body.get("message", "").strip().lower()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not message:
        return JsonResponse({"answer": "Please type a question."})

    for keyword, reply in GREETINGS.items():
        if message == keyword or message.startswith(keyword):
            return JsonResponse({"answer": reply})

    questions = [faq["question"].lower() for faq in FAQ]
    matches = difflib.get_close_matches(message, questions, n=1, cutoff=0.3)
    if matches:
        for faq in FAQ:
            if faq["question"].lower() == matches[0]:
                return JsonResponse({"answer": faq["answer"]})

    words = message.split()
    for faq in FAQ:
        faq_words = set(faq["question"].lower().split())
        if faq_words & set(words):
            return JsonResponse({"answer": faq["answer"]})

    return JsonResponse({"answer": DEFAULT_RESPONSE})
