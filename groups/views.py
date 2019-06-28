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
    template_name ='groups/create_question.html'

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
    template_name ='groups/create_question.html'

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

class AnswerCreate(CreateView):
    model = Answer
    template_name = 'groups/create_answer.html'
    form_class = forms.AnswerForm()
    # success_url = '/'

    def form_valid(self,form):
        quest_id = self.kwargs.get('pk')
        quest = get_object_or_404(Question,id=quest_id)
        answer = form(commit=False)
        answer.question = quest
        answer.save()
        return HttpResponseRedirect(quest.get_absolute_url())
"""
TypeError at /groups/create-answer/1/
'AnswerForm' object is not callable
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
