from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# デフォルトで用意されているUserではない
class User(AbstractUser):
    email = models.EmailField(max_length=254)

    class Meta:
        db_table = "User"


class Profile(models.Model):
    # on_deleteがないとエラーになったわ
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", primary_key=True
    )
    introduction = models.CharField("自己紹介", max_length=255, blank=True)
    hobby = models.CharField("趣味", max_length=255, blank=True)

    class Meta:
        db_table = "Profile"

    def __str__(self):
        return str(self.user)


# 新ユーザーの作成時に空のprofileも作成する
@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


class FriendShip(models.Model):
    pass
