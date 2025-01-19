from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import google.generativeai as genai
import os
#برای زرین پال
from django.conf import settings
import requests
import json
from django.http import HttpResponse , JsonResponse
from django.shortcuts import redirect
#برای ذخیره سازی سوابق تراکنش ها در مدل دیتای جنگو
from .models import TransactionHistory 
from datetime import datetime
#برای ذخیره سازی سوابق سوالات پرسیده شده توسط کاربران
from .models import QuestionHistory 

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
        #number همان سوال کاربر است که از سمت فرانت می آید
        number = request.POST.get('number')
        #مقادیری که از سمت مرورگر جهت ذخیره سازی در دیتابیس ارسال می شوند
        user_phone_number = request.POST.get('user_phone_number')
        user_full_name = request.POST.get('user_full_name')
        question = request.POST.get('number')
        credit = request.POST.get('credit')
        user_os = request.POST.get('user_os')
        #مقدار دهی اولیه به پارامتر هایی که از سمت مرورگر نیامده اند
        from_who = ""
        api_key_name = ""
        status =""


        #مقداردهی متغیری که باید در دیتابیس ذخیره شود
        if section == 1:
            from_who = "متخصص پوست و مو"
        elif section == 2:
            from_who = "استاد"            
        elif section == 2:
            from_who = "استاد"
        elif section == 3: 
            from_who = "مشاور خانواده"    
        elif section == 4:
            from_who = "متخصص تغذیه"
        elif section == 5:  
            from_who = "مربی"
        elif section == 6: 
            from_who = "وکیل" 
        elif section == 7:
            from_who = "مشاور تحصیلی"
        elif section == 8:   
            from_who = "پزشک" 
        elif section == 9:   
            from_who = "مشاور کسب و کار"   
        elif section == 10:  
            from_who = "متخصص بازار های مالی"
        elif section == 11:  
            from_who = "مشاور مهاجرت" 
        elif section == 12: 
            from_who = "برنامه نویس"  
        elif section == 13: 
            from_who = "مشاور خرید" 
        elif section == 14: 
            from_who = "تعمیر کار"  
        elif section == 15: 
            from_who = "مشاور سرمایه گذاری"                           
                     

        if number:
            try:
                GOOGLE_API_KEY = os.getenv('API_KEY_1')
                #مقدار دهی به متغیر های ذخیره سازی در دیتابیس
                api_key_name = "API_KEY_1"

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
                elif section == 14:
                    prompt = "به عنوان یک تعمیر کار پاسخ این سوال رو بده " + str(number)
                elif section == 15:
                    prompt = "به عنوان یک مشاور سرمایه گذاری پاسخ این سوال رو بده " + str(number)


                response = model.generate_content(prompt)
                result = response.text
                result = result.replace("*", "")
                if result:
                    user.balance -= 1000
                    user.save()
                    #مقدار دهی به متغیر های ذخیره سازی در دیتابیس
                    status = "Answered"                     

            except ValueError:
                result = "محدودیت هایی در پاسخگویی به این سوالات برای من وجود دارد و متاسفانه نمی توانم پاسخ این سوال شما را بدهم."
                #مقدار دهی به متغیر های ذخیره سازی در دیتابیس
                status = "Unable to respond" 
            except Exception as e:
                #مقدار دهی به متغیر های ذخیره سازی در دیتابیس
                status = "Error"  

                #ذخیره سازی سوال کاربر و متغیر های مورد نیاز دیگر در دیتابیس
                question = QuestionHistory(
                    created_at = datetime.now(),
                    status = status,
                    user_phone_number = user_phone_number,
                    user_full_name = user_full_name,
                    question = question,
                    from_who = from_who,
                    api_key_name = api_key_name,
                    credit = credit,
                    user_os = user_os
                )
                question.save()                

                return JsonResponse({'error': str(e)})


            #ذخیره سازی سوال کاربر و متغیر های مورد نیاز دیگر در دیتابیس
            question = QuestionHistory(
                created_at = datetime.now(),
                status = status,
                user_phone_number = user_phone_number,
                user_full_name = user_full_name,
                question = question,
                from_who = from_who,
                api_key_name = api_key_name,
                credit = credit,
                user_os = user_os
            )
            question.save()




    return JsonResponse({'result': result, 'balance': user.balance})



ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"


currency = "IRR"  # or "IRT"

# کد مرچنت خود را در فایل settings وارد کنید

# Required Data
amount = 20000  # Based on your currency
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://beporsimige.ir/homepage/'


# Important: need to edit for a real server.


