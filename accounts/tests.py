from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import User

from .models import User, Profile, user_is_created
from mysite import settings




class SignUpTests(TestCase):
    def test_success_get(self):
     
        response_get = self.client.get(reverse('accounts:signup'))
        self.assertEquals(response_get.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertTemplateUsed(response_get, 'accounts/signup.html')
        

    def test_success_post(self):
        
        data_post = {
            'email': 'example@example.com',
            'username': 'sample',
            'password1': 'testpassword',
            'password2': 'testpassword',
            }
        response_post = self.client.post(reverse('accounts:signup'), data_post)
        
        self.assertRedirects(response_post, reverse('accounts:home'), status_code=302, target_status_code=200)  
        
        self.assertTrue(User.objects.filter(username='sample', email='example@example.com').exists())
        self.assertIn(SESSION_KEY, self.client.session)

       

    def test_failure_post_with_empty_form(self):
        data_empty_form = {
            'email': '',
            'username': '',
            'password1': '',
            'password2': '',
        }
        
        
        response_empty_form = self.client.post(reverse('accounts:signup'), data_empty_form) 
        self.assertEquals(response_empty_form.status_code, 200)
        
        self.assertFalse(User.objects.exists())

        
        self.assertFormError(response_empty_form, 'form', 'username', 'このフィールドは必須です。')
        self.assertFormError(response_empty_form, 'form', 'email', 'このフィールドは必須です。')
        self.assertFormError(response_empty_form, 'form', 'password1', 'このフィールドは必須です。')
        self.assertFormError(response_empty_form, 'form', 'password2', 'このフィールドは必須です。')

    def test_failure_post_with_empty_username(self):

        data_empty_username = {
             'email': 'example@example.com',
             'username': '',
             'password1': 'example12345',
             'password2': 'example12345',
         }
        response_empty_username = self.client.post(reverse('accounts:signup'), data_empty_username)
        self.assertEquals(response_empty_username.status_code, 200)
        self.assertFalse(User.objects.exists())
        
        self.assertFormError(response_empty_username, 'form', 'username', 'このフィールドは必須です。')
        


         

    def test_failure_post_with_empty_email(self):

        data_empty_email = {
             'email': '',
             'username': 'sample',
             'password1': 'example12345',
             'password2': 'example12345',
         }
        response_empty_email = self.client.post(reverse('accounts:signup'), data_empty_email)
        self.assertEquals(response_empty_email.status_code, 200)
        self.assertFalse(User.objects.exists())
        
        self.assertFormError(response_empty_email, 'form', 'email', 'このフィールドは必須です。')

    def test_failure_post_with_empty_password(self):
        #ブランクのあるpaswordが送信された時
        data_empty_password = {
             'email': 'example@example.com',
             'username': 'sample',
             'password1': '',
             'password2': '',
         }
        response_empty_password = self.client.post(reverse('accounts:signup'), data_empty_password)
        self.assertEquals(response_empty_password.status_code, 200)
        self.assertFalse(User.objects.exists())
        
        self.assertFormError(response_empty_password, 'form', 'password2', 'このフィールドは必須です。')


    def test_failure_post_with_duplicated_user(self):
        #既に存在するユーザーを登録するリクエストを送った時
        data_duplicated_user = {
             'email': 'example@example.com',
             'username': 'sample',
             'password1': 'example12345',
             'password2': 'example12345',
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
             'email': 'ex',
             'username': 'sample',
             'password1': 'example12345',
             'password2': 'example12345',
         }
        response_invalid_email = self.client.post(reverse('accounts:signup'), data_invalid_email)
        self.assertEquals(response_invalid_email.status_code, 200)
        self.assertFalse(User.objects.exists())
        
        self.assertFormError(response_invalid_email, 'form', 'email', '有効なメールアドレスを入力してください。')
        
    def test_failure_post_with_too_short_password(self):
        #passwordが短すぎるとき
        data_too_short_password = {
             'email': 'example@example.com',
             'username': 'sample',
             'password1': 'test',
             'password2': 'test',
         }
        response_too_short_password = self.client.post(reverse('accounts:signup'), data_too_short_password)
        self.assertEquals(response_too_short_password.status_code, 200)
        self.assertFalse(User.objects.exists())
        
        self.assertFormError(response_too_short_password, 'form', 'password2', 'このパスワードは短すぎます。最低 8 文字以上必要です。')
        
    def test_failure_post_with_password_similar_to_username(self):
        #usernameに似たpasswordでリクエストを送信する
        data_similar_to_username = {
            'email': 'example@example.com',
             'username': 'example12345',
             'password1': 'example12345',
             'password2': 'example12345',
        }
        response_similar_to_username = self.client.post(reverse('accounts:signup'), data_similar_to_username)
        self.assertFalse(User.objects.exists())
        self.assertEquals(response_similar_to_username.status_code, 200)
        
        self.assertFormError(response_similar_to_username, 'form', 'password2', 'このパスワードは ユーザー名 と似すぎています。')


    def test_failure_post_with_only_numbers_password(self):
        #すべて数字のパスワードでリクエストを送信する
        data_only_numbers_password={
            'email': 'example@example.com',
             'username': 'sample',
             'password1': '1111111111',
             'password2': '1111111111',
        }
        reponse_only_numbers_password = self.client.post(reverse('accounts:signup'), data_only_numbers_password)
        self.assertEquals(reponse_only_numbers_password.status_code, 200)
        self.assertFalse(User.objects.exists())
        
        self.assertFormError(reponse_only_numbers_password, 'form', 'password2', 'このパスワードは一般的すぎます。',  'このパスワードは数字しか使われていません。')
        

    def test_failure_post_with_mismatch_password(self): 
        #パスワード１と２が異なるデータでリクエストを送信する
        data_mismatch_password = {
            'email': 'example@example.com',
             'username': 'sample',
             'password1': 'example12345',
             'password2': 'example123456',
        }
        
        response_mismatch_password = self.client.post(reverse('accounts:signup'), data_mismatch_password)
        self.assertFalse(User.objects.exists())
        self.assertEquals(response_mismatch_password.status_code, 200)
        self.assertFormError(response_mismatch_password, 'form', 'password2', '確認用パスワードが一致しません。')


class TestHomeView(TestCase):
    def setUp(self):
        data = {
            'username': 'yamada',
            'email': 'asaka@test.com',
            'password1': 'wasurenaide1108',
            'password2': 'wasurenaide1108',
        }
        self.client.post(reverse('accounts:signup'), data)
        

    def test_success_get(self):
        response = self.client.get(reverse('accounts:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/home.html')


class TestLoginView(TestCase):

    def setUp(self):
        User.objects.create_user(username='yamada', email='asaka@test.com', password='wasurenaide1108')
        self.url = reverse('accounts:login')
   
    def test_success_get(self):
        response_get = self.client.get(self.url)
        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'accounts/login.html')

    def test_success_post(self):
        
        data_post = {
            'username':'yamada',
            'password':'wasurenaide1108',
        }
       
        
        response_post = self.client.post(self.url, data_post)
        
        self.assertRedirects(response_post, reverse(settings.LOGIN_REDIRECT_URL), status_code=302, target_status_code=200)
        self.assertIn(SESSION_KEY, self.client.session)

       
        
    def test_failure_post_with_not_exists_user(self):
        #存在しないusername,passwordを送信する
        data_not_exists_user = {
            'username': 'aaaaaaaaaa',
            'password': 'Hasse118',
        }
        response_not_exists_user = self.client.post(self.url, data_not_exists_user)
        self.assertEquals(response_not_exists_user.status_code, 200)
        self.assertFormError(response_not_exists_user, 'form', '', '正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。')
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        data_with_empty_password = {
            'username' : '長谷川滉大',
            'password' : '',
        }

        response_with_empty_password=self.client.post(self.url, data_with_empty_password)
        self.assertEquals(response_with_empty_password.status_code, 200)
        self.assertFormError(response_with_empty_password, 'form', 'password', 'このフィールドは必須です。')
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):

    def setUp(self):
        data = {
            'username': 'yamada',
            'email': 'asaka@test.com',
            'password1': 'wasurenaide1108',
            'password2': 'wasurenaide1108',
        }
        self.client.post(reverse('accounts:signup'), data)

    def test_success_logout(self):
        response = self.client.get(reverse('accounts:logout'))
        
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL), status_code=302, target_status_code=200)
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def setUp(self):
         data = {
            'username': 'yamada',
            'email': 'asaka@test.com',
            'password1': 'wasurenaide1108',
            'password2': 'wasurenaide1108',
        }
         self.client.post(reverse('accounts:signup'), data)

  
    def test_success_get(self):
        users = Profile.objects.get()
        response_get = self.client.get(reverse('accounts:user_profile', kwargs={'pk':users.pk}))
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'accounts/profile.html')

    def test_failure_get_with_not_exists_user(self):
        response = self.client.get(reverse('accounts:user_profile', args=[1000]))
        self.assertEqual(response.status_code, 404)


