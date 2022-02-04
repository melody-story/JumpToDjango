# from django.http import HttpResponse
# from multiprocessing import context
from django.shortcuts      import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils          import timezone
from django.core.paginator import Paginator  
from django.contrib        import messages


from .models import Question, Answer
from .forms  import QuestionForm,  AnswerForm

# def index(request):
#     return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context) 


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    # question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

# def answer_create(request, question_id):
#     """
#     pybo 답변등록
#     """
#     question = get_object_or_404(Question, pk=question_id)
#     question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
#     # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
#     # answer.save()
#     return redirect('pybo:detail', question_id=question.id)

@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문등록
    """
    # form = QuestionForm()
    # return render(request, 'pybo/question_form.html', {'form': form})

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)# create_date값이 아직 없으므로, 임시저장을 한다!
            question.author = request.user # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save() # create_date 값 받은 뒤 최종 저장!
            return redirect('pybo:index')
    else:# method==get
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

def question_modify(request, question_id):
    """
    pybo 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question) 
        # 위 코드의 의미는 instance를 기준으로 QuestionForm을 생성하지만 request.POST의 값으로 덮어쓰라는 의미
        if form.is_valid:
            question = form.save(commit=False)
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form=QuestionForm(instance=question) 
        # 질문수정 화면에 조회된 질문의 제목과 내용이 반영될 수 있도록
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)
        
@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect("pybo:detail", question_id=answer.question.id)
    
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid:
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
        return redirect("pybo:detail", question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer' : answer,'form' : form}
    return render(request, 'pybo/answer_form.html', context)

def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "삭제 권한이 없습니다.")
    else:
        answer.delete()
    return redirect("pybo:detail", question_id=answer.question.id)