import profile
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
    user=models.OneToOneField(User,on_delete=models.CASCADE)#on_deleteがないとエラーになったわ
    introduction=models.CharField('自己紹介',max_length=255,blank=True)
    hobby=models.CharField('趣味',max_length=255,blank=True)
    #def __str__(self):
      #return self.user


#新ユーザーの作成時に空のprofileも作成する


@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        #Profile.objects.create(instance)#ここがまちがっているん
        Profile.objects.get_or_create(user=instance)
    else:
        instance.profile.save()



class FriendShip(models.Model):
     pass
