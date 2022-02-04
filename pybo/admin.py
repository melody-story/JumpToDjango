from django.contrib import admin
from .models import Question, Answer # 추가

class QuestionAdmin(admin.ModelAdmin): # 추가
    search_fields = ['subject'] # 제목(subject)으로 질문을 검색

admin.site.register(Question,QuestionAdmin)# 추가 
admin.site.register(Answer)# 추가 
