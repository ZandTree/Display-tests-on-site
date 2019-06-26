from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView
from .models import *
from django.contrib import messages
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
        id = self.kwargs.get('quiz_pk')        
        try:
            object = Quiz.objects.select_related('group').get(
                                group_id=group_id,id=id)
        except Quiz.DoesNotExist:
            raise Http404
        return object

class QuizCreate(CreateView):
    pass
# def quiz_create(request,course_pk):
#     course = get_object_or_404(models.Course,pk=course_pk,published=True)
#     form = forms.QuizForm()
#     if request.method == 'POST':
#         form = forms.QuizForm(request.POST)
#         if form.is_valid():
#             quiz = form.save(commit=False)
#             quiz.course = course
#             quiz.save()
#             messages.add_message(request,messages.SUCCESS,"Quiz added!")
#             return HttpResponseRedirect(quiz.get_absolute_url())
#
#     return render(request,'courses/quiz_form.html',{'form':form,'course':course})
#
#
# @login_required
# def quiz_edit(request,course_pk,quiz_pk):
#     quiz = get_object_or_404(models.Quiz,pk=quiz_pk, course_id=course_pk,course__published=True)
#     form = forms.QuizForm(instance=quiz)
#     if request.method == 'POST':
#         form = forms.QuizForm(instance=quiz,data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Quiz updated!".format(form.cleaned_data['title']))
#             return HttpResponseRedirect(quiz.get_absolute_url())
#
#     return render(request,'courses/quiz_form.html',{'form':form,'course':quiz.course})
#
#
# @login_required
# def create_question(request,quiz_pk,question_type):
#     quiz =get_object_or_404(models.Quiz,pk=quiz_pk)
#     if question_type == 'tf':
#         form_class = forms.TrueFalseQuestionForm
#     else:
#         form_class = forms.MultipleChoiceQuestionForm
#     form = form_class()
#     if request.method =='POST':
#         form = form_class(request.POST)
#         if form.is_valid():
#             question = form.save(commit=False)
#             question.quiz = quiz
#             question.save()
#             messages.success(request,'Question created')
#             return HttpResponseRedirect(quiz.get_absolute_url())
#
#     return render(request,'courses/question_form.html',
#         {'quiz': quiz,
#         'form':form}
#     )
# @login_required
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

# class Search(View):
#     def get(self,request):
#         word = request.GET.get('q')
#         group = models.Group.objects.filter(
#             Q( title__icontains=word)|Q(description__icontains=word),
#             published=True
#             )
#         return render(request,'groups/group_list.html',{'groups':groups})
