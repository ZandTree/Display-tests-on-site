from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('',views.GroupList.as_view(),name='groups-list'),
    path('quiz/<int:group_pk>/<int:quiz_pk>/',views.QuizDetail.as_view(),name='quiz'),
]
