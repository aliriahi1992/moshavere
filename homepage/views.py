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
                GOOGLE_API_KEY = 'AIzaSyAxFcWDhELaj8iR8QQkGLfrLSdK33yyn-4'
                genai.configure(api_key=GOOGLE_API_KEY)
                model = genai.GenerativeModel('gemini-pro')

                if section == 1:
                    prompt = "به عنوان یک مشاور در زمینه پوست و مو پاسخ این سوال رو بده " + str(number)
                elif section == 2:
                    prompt = "به عنوان یک استاد علمی و دانشگاهی و معلم پاسخ این سوال رو بده و اگر در حوزه علم و درس نیست بگو توی حوزه تو نیست پاسخ دادن به این سوال " + str(number)
                elif section == 3:
                    prompt = "به عنوان یک مشاور امور اجتماعی و خانوادگی و فردی پاسخ این سوال رو بده " + str(number)
                elif section == 4:
                    prompt = "به عنوان یک متخصص تغذیه و رژیم درمانی پاسخ این سوال رو بده " + str(number)
                elif section == 5:
                    prompt = "به عنوان یک مربی ورزشی پاسخ این سوال رو بده " + str(number)
                elif section == 6:
                    prompt = "به عنوان یک فرد آگاه از مسائل حقوقی و قضایی پاسخ این سوال رو بده " + str(number)
                elif section == 7:
                    prompt = "به عنوان یک فرد مشاور تحصیلی پاسخ این سوال رو بده " + str(number)
                elif section == 8:
                    prompt = "به عنوان یک پزشک پاسخ این سوال رو بده " + str(number)
                elif section == 9:
                    prompt = "به عنوان یک مشاور کسب و کار پاسخ این سوال رو بده " + str(number)
                elif section == 10:
                    prompt = "به عنوان یک متخصص بازار های مالی پاسخ این سوال رو بده " + str(number)
                elif section == 11:
                    prompt = "به عنوان یک مشاور امور مهاجرت پاسخ این سوال رو بده " + str(number)
                elif section == 12:
                    prompt = "به عنوان یک برنامه نویس پاسخ این سوال رو بده " + str(number)
                elif section == 13:
                    prompt = "به عنوان یک مشاور خرید محصول پاسخ این سوال رو بده " + str(number)

                response = model.generate_content(prompt)
                result = response.text
                result = result.replace("*", "")
                if result:
                    user.balance -= 1000
                    user.save()
            except ValueError:
                result = "لطفاً یک عدد صحیح وارد کنید"
            except Exception as e:
                return JsonResponse({'error': str(e)})
    
    return JsonResponse({'result': result, 'balance': user.balance})
