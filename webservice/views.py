from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from accounts.models import CustomUser
import os
import requests
import google.generativeai as genai
from django.contrib.auth.decorators import login_required
#برای ذخیره سازی سوابق سوالات پرسیده شده توسط کاربران
from homepage.models import QuestionHistory
#برای زرین پال
from django.conf import settings
import requests
import json
from django.http import HttpResponse , JsonResponse
from django.shortcuts import redirect
#برای ذخیره سازی سوابق تراکنش ها در مدل دیتای جنگو
from homepage.models import TransactionHistory 
from datetime import datetime



@login_required
def homepage(request):
    user = request.user
    user_questions = QuestionHistory.objects.filter(user_phone_number=user.mobile_number).order_by('-created_at')  # آخرین سوالات اول نمایش داده شوند
    return render(request, 'webservice/index.html', {'balance': user.balance, 'user_questions': user_questions, 'webservice_discount_code': user.webservice_discount_code , 'webservice_campaign_name': user.webservice_campaign_name , 'webservice_total_request_limit': user.webservice_total_request_limit, 'webservice_user_request_limit': user.webservice_user_request_limit, 'webservice_question_price': user.webservice_question_price})


@login_required
def user_questions(request):
    if request.user.is_authenticated:  # بررسی اینکه کاربر لاگین کرده باشد
        user_mobile_number = request.user.mobile_number  # دریافت شماره موبایل کاربر لاگین‌شده
        questions = QuestionHistory.objects.filter(user_phone_number=user_mobile_number).order_by('-created_at')  # فیلتر سوالات کاربر
        
        # تست برای بررسی دریافت داده‌ها
        print("User Mobile Number:", user_mobile_number)  # چک کردن شماره موبایل
        print("Questions Retrieved:", questions)  # بررسی سوالات در ترمینال
    else:
        questions = []

    return render(request, 'webservice/index.html', {'questions': questions})




@csrf_exempt
def update_ai_settings(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        user.webservice_total_request_limit = data.get('requests_per_hour', 10000)
        user.webservice_user_request_limit = data.get('user_requests_per_hour', 30)

        #برای اینکه فیلد خالی در دیتابیس ذخیره نشود
        if data.get('discount_code') == "" :
            user.webservice_discount_code = None
        else :
            user.webservice_discount_code =  data.get('discount_code')

        #برای اینکه فیلد خالی در دیتابیس ذخیره نشود
        if data.get('campaign_name') == "" :
            user.webservice_campaign_name = None
        else :
            user.webservice_campaign_name =  data.get('campaign_name')

        user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)




