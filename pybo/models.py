from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Question(models.Model):
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')# 계정이 삭제되면 이 계정이 작성한 질문을 모두 삭제
    subject     = models.CharField(max_length=200)
    content     = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter       = models.ManyToManyField(User, related_name='voter_question')
    
    def __str__(self):
        return self.subject

class Answer(models.Model):
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')# 계정이 삭제되면 이 계정이 작성한 답변을 모두 삭제
    question    = models.ForeignKey(Question, on_delete=models.CASCADE) # q.answer_set.all() 로 짊문의 모든 답변들을 가져올 수 있음.
    content     = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter       = models.ManyToManyField(User, related_name='voter_answer')
    # null=True는 데이터베이스에서 modify_date 칼럼에 null을 허용한다는 의미이며, blank=True는 form.is_valid()를 통한 입력 데이터 검사 시 값이 없어도 된다는 의미
    def __str__(self):
        return self.content
    
class Comment(models.Model):
    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    content     = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question    = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer      = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content