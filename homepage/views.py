from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
import json



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

@csrf_exempt
def process_question(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            section = data.get('section')
            question = data.get('question')

            if not question:
                return JsonResponse({'error': 'سوال نمی‌تواند خالی باشد.'}, status=400)

            # پردازش سوال بر اساس بخش (section)
            if section == 1:
                answer = f"پاسخ به سوال وکیل: {question}"
            elif section == 2:
                answer = f"پاسخ به سوال تغذیه: {question}"
            elif section == 3:
                answer = f"پاسخ به سوال مشاور خانواده: {question}"
            else:
                return JsonResponse({'error': 'بخش نامعتبر است.'}, status=400)

            return JsonResponse({'answer': answer}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'درخواست نامعتبر است.'}, status=400)
    else:
        return JsonResponse({'error': 'تنها درخواست‌های AJAX از نوع POST پذیرفته می‌شوند.'}, status=400)