from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import google.generativeai as genai

@login_required
def homepage(request):
    error_message = None
    user = request.user

    # بررسی موجودی کاربر
    if user.balance < 1000:
        error_message = "موجودی شما کافی نیست."

    return render(request, 'homepage/index.html', {
        'balance': user.balance if not error_message else None,
        'error': error_message,
    })

@login_required
def process_question(request):
    if request.method == 'POST' and request.is_ajax():
        section = request.POST.get('section')  # سکشنی که درخواست از آن ارسال شده است
        question = request.POST.get('question')
        user = request.user

        # بررسی موجودی کاربر
        if user.balance < 1000:
            return JsonResponse({'error': 'موجودی شما کافی نیست.'}, status=400)

        if not question:
            return JsonResponse({'error': 'لطفاً یک سوال وارد کنید.'}, status=400)

        try:
            # تنظیم کلید API و ارسال درخواست به Gemini
            GOOGLE_API_KEY = 'AIzaSyAxFcWDhELaj8iR8QQkGLfrLSdK33yyn-4'
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel('gemini-pro')

            if section == '1':
                prompt = f":به عنوان یک وکیل پاسخ این سوال رو بده و اگر در حوزه تخصص وکیل نیست بگو توی حوزه تو نیست پاسخ دادن به این سوال {question}"
            elif section == '2':
                prompt = f":به عنوان یک متخصص تغذیه پاسخ این سوال رو بده {question}"
            elif section == '3':
                prompt = f":به عنوان یک مشاور خانواده پاسخ این سوال رو بده و اگر در حوزه تخصص مشاور خانواده نیست بگو توی حوزه تو نیست پاسخ دادن به این سوال {question}"
            else:
                return JsonResponse({'error': 'سکشنی معتبر نیست.'}, status=400)

            response = model.generate_content(prompt)
            answer = response.text

            if answer:
                # کسر شارژ از موجودی کاربر
                user.balance -= 1000
                user.save()
                return JsonResponse({'answer': answer})
            else:
                return JsonResponse({'error': 'پاسخی از سرور دریافت نشد.'}, status=500)

        except Exception as e:
            return JsonResponse({'error': f'خطا در پردازش: {str(e)}'}, status=500)

    return JsonResponse({'error': 'درخواست نامعتبر است.'}, status=400)