@csrf_exempt  # برای جلوگیری از مشکلات CSRF در درخواست‌های POST
def webservice_chat_view(request):
    if request.method == "POST":
        try:
            # دریافت داده‌های درخواست
            data = json.loads(request.body)
            question = data.get("question")
            mobile = request.headers.get("X-Mobile")
            webservice_user = request.headers.get("X-User")
            webservice_user_os = request.headers.get("X-OS")
            #دریافت اورجین و ریفرر از ریکوئست جهت تشخیص اینکه درخواست از کدام وبسایت آمده
            # همچنین استفاده از ریفرر به این خاطر است که استثنائا در وبسایت بپرسی میگه ممکن است برای دمو روی یک اورجین چندین ریکوئست بیاید
            #در این حالت از ریفرر برای یکتا کردن کاربران استفاده میکنیم و برای بقیه دامنه ها از اورجین استفاده می شود
            request_origin = request.headers.get("Origin")
            request_Referer = request.headers.get("Referer")
            if request_origin == "https://beporsimige.ir" :
                origin = request_Referer
            else :
                origin = request_origin    
            

            user = CustomUser.objects.filter(webservice_origin=origin, is_webservice=True).first()
    
            if user :
                if user.balance >0 :    
                    section = user.webservice_from_who

                    #مقداردهی متغیری که باید در دیتابیس ذخیره شود
                    if section == 1:
                        from_who = "مشاور پوست و مو"
                    elif section == 2:
                        from_who = "استاد"            
                    elif section == 3: 
                        from_who = "مشاور"    
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
                    elif section == 16: 
                        from_who = "متخصص موبایل و کامپیوتر"  


                    try:
                        GOOGLE_API_KEY = os.getenv('API_KEY_1')
                        #مقدار دهی به متغیر های ذخیره سازی در دیتابیس
                        api_key_name = "API_KEY_1"

                        genai.configure(api_key=GOOGLE_API_KEY)
                        model = genai.GenerativeModel('gemini-pro')





                        if section == 1:
                            who = "به عنوان یک مشاور در زمینه پوست و مو پاسخ این سوال رو بده "
                        elif section == 2:
                            who = "به عنوان یک استاد علمی و دانشگاهی و معلم پاسخ این سوال رو بده  "
                        elif section == 3:
                            who = "به عنوان یک مشاور امور اجتماعی و خانوادگی و فردی پاسخ این سوال رو بده "
                        elif section == 4:
                            who = "به عنوان یک متخصص تغذیه و رژیم درمانی پاسخ این سوال رو بده "
                        elif section == 5:
                            who = "به عنوان یک مربی ورزشی پاسخ این سوال رو بده "
                        elif section == 6:
                            who = "به عنوان یک فرد آگاه از مسائل حقوقی و قضایی پاسخ این سوال رو بده "
                        elif section == 7:
                            who = "به عنوان یک فرد مشاور تحصیلی پاسخ این سوال رو بده "
                        elif section == 8:
                            who = "به عنوان یک پزشک پاسخ این سوال رو بده "
                        elif section == 9:
                            who = "به عنوان یک مشاور کسب و کار پاسخ این سوال رو بده "
                        elif section == 10:
                            who = "به عنوان یک متخصص بازار های مالی پاسخ این سوال رو بده "
                        elif section == 11:
                            who = "به عنوان یک مشاور امور مهاجرت پاسخ این سوال رو بده "                
                        elif section == 12:
                            who = "به عنوان یک برنامه نویس پاسخ این سوال رو بده "
                        elif section == 13:
                            who = "به عنوان یک مشاور خرید محصول پاسخ این سوال رو بده "
                        elif section == 14:
                            who = "به عنوان یک تعمیر کار پاسخ این سوال رو بده "
                        elif section == 15:
                            who = "به عنوان یک مشاور سرمایه گذاری پاسخ این سوال رو بده "
                        elif section == 16:
                            who = "به عنوان یک متخصص موبایل و کامپیوتر پاسخ این سوال رو بده "  


                        if user.webservice_campaign_name is not None :
                            campaign = " و بعد بهش " + user.webservice_campaign_name + " رو بهش پیشنهاد کن که بدون نیاز به کد تخفیف میتونه ازش استفاده کنه "
                        if user.webservice_discount_code is not None :
                            discount_code = "' و بعد کد تخفیف " + user.webservice_discount_code + " رو برای بهره مندی از '" + user.webservice_campaign_name + " در  " + user.full_name + " پیشنهاد کن "
                        name = " و در پایان هم از مخاطب بابت مشاوره ای که در " + user.full_name + " گرفته صمیمانه تشکر کن ."

                        #در صورتیکه کد تخفیف وارد شده بود دیگر کمپین را جداگانه معرفی نکند
                        if user.webservice_discount_code == None :
                            discount_code = ""
                        else :
                            campaign = ""
                        
                        #اگر کمپین و عنوان جشنواره تعریف نشده بود به کل جملات کمپین و کد تخفیف حذف شوند
                        if user.webservice_campaign_name == None :
                            campaign = ""
                            discount_code = ""




                    
                        prompt = who + campaign + discount_code + name + " : " + str(question)






                        response = model.generate_content(prompt)
                        result = response.text
                        result = result.replace("*", "")
                        if result:
                            user.balance -= 1
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
                            #created_at = datetime.now(),
                            status = status,
                            user_phone_number = user.mobile_number,
                            user_full_name = user.full_name,
                            question = question,
                            from_who = from_who,
                            api_key_name = api_key_name,
                            credit = user.balance,
                            user_os = webservice_user_os,
                            webservice_user = webservice_user,
                            webservice_discount_code = user.webservice_discount_code,
                            webservice_campaign_name = user.webservice_campaign_name                            
                        )
                        question.save()                
                        print(f"Error: {e}")
                        return JsonResponse({'error': str(e)})


                    #ذخیره سازی سوال کاربر و متغیر های مورد نیاز دیگر در دیتابیس
                    question = QuestionHistory(
                        #created_at = datetime.now(),
                        status = status,
                        user_phone_number = user.mobile_number,
                        user_full_name = user.full_name,
                        question = question,
                        from_who = from_who,
                        api_key_name = api_key_name,
                        credit = user.balance,
                        user_os = webservice_user_os,
                        webservice_user = webservice_user,
                        webservice_discount_code = user.webservice_discount_code,
                        webservice_campaign_name = user.webservice_campaign_name
                    )
                    question.save()               
                    return JsonResponse({"answer": result, "note": "پاسخ جدید پردازش شد"})
                else :
                    return JsonResponse({"answer": "این سرویس در حال حاضر غیر فعال است", "note": "اعتبار کاربر وب سرویس پایان یافته است"})    
            
            else :
                return JsonResponse({"answer": "کاربر نا معتبر است", "note": "کاربر وب سرویس ندارد"})


            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)









ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"


