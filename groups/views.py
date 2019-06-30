from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView,DetailView,
                                CreateView,UpdateView,
                                View,FormView
                                )
from .models import *
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect,Http404
from . import forms
from django.contrib.auth.models import User
from django.utils import timezone


class GroupList(ListView):
    model = Group
    # def get_queryset(self):
        # qs = Group.objects.datetimes('created_at','year')
        #qs with year is: <QuerySet [datetime.datetime(2019, 1, 1, 0, 0, tzinfo=<UTC>)]>
        #print([d.second for d in Group.objects.datetimes('created_at', 'second')])
        # [42, 10, 38]
        # return Group.objects.all()

class QuizDetail(DetailView):
    model = Quiz
    def get_object(self):
        group_id = self.kwargs.get('group_pk')
        quiz_id = self.kwargs.get('quiz_pk')
        try:
            object = Quiz.objects.select_related('group').get(
                                group_id=group_id,id=quiz_id)
        except Quiz.DoesNotExist:
            raise Http404
        return object

class QuizCreate(CreateView):
    model = Quiz
    fields = ['title','description','order','total_questions']
    template_name = 'groups/create_quiz.html'

    def form_valid(self,form):
        group_pk = self.kwargs.get('pk')
        group = get_object_or_404(Group,id=group_pk)
        quiz = form.save(commit=False)
        quiz.group = group
        quiz.save()
        messages.add_message(self.request,messages.SUCCESS,"Quiz added!")
        return HttpResponseRedirect(quiz.get_absolute_url())

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['create'] = True
        return context

class QuizEdit(SuccessMessageMixin,UpdateView):
    model = Quiz
    fields = ['title','description','order','total_questions']
    template_name = 'groups/create_quiz.html'
    # static success_message can be here as well
    def get_object(self):
        group_id = self.kwargs.get('group_pk')
        id = self.kwargs.get('quiz_pk')
        try:
            object = Quiz.objects.select_related('group').get(
                                group_id=group_id,id=id)
        except Quiz.DoesNotExist:
            raise Http404
        return object
    def get_success_message(self,*args,**kwargs):
        return 'Quiz "{}"  successfully updated'.format(self.get_object().title)

class QuestionCreate(FormView):
    template_name ='groups/create_edit_question.html'

    def get_form_class(self,form_class=None):
        question_type = self.kwargs.get('question_type')
        if question_type == 'mc':
            form_class = forms.MultipleChoiceQuestionForm
        else:
            form_class = forms.TrueFalseQuestionForm
        return form_class

    def form_valid(self,form):
        question = form.save(commit=False)
        quiz_pk = self.kwargs.get('quiz_pk')
        quiz = get_object_or_404(Quiz,id=quiz_pk)
        question.quiz = quiz
        question.save()
        return HttpResponseRedirect(question.get_absolute_url())

class QuestEdit(SuccessMessageMixin,UpdateView):
    model = Question
    template_name ='groups/create_edit_question.html'

    def get_object(self):
        quiz_id = self.kwargs.get('quiz_pk')
        question_id = self.kwargs.get('question_pk')
        try:
            object = Question.objects.select_related('quiz').get(
                                quiz_id=quiz_id,id=question_id)
        except Question.DoesNotExist:
            raise Http404
        return object
    def get_form_class(self,form_class=None):
        question = self.get_object()
        if hasattr('question','truefalsequestion'):
            form_class = forms.TrueFalseQuestionForm
        else:
            form_class = forms.MultipleChoiceQuestionForm
        return form_class
    def get_success_message(self,*args,**kwargs):
        return 'Question "{}"  successfully updated'.format(self.get_object())

class AnswerCreate(View):
    def get(self,request,pk):
        quest = get_object_or_404(Question,id=pk)
        formset = forms.AnswerFormSet(queryset=quest.ans.all())
        return render(request,'groups/create_answer.html',{'formset':formset})

    def post(self,request,**kwargs):
        quest_id = self.kwargs.get('pk')
        quest = get_object_or_404(Question,id=quest_id)
        formset = forms.AnswerFormSet(request.POST,queryset=quest.ans.all())
        if formset.is_valid():
            answers= formset.save(commit=False)
            for answer in answers:
                answer.question = quest
                answer.save()
        messages.success(self.request, "Answers saved successfully")
        # return super().form_valid(form)
        return HttpResponseRedirect(quest.get_absolute_url())

# example for DigitalProducts
# def post(...):
#     formset = forms.DigitalProductsFormset(request.POST) # without question
#     if formset.is_valid():
#         for form in formset:
#             if form.is_valid():
#                 form.save()
#         return HttpResponseRedirect(or x.get_absolute_url,or reverse(...))


#let look at the formset = special set of fields to controle Num fields:
"""

fot the whole formset = one bundel
<input type="hidden" name="form-TOTAL_FORMS" value="3" id="id_form-TOTAL_FORMS" />
<input type="hidden" name="form-INITIAL_FORMS" value="2" id="id_form-INITIAL_FORMS" />
<input type="hidden" name="form-MIN_NUM_FORMS" value="0" id="id_form-MIN_NUM_FORMS" />

# default value = 1000
<input type="hidden" name="form-MAX_NUM_FORMS" value="1000" id="id_form-MAX_NUM_FORMS" />

#custom (here max_num = 5 in forms.py) ==> value = 5
<input type="hidden" name="form-MAX_NUM_FORMS" value="5" id="id_form-MAX_NUM_FORMS" />
otherwise:(if no bundel above)
django.forms.utils.ValidationError: ['ManagementForm data is missing or has been tampered with']
"""
#For each form in formset (iteration)
"""
<tr><th><label for="id_form-0-text">Text:</label></th><td>
<input type="text" name="form-0-text" value="Yes" id="id_form-0-text" maxlength="1024" /></td></tr>
<tr><th><label for="id_form-0-order">Order:</label></th><td>
<input type="number" name="form-0-order" value="1" id="id_form-0-order" /></td></tr>
<tr><th><label for="id_form-0-correct">Correct:</label></th><td>
<input type="checkbox" name="form-0-correct" id="id_form-0-correct" />
<input type="hidden" name="form-0-id" value="15" id="id_form-0-id" /></td></tr> <tr><th><label for="id_form-1-text">Text:</label></th><td>
"""

















# # @login_required
# def edit_question(request,quiz_pk,question_pk):
#     question =get_object_or_404(models.Question,pk=question_pk,quiz_id = quiz_pk)
#     if hasattr(question,'truefalsequestion'):
#         form_class = forms.TrueFalseQuestionForm
#         question = question.truefalsequestion
#     else:
#         form_class = forms.MultipleChoiceQuestionForm
#         question = question.multiplechoicequestion
#     form = form_class(instance=question)
#     if request.method =='POST':
#         form = form_class(request.POST,instance=question)
#         if form.is_valid():
#             form.save()
#             messages.success(request,'Question created')
#             return HttpResponseRedirect(question.quiz.get_absolute_url())
#
#     return render(request,'courses/question_form.html',
#         {'form':form,
#         'quiz':question.quiz}
#     )
#
# @login_required
# def create_answer(request,question_pk):
#     question = get_object_or_404(models.Question,pk=question_pk)
#     form = forms.AnswerForm()
#     if request.method == 'POST':
#         form = forms.AnswerForm(request.POST)
#         answer = form.save(commit=False)
#         answer.question = question
#         answer.save()
#         messages.success(request,"Answer added")
#         return HttpResponseRedirect(question.get_absolute_url())
#     return render(request,'courses/create_answer.html',{'question':question,'form':form})
#