class TestUserProfileEditView(TestCase):

    def setUp(self):
        data = {
            'username': 'yamada',
            'email': 'asaka@test.com',
            'password1': 'wasurenaide1108',
            'password2': 'wasurenaide1108',
        }
        self.client.post(reverse('accounts:signup'), data)
        

    def test_success_get(self):
        user = Profile.objects.get()
        url = reverse('accounts:user_profile_edit', kwargs={'pk':user.pk})
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'accounts/profile_edit.html')

    def test_success_post(self):
        data_post = {
            'hobby': 'サッカー',
            'introduction': '全国の山田太郎はいつも代表の名前になっている',
        }
        user = Profile.objects.get()
        response_post = self.client.post(reverse('accounts:user_profile_edit', kwargs={'pk':user.pk}), data_post)
        self.assertRedirects(response_post, reverse('accounts:user_profile', kwargs={'pk':user.pk}), status_code=302, target_status_code=200)
        user_object = Profile.objects.get()
        self.assertEqual(user_object.hobby, data_post['hobby'])
        self.assertEqual(user_object.introduction, data_post['introduction'])

    def test_failure_post_with_not_exists_user(self):
        #存在しないユーザーに対して有効なprofileのデータでリクエストを送信する
        response = self.client.get(reverse('accounts:user_profile', args=[1000]))
        self.assertEqual(response.status_code, 404)
        
    def test_failure_post_with_incorrect_user(self):
        #ほかのユーザーに対して有効なprofileのデータでリクエストを送信する
        incorrect_user_data = {
            'hobby': '存在しない',
            'introduction': 'ドッペルゲンガーを探すこと'
        }
        
        response = self.client.post(reverse('accounts:user_profile_edit', kwargs={'pk':99}), incorrect_user_data)
        self.assertEquals(response.status_code, 403)
        self.assertFalse(User.objects.filter(username='satou').exists())
        

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
