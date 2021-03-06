from django import forms
from pybo.models import Question, Answer, Comment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # }
        # 위와 같이 Meta 클래스의 widgets 속성을 지정하면 입력 필드에 form-control과 같은 부트스트랩 클래스를 추가할 수 있다.
        labels = {
            'subject': '제목',
            'content': '내용',
        }
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model  = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['content'] # 사용될 필드
        labels = {
            'content' : '댓글내용',
        }
        