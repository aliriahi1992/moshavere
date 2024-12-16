from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse  # اضافه کردن JsonResponse
import google.generativeai as genai

@login_required
def homepage(request):
    if request.method == 'POST' and request.is_ajax(): # بررسی درخواست AJAX
        number = request.POST.get('number')
        section = request.POST.get('section') # دریافت شماره سکشن
        if number and section:
            try:
                GOOGLE_API_KEY = 'AIzaSyAxFcWDhELaj8iR8QQkGLfrLSdK33yyn-4' #کلید API خود را قرار دهید
                genai.configure(api_key=GOOGLE_API_KEY)
                model = genai.GenerativeModel('gemini-pro')
                prompt = f":به عنوان یک {'وکیل' if section == '1' else 'متخصص تغذیه' if section == '2' else 'مشاور خانواده'} پاسخ این سوال رو بده و اگر در حوزه تخصص {'وکیل' if section == '1' else 'متخصص تغذیه' if section == '2' else 'مشاور خانواده'} نیست بگو توی حوزه تو نیست پاسخ دادن به این سوال {number}"
                response = model.generate_content(prompt)
                result = response.text
                if result:
                    user = request.user
                    if user.balance >= 1000:
                        user.balance -= 1000
                        user.save()
                        return JsonResponse({'result': result, 'balance': user.balance}) # ارسال پاسخ به صورت JSON
                    else:
                        return JsonResponse({'error': "موجودی شما کافی نیست."})
                else:
                    return JsonResponse({'error': "خطا در دریافت پاسخ از Gemini"})
            except ValueError:
                return JsonResponse({'error': "لطفاً یک ورودی معتبر وارد کنید."})
            except Exception as e: # گرفتن سایر خطاها مانند خطای اتصال به Gemini
                return JsonResponse({'error': str(e)})
    else:
        user = request.user
        return render(request, 'homepage/index.html', {'balance': user.balance})