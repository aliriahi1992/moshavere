from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import google.generativeai as genai
import os

@login_required
def homepage(request):
    return render(request, 'homepage/index.html', {'balance': request.user.balance})

@login_required
def ask_question(request, section):
    user = request.user
    result = None
    error_message = None

    if user.balance < 1000:
        return JsonResponse({'error': 'موجودی شما کافی نیست.'})

    if request.method == 'POST':
        number = request.POST.get('number')
        if number:
            try:
                GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
                genai.configure(api_key=GOOGLE_API_KEY)
                model = genai.GenerativeModel('gemini-pro')
                if section == '1':
                    prompt = "به عنوان یک وکیل پاسخ این سوال رو بده و اگر در حوزه تخصص وکیل نیست بگو توی حوزه تو نیست پاسخ دادن به این سوال " + str(number)
                elif section == '2':
                    prompt = "به عنوان یک متخصص تغذیه پاسخ این سوال رو بده " + str(number)
                elif section == '3':
                    prompt = "به عنوان یک مشاور خانواده پاسخ این سوال رو بده و اگر در حوزه تخصص مشاور خانواده نیست بگو توی حوزه تو نیست پاسخ دادن به این سوال " + str(number)
                response = model.generate_content(prompt)
                result = response.text
                if result:
                    user.balance -= 1000
                    user.save()
            except ValueError:
                result = "لطفاً یک عدد صحیح وارد کنید"
            except Exception as e:
                return JsonResponse({'error': str(e)})
    
    return JsonResponse({'result': result, 'balance': user.balance})
