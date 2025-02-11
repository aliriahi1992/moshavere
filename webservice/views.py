from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from accounts.models import CustomUser
import os
import google.generativeai as genai
from django.contrib.auth.decorators import login_required
#برای ذخیره سازی سوابق سوالات پرسیده شده توسط کاربران
from homepage.models import QuestionHistory




@login_required
def homepage(request):
    user = request.user
    user_questions = QuestionHistory.objects.filter(user_phone_number=user.mobile_number).order_by('-created_at')  # آخرین سوالات اول نمایش داده شوند
    return render(request, 'webservice/index.html', {'balance': user.balance, 'user_questions': user_questions})


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
                        from_who = "متخصص پوست و مو"
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
                    elif section == 16: 
                        from_who = "متخصص موبایل و کامپیوتر"  


                    try:
                        GOOGLE_API_KEY = os.getenv('API_KEY_1')
                        #مقدار دهی به متغیر های ذخیره سازی در دیتابیس
                        api_key_name = "API_KEY_1"

                        genai.configure(api_key=GOOGLE_API_KEY)
                        model = genai.GenerativeModel('gemini-pro')

                        if section == 1:
                            prompt = "به عنوان یک مشاور در زمینه پوست و مو پاسخ این سوال رو بده " + str(question)
                        elif section == 2:
                            prompt = "به عنوان یک استاد علمی و دانشگاهی و معلم پاسخ این سوال رو بده  " + str(question)
                        elif section == 3:
                            prompt = "به عنوان یک مشاور امور اجتماعی و خانوادگی و فردی پاسخ این سوال رو بده " + str(question)
                        elif section == 4:
                            prompt = "به عنوان یک متخصص تغذیه و رژیم درمانی پاسخ این سوال رو بده " + str(question)
                        elif section == 5:
                            prompt = "به عنوان یک مربی ورزشی پاسخ این سوال رو بده " + str(question)
                        elif section == 6:
                            prompt = "به عنوان یک فرد آگاه از مسائل حقوقی و قضایی پاسخ این سوال رو بده " + str(question)
                        elif section == 7:
                            prompt = "به عنوان یک فرد مشاور تحصیلی پاسخ این سوال رو بده " + str(question)
                        elif section == 8:
                            prompt = "به عنوان یک پزشک پاسخ این سوال رو بده " + str(question)
                        elif section == 9:
                            prompt = "به عنوان یک مشاور کسب و کار پاسخ این سوال رو بده " + str(question)
                        elif section == 10:
                            prompt = "به عنوان یک متخصص بازار های مالی پاسخ این سوال رو بده " + str(question)
                        elif section == 11:
                            prompt = "به عنوان یک مشاور امور مهاجرت پاسخ این سوال رو بده " + str(question)                  
                        elif section == 12:
                            prompt = "به عنوان یک برنامه نویس پاسخ این سوال رو بده " + str(question)
                        elif section == 13:
                            prompt = "به عنوان یک مشاور خرید محصول پاسخ این سوال رو بده " + str(question)  
                        elif section == 14:
                            prompt = "به عنوان یک تعمیر کار پاسخ این سوال رو بده " + str(question)
                        elif section == 15:
                            prompt = "به عنوان یک مشاور سرمایه گذاری پاسخ این سوال رو بده " + str(question)
                        elif section == 16:
                            prompt = "به عنوان یک متخصص موبایل و کامپیوتر پاسخ این سوال رو بده " + str(question)                    


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
                            webservice_user = webservice_user
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
                        webservice_user = webservice_user
                    )
                    question.save()               
                    return JsonResponse({"answer": result, "note": "پاسخ جدید پردازش شد"})
                else :
                    return JsonResponse({"answer": "این سرویس در حال حاضر غیر فعال است", "note": "اعتبار کاربر وب سرویس پایان یافته است"})    
            
            else :
                return JsonResponse({"answer": "کاربر نا معتبر است", "note": "کاربر وب سرویس ندارد"})


            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)






            


