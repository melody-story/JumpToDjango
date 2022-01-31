# from django.http import HttpResponse
from django.shortcuts import render
from .models import Question

# def index(request):
#     return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")


def index(request):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)