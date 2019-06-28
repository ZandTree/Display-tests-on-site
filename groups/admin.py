from django.contrib import admin
from .models import Group,Quiz,Question,MulitpleChoiceQuestion,TrueFalseQuestion,Answer

admin.site.register(Group)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(MulitpleChoiceQuestion)
admin.site.register(TrueFalseQuestion)
admin.site.register(Answer)
