from django.urls import path,re_path
from . import views

app_name = 'groups'

urlpatterns = [
    path('',views.GroupList.as_view(),name='groups-list'),
    path('display/<int:group_pk>/<int:quiz_pk>/',views.QuizDetail.as_view(),name='quiz'),
    path('create-quiz/<int:pk>/',views.QuizCreate.as_view(),name='create-quiz'),
    path('edit-quiz/<int:group_pk>/<int:quiz_pk>/',views.QuizEdit.as_view(),name='edit-quiz'),
    re_path(r'^(?P<quiz_pk>\d+)/create-question/(?P<question_type>mc|tf)/$',views.QuestionCreate.as_view(),name='create-question'),
    path('edit-question/<int:question_pk>/quiz/<int:quiz_pk>/',views.QuestEdit.as_view(),name='edit-question'),
    path('create-answer/<int:pk>/',views.AnswerCreate.as_view(),name='create-answer'),
    # /groups/edit-question/1/quiz/1/

]
