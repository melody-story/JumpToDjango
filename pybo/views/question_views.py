from django.shortcuts      import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils          import timezone
from django.contrib        import messages

from ..models import Question
from ..forms  import QuestionForm


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