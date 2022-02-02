from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.png',upload_to='profile_pics')
    gender = models.CharField(max_length=10)
    mobile_no = models.CharField(max_length=10)
    bio = models.CharField(max_length=1000)
    birth_date = models.DateField(null=True)

    REQUIRED_FIELDS = ['profile_picture','gender','mobile_no','city','birth_date','username']

    def __str__(self):
        return str(self.user.username)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)