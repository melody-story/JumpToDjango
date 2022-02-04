from django.shortcuts      import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils          import timezone
from django.contrib        import messages

from ..models import Question, Answer, Comment
from ..forms  import CommentForm

@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """
    pybo 질문댓글생성
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question # question.id가 아니라 객체가 들어간다.
            comment.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    pybo 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "수정권한이 없습니다.")
        redirect("pybo:detail", question_id=comment.question.id)
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect("pybo:detail", question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)
        
@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """
    pybo 질문댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect('pybo:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id)

@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """
    pybo 답글댓글등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm()
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """
    pybo 답글댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "댓글을 수정할 권한이 없습니다.")
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)
            
@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """
    pybo 답글댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "댓글 삭제 권한이 없습니다.")
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)