def send_request(request):
    if request.method == 'POST':
        #دریافت متغیر های ارسالی به درگاه از صفحه وب سمت مشتری
        data = json.loads(request.body)
        amount = data.get('amount')
        orginal_price = data.get('orginal_price')
        mobile = data.get('mobile')
        description = data.get('description')
        order_id = data.get('order_id')
        email = data.get('email')
        #مقادیر اختصاصی جهت ثبت در دیتا مدل سوابق تراکنش خودمان در جنگو
        user_full_name = data.get('user_full_name')
        discount_code = data.get('discount_code')
        initial_credit = data.get('initial_credit')
        user_os = data.get('user_os')



        metadata = {
	    "mobile": mobile,  # Buyer phone number Must start with 09
	    "email": email,  # Buyer Email
	    "order_id": order_id,  # Order Id
        }



        if not amount:
            return JsonResponse({'status': False, 'error': 'مقدار نامعتبر است.'})

        # داده‌های مورد نیاز برای زرین پال
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": int(amount),
            "currency": currency,
            "description": description,
            "callback_url": CallbackURL,
            "metadata": metadata
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'accept': 'application/json'}

        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            response = response.json()
            err = response.get("errors")
            if err:
                return JsonResponse(err, content_type="application/json", safe=False)
            if response['data']['code'] == 100:

                #استفاده از مفهوم سشن برای ذخیره سازی اطلاعات پرداخت کاربر در زمان ارسال به درگاه و بازگشت از درگاه ، این مقادیر جلوتر در تابع وریفای از سشن استخراج می شوند
                request.session['user_phone_number'] = str(mobile)
                request.session['user_full_name'] = str(user_full_name)
                request.session['amount'] = int(amount)
                request.session['orginal_price'] = int(orginal_price)
                request.session['discount_code'] = str(discount_code)
                request.session['initial_credit'] = str(initial_credit)
                request.session['user_os'] = str(user_os)

                url = ZP_API_STARTPAY + str(response['data']['authority'])
                return JsonResponse({'url': url})
            else:
                return JsonResponse({'status': False, 'code': str(response['data']['code'])})
        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'error': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'error': 'اتصال برقرار نشد'})

    return JsonResponse({'status': False, 'error': 'درخواست نامعتبر است.'})


@login_required
def verify(request):
    #جهت افزایش اعتبار یوزر 
    user = request.user
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    if status == "NOK":
       
        #ذخیره سازی سابقه تراکنش به عنوان تراکنشی نا موفق
        transaction = TransactionHistory(
            created_at = datetime.now(),
            status = "NOK",
            user_phone_number = request.session.get('user_phone_number'),
            user_full_name = request.session.get('user_full_name'),
            orginal_price = request.session.get('orginal_price'),
            amount = request.session.get('amount'),
            ref_id = "",
            discount_code = request.session.get('discount_code'),
            initial_credit = request.session.get('initial_credit'),
            secondary_credit = request.session.get('initial_credit'),
            user_os = request.session.get('user_os')
        )
        transaction.save()


        return JsonResponse({'status': False, 'message': "پرداخت ناموفق"})

    data = {
        "merchant_id": settings.MERCHANT,
        #استفاده از مفهوم سشن برای ذخیره سازی اطلاعات پرداخت کاربر در زمان ارسال به درگاه و بازگشت از درگاه
        "amount" : request.session.get('amount'),
        "authority": authority,
    }
    headers = {'content-type': 'application/json', 'accept': 'application/json'}
    try:
        response = requests.post(ZP_API_VERIFY, data=json.dumps(data), headers=headers)
        response = response.json()
        if response['data']['code'] == 100:

            #جهت افزایش اعتبار یوزر 
            user.balance += request.session.get('orginal_price')/10
            user.save()

            
            #ذخیره سازی سابقه تراکنش به عنوان تراکنشی نا موفق
            transaction = TransactionHistory(
                created_at = datetime.now(),
                status = "OK",
                user_phone_number = request.session.get('user_phone_number'),
                user_full_name = request.session.get('user_full_name'),
                orginal_price = request.session.get('orginal_price'),
                amount = request.session.get('amount'),
                ref_id = response['data']['ref_id'],
                discount_code = request.session.get('discount_code'),
                initial_credit = request.session.get('initial_credit'),
                secondary_credit = int(request.session.get('initial_credit')) + int(request.session.get('orginal_price'))/10,
                user_os = request.session.get('user_os')
            )
            transaction.save()           
            

            return JsonResponse({'status': True, 'message': 'پرداخت موفق', 'ref_id': response['data']['ref_id']})



        else:
            return JsonResponse({'status': False, 'message': 'پرداخت ناموفق', 'data': response})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'message': 'اتصال برقرار نشد'})
