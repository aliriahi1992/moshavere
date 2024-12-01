from django.shortcuts import render
import google.generativeai as genai
import requests


def homepage(request):
    result1 = result2 = result3 = None

    # بررسی درخواست POST برای سکشن 1
    if request.method == 'POST' and 'number1' in request.POST:
        number = request.POST.get('number1')
        if number:
            try:

                # دریافت کلید API از تنظیمات یا دیتابیس
                GOOGLE_API_KEY = 'AIzaSyAxFcWDhELaj8iR8QQkGLfrLSdK33yyn-4'  # یا استفاده از userdata.get('API_KEY_1')
                genai.configure(api_key=GOOGLE_API_KEY)
                # انتخاب مدل و ارسال درخواست به Gemini
                model = genai.GenerativeModel('gemini-pro')
                # فرض می‌کنیم که می‌خواهیم از دو عدد برای تولید محتوای خاص استفاده کنیم
                prompt = "به عنوان یک وکیل به این سوال پاسخ بده با توجه به قوانین ایران و اگر این سوال در حوزه قضایی نیست بگو در حوزه تو نیست پاسخ دادن بهش"
                response = model.generate_content(prompt)
                # اینجا باید پاسخ مدل را پردازش کنید
                result1 = response.text

            except ValueError:
                result1 = "لطفاً یک عدد صحیح وارد کنید"

    # بررسی درخواست POST برای سکشن 2
    if request.method == 'POST' and 'number2' in request.POST:
        number = request.POST.get('number2')
        if number:
            try:

                # دریافت کلید API از تنظیمات یا دیتابیس
                GOOGLE_API_KEY = 'AIzaSyAxFcWDhELaj8iR8QQkGLfrLSdK33yyn-4'  # یا استفاده از userdata.get('API_KEY_1')
                genai.configure(api_key=GOOGLE_API_KEY)
                # انتخاب مدل و ارسال درخواست به Gemini
                model = genai.GenerativeModel('gemini-pro')
                # فرض می‌کنیم که می‌خواهیم از دو عدد برای تولید محتوای خاص استفاده کنیم
                prompt = "به عنوان یک متخصص تغذیه به این سوال جواب بده و اگر در حوزه تغذیه نیست بگو در حوزه تو نیست پاسخ دادن بهش"
                response = model.generate_content(prompt)
                # اینجا باید پاسخ مدل را پردازش کنید
                result2 = response.text

            except ValueError:
                result2 = "لطفاً یک عدد صحیح وارد کنید"

    # بررسی درخواست POST برای سکشن 3
    if request.method == 'POST' and 'number3' in request.POST:
        number = request.POST.get('number3')
        if number:
            try:

                # دریافت کلید API از تنظیمات یا دیتابیس
                GOOGLE_API_KEY = 'AIzaSyAxFcWDhELaj8iR8QQkGLfrLSdK33yyn-4'  # یا استفاده از userdata.get('API_KEY_1')
                genai.configure(api_key=GOOGLE_API_KEY)
                # انتخاب مدل و ارسال درخواست به Gemini
                model = genai.GenerativeModel('gemini-pro')
                # فرض می‌کنیم که می‌خواهیم از دو عدد برای تولید محتوای خاص استفاده کنیم
                prompt = "به عنوان یک مشاور خانواده پاسخ این سوال رو بده و اگر در حوزه مشاور نیست بگو در حوزه تو نیست پاسخ دادن بهش"
                response = model.generate_content(prompt)
                # اینجا باید پاسخ مدل را پردازش کنید
                result3 = response.text

            except ValueError:
                result3 = "لطفاً یک عدد صحیح وارد کنید"

    return render(request, 'homepage/index.html', {
        'result1': result1,
        'result2': result2,
        'result3': result3
    })
