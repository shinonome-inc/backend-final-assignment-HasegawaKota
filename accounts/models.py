from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
#from .models import User



#デフォルトで用意されているUserではない
class User(AbstractUser,PermissionsMixin):
    email = models.EmailField(max_length=254)
    yourname = models.CharField(null=True, max_length=254)


   

    class Meta:
        db_table = 'User'

class Profile(models.Model):
    uesr=models.OneToOneField(User,on_delete=models.CASCADE)#on_deleteがないとエラーになったわ
    introduction=models.CharField('自己紹介',max_length=255,blank=True)
    hobby=models.CharField('趣味',max_length=255,blank=True)


#新ユーザーの作成時に空のprofileも作成する
@receiver(post_save, sender=User)
def save_profile(sender,instance,**kwargs):
      instance.profile.save()

#@receiver(post_save, sender=User)#新ユーザーの作成時に空のprofileも作成する
#def create_profile(sender,  **kwargs ):
    #if kwargs['created']:
        #user_profile=Profile.objects.get_or_create(user=kwargs['instance'])



class FriendShip(models.Model):
     pass
