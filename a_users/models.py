from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image  = models.ImageField(upload_to='avatars/', null=True, blank=True)
    display_name = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.user
    
    @property
    def name(self):
        if self.display_name:
            name = self.display_name
        else:
            name = self.user.username
            
        return name
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar.svg')
            
        return avatar