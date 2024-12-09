from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from django.contrib import messages

def auth_page(request):
    if request.method == "POST":
        if "register" in request.POST:
            reg_form = RegistrationForm(request.POST)
            login_form = LoginForm()
            if reg_form.is_valid():
                reg_form.save()  # رمز عبور به صورت هش‌شده ذخیره می‌شود
                messages.success(request, "ثبت‌نام با موفقیت انجام شد!")
                return redirect('accounts:auth_page')
        elif "login" in request.POST:
            reg_form = RegistrationForm()
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                user = authenticate(
                    request,
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password']
                )
                if user:
                    login(request, user)
                    return redirect('homepage:homepage')
                else:
                    messages.error(request, "شماره موبایل یا رمز عبور نادرست است.")
            else:
                messages.error(request, "فرم ورود معتبر نیست.")
    else:
        reg_form = RegistrationForm()
        login_form = LoginForm()

    return render(request, 'accounts/auth_page.html', {'reg_form': reg_form, 'login_form': login_form})
