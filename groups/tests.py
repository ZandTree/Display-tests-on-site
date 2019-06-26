from django.test import TestCase

# Create your tests here.

class StepModelTests(TestCase):
    """ Тест на наличие step в group"""
    def setUp(self):
        ''' это как стандартная затравка для всех одинаковая, хотя у меня пока 1 тест'''
        self.group = Group.objects.create(title='Trees',description='Learn to plant')
    def test_step_creation(self):
        step = Step.objects.create(title='Apples',description='How to plant an appletree',group = self.group)
        self.assertIn(step,self.group.step_set.all())
