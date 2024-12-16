from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import google.generativeai as genai

@login_required
def homepage(request):
    user = request.user
    error_message = None
    if user.balance < 1000:
        error_message = "موجودی شما کافی نیست."

    if request.method == 'POST':
        if error_message:
            return JsonResponse({'error': error_message})

        question = request.POST.get('question')
        section_id = request.POST.get('section_id')

        if question:
            try:
                # API گوگل
                genai.configure(api_key='AIzaSyAxFcWDhELaj8iR8QQkGLfrLSdK33yyn-4')
                model = genai.GenerativeModel('gemini-pro')

                prompts = {
                    '1': f"به عنوان یک وکیل پاسخ بده: {question}",
                    '2': f"به عنوان یک متخصص تغذیه پاسخ بده: {question}",
                    '3': f"به عنوان یک مشاور خانواده پاسخ بده: {question}"
                }

                prompt = prompts.get(section_id, "سوال نامعتبر است.")
                response = model.generate_content(prompt)
                result = response.text if response else "خطایی در دریافت پاسخ رخ داده است."

                # کاهش موجودی
                user.balance -= 1000
                user.save()

                return JsonResponse({'result': result})
            except Exception as e:
                return JsonResponse({'error': "خطایی در پردازش سوال رخ داده است."})

    sections = [
        {'id': '1', 'title': 'پرسش از وکیل', 'description': 'سوالات قضایی خود را مطرح کنید.', 'image': '/img/vakil.jpg'},
        {'id': '2', 'title': 'پرسش از متخصص تغذیه', 'description': 'سوالات تغذیه‌ای خود را بپرسید.', 'image': '/img/taghzie.jpg'},
        {'id': '3', 'title': 'پرسش از مشاور خانواده', 'description': 'سوالات خانوادگی خود را بپرسید.', 'image': '/img/moshaver.jpg'}
    ]

    return render(request, 'homepage/index.html', {
        'user': user,
        'balance': user.balance if not error_message else None,
        'error': error_message,
        'sections': sections
    })
