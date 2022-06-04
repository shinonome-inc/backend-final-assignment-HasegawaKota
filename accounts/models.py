from django.contrib.auth.models import AbstractUser
from django.db import models


#デフォルトで用意されているUserではない
class User(AbstractUser):
    email = models.EmailField(max_length=254)
    yourname = models.CharField(null=True, max_length=254)
   

    class Meta:
        db_table = 'User'

class FriendShip(models.Model):
     pass
