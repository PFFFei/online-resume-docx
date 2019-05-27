from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm
from .models import User
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'accounts/home.html')

def login_view(request):  # 用户根据 Email 和 Password 进行登陆
    # 判断是否已登录
    if request.user.is_authenticated:
        return redirect("resume:templates") # 登陆后定向到模板
    else:
        title = "登 陆"
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # authenticates Email & Password
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect("resume:templates")
        context = {"form": form,
                   "title": title
                   }

        return render(request, "accounts/form.html", context)


def register_view(request):  
    if request.user.is_authenticated:
        return redirect("resume:templates")
    else:
        title = "注 册"
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            new_user = authenticate(email=user.email, password=password)
            login(request, new_user)
            return redirect("resume:templates")

        context = {"title": title, "form": form}

        return render(request, "accounts/form.html", context)

@login_required
def logout_view(request):  
    # 判断是否已登录
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    else:
        logout(request)
        return redirect("accounts:home")
