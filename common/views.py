from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from common.forms import UserForm
# Create your views here.
def singup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') #  cleaned_data: 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) # 사용자 인증 # 회원가입과 동시에 자동 인증
            login(request, user) # 회원가입과 동시에 자동 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form' : form})
    
def page_not_found(request, exception):
    """
    404 Page not found
    """
    return render(request, 'common/404.html', {})