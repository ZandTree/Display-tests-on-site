from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image
from utils import make_avatar_path


# Create your models here.
CHOICES = (
    ('start','beginner'),
    ('medium','intermed'),
    ('high','senior'),
)
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile')
    first_name = models.CharField(max_length=24,default="")
    last_name = models.CharField(max_length=56,default="")
    created = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(blank=True,null=True,upload_to=make_avatar_path)
    level = models.CharField(max_length=5,choices=CHOICES,default='start')

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + self.last_name
        else:
            return self.user.username

    def get_absolute_url(self):
        return reverse('profiles:profile',kwargs={'pk':self.user_id})

    @property
    def get_ava_path(self,*args,**kwargs):
        if self.avatar:
            return '/media/{}'.format(self.avatar)
        else:
            return '/static/img/redcat.jpg/'

    def save(self,**kwargs):
        super().save(kwargs)
        img= Image.open(self.avatar.path)
        if img.height >200 or img.width>200:
            output_size = (200,200)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,*args,**kwargs):
    if created:
        Profile.objects.create(user=instance)
