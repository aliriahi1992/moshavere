from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import google.generativeai as genai

@login_required
def homepage(request):
    result1 = result2 = result3 = None
    error_message = None

    # کسر شارژ از کاربر
    user = request.user
    if user.balance < 1000:
        error_message = "موجودی شما کافی نیست."
        
    # بررسی درخواست POST برای سکشن 1
    if request.method == 'POST' and 'number1' in request.POST:
        number = request.POST.get('number1')
        if number:
            try:
                # تنظیم کلید API و ارسال درخواست به Gemini
                GOOGLE_API_KEY = 'AIzaSyAxFcWDhELaj8iR8QQkGLfrLSdK33yyn-4'
                genai.configure(api_key=GOOGLE_API_KEY)
                model = genai.GenerativeModel('gemini-pro')
                prompt = " :به عنوان یک وکیل پاسخ این سوال رو بده و اگر در حوزه تخصص وکیل نیست بگو توی حوزه تو نیست پاسخ دادن به این سوال " + str(number)
                response = model.generate_content(prompt)
                result1 = response.text
                if result1 is not None :
                    user.balance -= 1000
                    user.save()  # ذخیره تغییرات در دیتابیس
            except ValueError:
                result1 = "لطفاً یک عدد صحیح وارد کنید"

    # بررسی درخواست POST برای سکشن 2
    if request.method == 'POST' and 'number2' in request.POST:
        number = request.POST.get('number2')
        if number:
            try:
                # تنظیم کلید API و ارسال درخواست به Gemini
                GOOGLE_API_KEY = 'AIzaSyAxFcWDhELaj8iR8QQkGLfrLSdK33yyn-4'
                genai.configure(api_key=GOOGLE_API_KEY)
                model = genai.GenerativeModel('gemini-pro')
                prompt = " :به عنوان یک متخصص تغذیه پاسخ این سوال رو بده " + str(number)
                response = model.generate_content(prompt)
                result2 = response.text
                if result2 is not None :
                    user.balance -= 1000
                    user.save()  # ذخیره تغییرات در دیتابیس                
            except ValueError:
                result2 = "لطفاً یک عدد صحیح وارد کنید"

    # بررسی درخواست POST برای سکشن 3
    if request.method == 'POST' and 'number3' in request.POST:
        number = request.POST.get('number3')
        if number:
            try:
                # تنظیم کلید API و ارسال درخواست به Gemini
                GOOGLE_API_KEY = 'AIzaSyAxFcWDhELaj8iR8QQkGLfrLSdK33yyn-4'
                genai.configure(api_key=GOOGLE_API_KEY)
                model = genai.GenerativeModel('gemini-pro')
                prompt = " :به عنوان یک مشاور خانواده پاسخ این سوال رو بده و اگر در حوزه تخصص مشاور خانواده نیست بگو توی حوزه تو نیست پاسخ دادن به این سوال " + str(number)
                response = model.generate_content(prompt)
                result3 = response.text
                if result3 is not None :
                    user.balance -= 1000
                    user.save()  # ذخیره تغییرات در دیتابیس                
            except ValueError:
                result3 = "لطفاً یک عدد صحیح وارد کنید"

    # رندر کردن قالب همراه با داده‌های لازم
    return render(request, 'homepage/index.html', {
        'result1': result1,
        'result2': result2,
        'result3': result3,
        'balance': user.balance if not error_message else None,  # نمایش شارژ فقط در صورت موجودی کافی
        'error': error_message  # نمایش خطا در صورت کمبود موجودی
    })
