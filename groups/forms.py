from django import forms
from . import models
from django.forms import modelformset_factory

class QuizForm(forms.ModelForm):
    class Meta:
        model = models.Quiz
        fields = [
        'title',
        'description',
        'order',
        'total_questions',
        ]
class TrueFalseQuestionForm(forms.ModelForm):
    class Meta:
        model = models.TrueFalseQuestion
        fields = ['order','prompt']

class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = models.MulitpleChoiceQuestion
        fields = ['order','prompt','shuffle_answers']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ['text','order','correct']

AnswerFormSet = forms.modelformset_factory(
                        models. Answer,
                        form = AnswerForm
                        # extra=2
                    )
