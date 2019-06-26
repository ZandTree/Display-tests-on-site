from django.db import models
from django.shortcuts import reverse

# Create your models here.

class Group(models.Model):
    title = models.CharField(max_length=124)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Step(models.Model):
    title = models.CharField(max_length=124)
    description = models.TextField()
    order = models.IntegerField(default=0)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    class Meta:
        abstract = True
        ordering = ['order']

class Quiz(Step):
    total_questions = models.SmallIntegerField(default=4)
    times_taken = models.IntegerField(default=0,editable=False)
    def __str__(self):
        return 'test{} {}'.format(self.order,self.title)

    def get_absolute_url(self):
        return reverse('groups:quiz',
                        kwargs={'group_pk':self.group_id,'quiz_pk':self.id})
    class Meta:
        verbose_name_plural = 'Quizzes'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    prompt = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    class Meta:
        ordering = ['order',]
    def get_absolute_url(self):
        return self.quiz.get_absolute_url()

    def __str__(self):
        return self.prompt

class MulitpleChoiceQuestion(Question):
    shuffle_answers = models.BooleanField(default=False)

class TrueFalseQuestion(Question):
    pass

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='ans')
    correct = models.BooleanField(default=False)
    text = models.CharField(max_length=1024)
    order = models.IntegerField(default=0)
    def __str__(self):
        return 'answer {} for question {}'.format(self.id,self.question)
    class Meta:
        ordering = ['order',]
    def __str__(self):
        return self.text
