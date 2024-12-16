from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import google.generativeai as genai

@login_required
def homepage(request):
    error_message = None
    user = request.user

    # چک کردن موجودی کاربر
    if user.balance < 1000:
        error_message = "موجودی شما کافی نیست."

    if request.method == 'POST':
        section = request.POST.get('section')  # تشخیص سکشن ارسال شده
        question = request.POST.get('question')
        result = None

        if section and question and not error_message:
            try:
                # تنظیم کلید API و مدل Gemini
                GOOGLE_API_KEY = 'AIzaSyAxFcWDhELaj8iR8QQkGLfrLSdK33yyn-4'
                genai.configure(api_key=GOOGLE_API_KEY)
                model = genai.GenerativeModel('gemini-pro')

                # تولید prompt بر اساس سکشن
                prompts = {
                    '1': f":به عنوان یک وکیل پاسخ این سوال رو بده و اگر در حوزه تخصص وکیل نیست بگو توی حوزه تو نیست پاسخ دادن به این سوال {question}",
                    '2': f":به عنوان یک متخصص تغذیه پاسخ این سوال رو بده {question}",
                    '3': f":به عنوان یک مشاور خانواده پاسخ این سوال رو بده و اگر در حوزه تخصص مشاور خانواده نیست بگو توی حوزه تو نیست پاسخ دادن به این سوال {question}"
                }

                if section in prompts:
                    prompt = prompts[section]
                    response = model.generate_content(prompt)
                    result = response.text

                    if result:
                        # کسر موجودی و ذخیره
                        user.balance -= 1000
                        user.save()

            except Exception as e:
                result = "خطایی در پردازش درخواست رخ داده است."

        # بازگشت پاسخ به صورت JSON
        return JsonResponse({
            'result': result,
            'balance': user.balance if not error_message else None,
            'error': error_message
        })

    return render(request, 'homepage/index.html', {
        'balance': user.balance,
        'error': error_message
    })
