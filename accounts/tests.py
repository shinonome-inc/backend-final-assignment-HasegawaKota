import email
from importlib.resources import path
from tkinter.tix import Form
from django import views
from django.test import TestCase
from .models import User
from django.urls import reverse
from .forms import SignupForm
from django.contrib.auth import SESSION_KEY


class TestSignUpView(TestCase):
    def test_success_get(self):
        #response_getは名前だよ
        #リクエストを送信する
        response_get=self.client.get(reverse('signup'))
        #ユーザーが
        self.assertEquals(response_get.status_code,200)
        self.assertFalse(User.objects.exists())
        self.assertTemplateUsed(response_get,'accounts/signup.html')
        

    def test_success_post(self):
        
        data_post={
            'email':'example@example.com',
            'username':'sample',
            'password1':'testpassword',
            'password2':'testpassword',
            }
        response_post=self.client.post(reverse('signup'),data_post)
        
        self.assertRedirects(response_post,reverse('home'),status_code=302,target_status_code=200)


        
       #form=SignupForm(self.data_post)
       #self.assertTrue(form)

    def test_failure_post_with_empty_form(self):
        data_empty_form={
            'email':'',
            'username':'',
            'password1':'',
            'password2':'',
        }
        #self.client.post(テストしたいURL,POST送信するデータ)
        #self.client.get(テストしたいURL)
        response_empty_form = self.client.post(reverse('signup'),data_empty_form) #これも名前
        self.assertEquals(response_empty_form.status_code,200)
        #Userオブジェクトが作られていないことを確認
        self.assertFalse(User.objects.exists())

        form=SignupForm(data_empty_form)
        
        self.assertTrue(form.errors['email'])
        self.assertTrue(form.errors['username'])
        self.assertTrue(form.errors['password1'])
        self.assertTrue(form.errors['password2'])
        

    def test_failure_post_with_empty_username(self):

        data_empty_username={
             'email':'example@example.com',
             'username':'',
             'password1':'example12345',
             'password2':'example12345',
         }
        response_empty_username=self.client.post(reverse('signup'),data_empty_username)
        self.assertEquals(response_empty_username.status_code,200)
        self.assertFalse(User.objects.exists())
        form=SignupForm(data_empty_username)
        self.assertTrue(form.errors['username'])


         

    def test_failure_post_with_empty_email(self):

        data_empty_email={
             'email':'',
             'username':'sample',
             'password1':'example12345',
             'password2':'example12345',
         }
        response_empty_email=self.client.post(reverse('signup'),data_empty_email)
        self.assertEquals(response_empty_email.status_code,200)
        self.assertFalse(User.objects.exists())
        form=SignupForm(data_empty_email)
        self.assertTrue(form.errors['email'])

    def test_failure_post_with_empty_password(self):
        #ブランクのあるpaswordが送信された時
        data_empty_password={
             'email':'example@example.com',
             'username':'sample',
             'password1':'',
             'password2':'',
         }
        response_empty_password=self.client.post(reverse('signup'),data_empty_password)
        self.assertEquals(response_empty_password.status_code,200)
        self.assertFalse(User.objects.exists())
        form=SignupForm(data_empty_password)
        self.assertTrue(form.errors['password1'])


    def test_failure_post_with_duplicated_user(self):
        #既に存在するユーザーを登録するリクエストを送った時
        data_duplicated_user={
             'email':'example@example.com',
             'username':'sample',
             'password1':'example12345',
             'password2':'example12345',
         }
        
        
        
        User.objects.create(
             email='example@example.com',
             username='sample',
             password='example12345',
             #password2='example12345',
             )
        response_duplicated_user=self.client.post(reverse('signup'),data_duplicated_user)
        self.assertEquals(response_duplicated_user.status_code,200)
        #ユーザーオブジェクトが既に作られていることを確認
        #self.assertFalse(User.objects.exists())
        
        self.assertFormError(response_duplicated_user,'form','username','同じユーザー名が既に登録済みです。')


    def test_failure_post_with_invalid_email(self):
        #emailが有効な形式でないリクエストを送信するとき
        data_invalid_email={
             'email':'ex',
             'username':'sample',
             'password1':'example12345',
             'password2':'example12345',
         }
        response_invalid_email=self.client.post(reverse('signup'),data_invalid_email)
        self.assertEquals(response_invalid_email.status_code,200)
        self.assertFalse(User.objects.exists())
        form=SignupForm(data_invalid_email)
        self.assertTrue(form.errors['email'])

    def test_failure_post_with_too_short_password(self):
        #passwordが短すぎるとき
        data_too_short_password={
             'email':'example@example.com',
             'username':'sample',
             'password1':'example12345',
             'password2':'example12345',
         }
        response_too_short_password=self.client.post(reverse('signup'),data_too_short_password)
        self.assertEquals(response_too_short_password.status_code,200)
        self.assertFalse(User.objects.exists())
        form=SignupForm(data_too_short_password)
        self.assertTrue(form.errors['password2'])#password1からpassword2にしたらエラー治った。なんで？
        
    def test_failure_post_with_password_similar_to_username(self):
        #usernameに似たpasswordでリクエストを送信する
        data_similar_to_username={
            'email':'example@example.com',
             'username':'example12345',
             'password1':'example12345',
             'password2':'example12345',
        }
        response_similar_to_username=self.client.post(reverse('signup'),data_similar_to_username)
        self.assertFalse(User.objects.exists())
        self.assertEquals(response_similar_to_username.status_code,200)
        form=SignupForm(data_similar_to_username)
        self.assertTrue(form.errors['password2'])#ここはpassword1じゃなくて２みたい


    def test_failure_post_with_only_numbers_password(self):
        #すべて数字のパスワードでリクエストを送信する
        data_only_numbers_password={
            'email':'example@example.com',
             'username':'sample',
             'password1':'1111111111',
             'password2':'1111111111',
        }
        reponse_only_numbers_password=self.client.post(reverse('signup'),data_only_numbers_password)
        self.assertEquals(reponse_only_numbers_password.status_code,200)
        self.assertFalse(User.objects.exists())
        form=SignupForm(data_only_numbers_password)
        self.assertTrue(form.errors['password2'])

       
    def test_failure_post_with_mismatch_password(self): 
        #パスワード１と２が異なるデータでリクエストを送信する
        data_mismatch_password={
            'email':'example@example.com',
             'username':'sample',
             'password1':'example12345',
             'password2':'example123456',
        }
        #response_mismatch_password名前な
        response_mismatch_password=self.client.post(reverse('signup'),data_mismatch_password)
        self.assertFalse(User.objects.exists())
        self.assertEquals(response_mismatch_password.status_code,200)
        form=SignupForm(data_mismatch_password)
        self.assertTrue(form.errors['password2'])

class TestHomeView(TestCase):
    def test_success_get(self):
        response=self.client.get(reverse('home'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/home.html')


class TestLoginView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass


class TestLogoutView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
