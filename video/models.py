from django.db import models
from user.models import User
from django.core.exceptions import ValidationError
import os



def video_upload(instance, filename):
    ext = os.path.splitext(filename)[1]
    user=f'{instance.created_by.first_name}{instance.created_by.last_name}'.replace(" ",'')
    format = f'{user}/{instance.video_name.lower()}{ext}'
    return os.path.join(format)


def validate_video_file(value):
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions are: .mp4, .mov, .avi, .mkv')
    


class Video(models.Model):
    video_name=models.CharField(max_length=100)
    category=models.CharField(max_length=50)
    description=models.TextField(max_length=500)
    file=models.FileField(validators=[validate_video_file],upload_to=video_upload)
    created_by=models.ForeignKey(User,on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.video_name