currency = "IRR"  # or "IRT"

# کد مرچنت خود را در فایل settings وارد کنید

# Required Data
amount = 20000  # Based on your currency
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
#CallbackURL = 'http://127.0.0.1:8000/webservice/'
CallbackURL = 'http://beporsimige.ir/webservice/'

# Important: need to edit for a real server.


#تابع ارسال درخواست به درگاه بانکی
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


#تابع نمایش نتیجه تراکنش بانکی و ذخیره نتیجه
@login_required
def verify(request):
    #جهت افزایش اعتبار یوزر 
    user = request.user
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    if status == "NOK":
       
        #ذخیره سازی سابقه تراکنش به عنوان تراکنشی نا موفق
        transaction = TransactionHistory(
            #created_at = datetime.now(),
            status = "NOK",
            user_phone_number = request.session.get('user_phone_number'),
            user_full_name = request.session.get('user_full_name'),
            orginal_price = request.session.get('orginal_price'),
            amount = request.session.get('amount'),
            ref_id = "",
            discount_code = request.session.get('discount_code'),
            initial_credit = request.session.get('initial_credit'),
            secondary_credit = request.session.get('initial_credit'),
            user_os = request.session.get('user_os'),
            webservice_question_price = user.webservice_question_price
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
            i = request.session.get('orginal_price') / user.webservice_question_price

            user.balance += i
            user.save()

            
            #ذخیره سازی سابقه تراکنش به عنوان تراکنش موفق
            transaction = TransactionHistory(
                #created_at = datetime.now(),
                status = "OK",
                user_phone_number = request.session.get('user_phone_number'),
                user_full_name = request.session.get('user_full_name'),
                orginal_price = request.session.get('orginal_price'),
                amount = request.session.get('amount'),
                ref_id = response['data']['ref_id'],
                discount_code = request.session.get('discount_code'),
                initial_credit = request.session.get('initial_credit'),
                secondary_credit = int(request.session.get('initial_credit')) + i,
                user_os = request.session.get('user_os'),
                webservice_question_price = user.webservice_question_price
            )
            transaction.save()           
            

            return JsonResponse({'status': True, 'message': 'پرداخت موفق', 'ref_id': response['data']['ref_id'] , 'balance': user.balance})



        else:
            return JsonResponse({'status': False, 'message': 'پرداخت ناموفق', 'data': response})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'message': 'اتصال برقرار نشد'})

            


