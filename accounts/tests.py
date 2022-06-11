from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import SESSION_KEY
from .models import User





class SignUpTests(TestCase):
    def test_success_get(self):
     
        response_get=self.client.get(reverse('accounts:signup'))
        self.assertEquals(response_get.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertTemplateUsed(response_get,'accounts/signup.html')
        

    def test_success_post(self):
        
        data_post = {
            'email':'example@example.com',
            'username':'sample',
            'password1':'testpassword',
            'password2':'testpassword',
            }
        response_post=self.client.post(reverse('accounts:signup'), data_post)
        
        self.assertRedirects(response_post, reverse('home'), status_code=302,target_status_code=200)  
        
        self.assertTrue(User.objects.filter(username='sample', email='example@example.com').exists())

       

    def test_failure_post_with_empty_form(self):
        data_empty_form = {
            'email':'',
            'username':'',
            'password1':'',
            'password2':'',
        }
        
        
        response_empty_form = self.client.post(reverse('accounts:signup'), data_empty_form) 
        self.assertEquals(response_empty_form.status_code, 200)
        
        self.assertFalse(User.objects.exists())

        
        self.assertFormError(response_empty_form, 'form','username', 'このフィールドは必須です。')
        self.assertFormError(response_empty_form, 'form', 'email', 'このフィールドは必須です。')
        self.assertFormError(response_empty_form, 'form', 'password1', 'このフィールドは必須です。')
        self.assertFormError(response_empty_form, 'form', 'password2', 'このフィールドは必須です。')

    def test_failure_post_with_empty_username(self):

        data_empty_username = {
             'email':'example@example.com',
             'username':'',
             'password1':'example12345',
             'password2':'example12345',
         }
        response_empty_username = self.client.post(reverse('accounts:signup'), data_empty_username)
        self.assertEquals(response_empty_username.status_code, 200)
        self.assertFalse(User.objects.exists())
        
        self.assertFormError(response_empty_username, 'form', 'username', 'このフィールドは必須です。')
        


         

    def test_failure_post_with_empty_email(self):

        data_empty_email = {
             'email':'',
             'username':'sample',
             'password1':'example12345',
             'password2':'example12345',
         }
        response_empty_email = self.client.post(reverse('accounts:signup'), data_empty_email)
        self.assertEquals(response_empty_email.status_code,200)
        self.assertFalse(User.objects.exists())
        
        self.assertFormError(response_empty_email, 'form', 'email', 'このフィールドは必須です。')

    def test_failure_post_with_empty_password(self):
        #ブランクのあるpaswordが送信された時
        data_empty_password = {
             'email':'example@example.com',
             'username':'sample',
             'password1':'',
             'password2':'',
         }
        response_empty_password = self.client.post(reverse('accounts:signup'), data_empty_password)
        self.assertEquals(response_empty_password.status_code, 200)
        self.assertFalse(User.objects.exists())
        
        self.assertFormError(response_empty_password, 'form', 'password2', 'このフィールドは必須です。')


    def test_failure_post_with_duplicated_user(self):
        #既に存在するユーザーを登録するリクエストを送った時
        data_duplicated_user = {
             'email':'example@example.com',
             'username':'sample',
             'password1':'example12345',
             'password2':'example12345',
         }
        
        
        
        User.objects.create(
             email='example@example.com',
             username='sample',
             password='example12345',
             
             )
        response_duplicated_user = self.client.post(reverse('accounts:signup'), data_duplicated_user)
        self.assertEquals(response_duplicated_user.status_code, 200)
        
        
        self.assertFormError(response_duplicated_user, 'form', 'username', '同じユーザー名が既に登録済みです。')


    def test_failure_post_with_invalid_email(self):
        #emailが有効な形式でないリクエストを送信するとき
        data_invalid_email = {
             'email':'ex',
             'username':'sample',
             'password1':'example12345',
             'password2':'example12345',
         }
        response_invalid_email = self.client.post(reverse('accounts:signup'), data_invalid_email)
        self.assertEquals(response_invalid_email.status_code, 200)
        self.assertFalse(User.objects.exists())
        
        self.assertFormError(response_invalid_email, 'form', 'email', '有効なメールアドレスを入力してください。')
        
    def test_failure_post_with_too_short_password(self):
        #passwordが短すぎるとき
        data_too_short_password = {
             'email':'example@example.com',
             'username':'sample',
             'password1':'test',
             'password2':'test',
         }
        response_too_short_password = self.client.post(reverse('accounts:signup'), data_too_short_password)
        self.assertEquals(response_too_short_password.status_code, 200)
        self.assertFalse(User.objects.exists())
        
        self.assertFormError(response_too_short_password, 'form', 'password2', 'このパスワードは短すぎます。最低 8 文字以上必要です。')
        
    def test_failure_post_with_password_similar_to_username(self):
        #usernameに似たpasswordでリクエストを送信する
        data_similar_to_username = {
            'email':'example@example.com',
             'username':'example12345',
             'password1':'example12345',
             'password2':'example12345',
        }
        response_similar_to_username = self.client.post(reverse('accounts:signup'), data_similar_to_username)
        self.assertFalse(User.objects.exists())
        self.assertEquals(response_similar_to_username.status_code, 200)
        
        self.assertFormError(response_similar_to_username, 'form', 'password2', 'このパスワードは ユーザー名 と似すぎています。')


    def test_failure_post_with_only_numbers_password(self):
        #すべて数字のパスワードでリクエストを送信する
        data_only_numbers_password={
            'email':'example@example.com',
             'username':'sample',
             'password1':'1111111111',
             'password2':'1111111111',
        }
        reponse_only_numbers_password = self.client.post(reverse('accounts:signup'), data_only_numbers_password)
        self.assertEquals(reponse_only_numbers_password.status_code, 200)
        self.assertFalse(User.objects.exists())
        
        self.assertFormError(reponse_only_numbers_password, 'form', 'password2', 'このパスワードは一般的すぎます。',  'このパスワードは数字しか使われていません。')
        
       
    def test_failure_post_with_mismatch_password(self): 
        #パスワード１と２が異なるデータでリクエストを送信する
        data_mismatch_password = {
            'email':'example@example.com',
             'username':'sample',
             'password1':'example12345',
             'password2':'example123456',
        }
        
        response_mismatch_password = self.client.post(reverse('accounts:signup'), data_mismatch_password)
        self.assertFalse(User.objects.exists())
        self.assertEquals(response_mismatch_password.status_code, 200)

        self.assertFormError(response_mismatch_password, 'form', 'password2', '確認用パスワードが一致しません。')


class TestHomeView(TestCase):
    def test_success_get(self):
        response = self.client.get(reverse('accounts:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/home.html')


class TestLoginView(TestCase):
    def test_success_get(self):
        response_get = self.client.get(reverse('accounts:login'))
        self.assertEquals(response_get.status_code,302)
        self.assertTemplateUsed(response_get,'accounts/login.html')

    def test_success_post(self):
        data_post = {
            'username':'山田太郎',
            'password':'tarou1108',
        }
        response_post= self.client.post(reverse('accounts:login'),data_post)
        self.assertRedirects(response_post,reverse('accounts:login'),status_code=302,target_status_code=200)
        self.assertIn(SESSION_KEY,self.client.session)

    def test_failure_post_with_not_exists_user(self):
        #存在しないusername,passwordを送信する
        data_not_exists_user={
            'username':'山田太郎',
            'password':'tarou1108',
        }
        response_not_exists_user=self.client.post(reverse('accounts:login'),data_not_exists_user)
        self.assertEquals(response_not_exists_user.status_code,200)
        self.assertFormError(response_not_exists_user, 'form', '','正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。')
        self.assertNotIn(SESSION_KEY,self.client.session)

    def test_failure_post_with_empty_password(self):
        data_with_empty_password={
            'username' : '山田太郎',
            'password' : '',
        }

        response_with_empty_password=self.client.post(reverse('accounts:login'),data_with_empty_password)
        self.assertEquals(response_with_empty_password.status_code,200)
        self.assertFormError(response_with_empty_password, 'form', 'password','このフィールドは必須です。')
        self.assertNotIn(SESSION_KEY,self.client.session)


class TestLogoutView(TestCase):
    def test_success_get(self):
        pass #response_logout=self.client.get


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
