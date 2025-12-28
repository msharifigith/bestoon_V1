import openai
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

# Make sure to add your OpenAI API key to settings
openai.api_key = settings.OPENAI_API_KEY


def get_ai_response(user_message):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the appropriate engine (like GPT-3 or GPT-4)
            prompt=user_message,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)


def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        ai_response = get_ai_response(user_message)
        return JsonResponse({"response": ai_response})

    return render(request, 'chatAI/chat.html')
