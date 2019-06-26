from django.utils import timezone
import os


def make_avatar_path(instance,file):
    tail = file.split('.')[-1]
    head = file.split('.')[0]
    if len(head) > 10:
        head = head[:10]
    created = timezone.now().strftime("Y-%m-%d")
    file_name = head +'_' + created +'.' + tail
    img_folder = "user_{}".format(instance.user_id)
    return  os.path.join('avatars',user_folder,file_name)
