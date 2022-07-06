from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from tweets.models import Tweet


class TestTweetCreateView(TestCase):
    def setUp(self):
        User.objects.create_user(username='yamada', email='asaka@test.com', password='wasurenaide1108')
        self.client.login(username='yamada', password='wasurenaide1108')

    def test_success_get(self):
        response_get = self.client.get(reverse('tweet:create'))
        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'tweets/tweets_create.html')

    def test_success_post(self):
        test_data = {'contents': '頑張ってテストコードを書いています'}
        response_post = self.client.post(reverse('tweet:create'), test_data)
        tweet = Tweet.objects.get(contents='頑張ってテストコードを書いています')
        self.assertRedirects(
            response_post,
            reverse('tweet:detail', kwargs={'pk': tweet.pk}),
            status_code=302,
            target_status_code=200,
        )

        self.assertTrue(Tweet.objects.exists())
        tweet_object = Tweet.objects.get(contents='頑張ってテストコードを書いています')
        self.assertEquals(tweet_object.contents, test_data['contents'])

    def test_failure_post_with_empty_content(self):
        data_empty = {'contents': ''}
        response_empty = self.client.post(reverse('tweet:create'), data_empty)
        self.assertEquals(response_empty.status_code, 200)
        self.assertFalse(Tweet.objects.exists())
        self.assertFormError(response_empty, 'form', 'contents', 'このフィールドは必須です。')

    def test_failure_post_with_too_long_content(self):
        data_too_long = {'contents': "f" * 213}
        response_too_long = self.client.post(reverse('tweet:create'), data_too_long)
        self.assertEquals(response_too_long.status_code, 200)
        self.assertFalse(Tweet.objects.exists())
        self.assertFormError(response_too_long, 'form', 'contents', 'この値は 200 文字以下でなければなりません( 213 文字になっています)。')


class TestTweetDetailView(TestCase):
    def test_success_get(self):
        User.objects.create_user(username='yamada', email='asaka@test.com', password='wasurenaide1108')
        self.client.login(username='yamada', password='wasurenaide1108')
        data = {'contents': '頑張ってテストコードを書いています'}
        self.client.post(reverse('tweet:create'), data)
        tweet = Tweet.objects.get(contents='頑張ってテストコードを書いています')
        response_get = self.client.get(reverse('tweet:detail', kwargs={'pk': tweet.pk}))
        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'tweets/tweets_detail.html')
        self.assertContains(response_get, data['contents'])


class TestTweetDeleteView(TestCase):
    def setUp(self):
        User.objects.create_user(username='yamada', email='asaka@test.com', password='wasurenaide1108')
        self.client.login(username='yamada', password='wasurenaide1108')
        data = {'contents': 'ワンピースの映画早く見たい'}
        self.client.post(reverse('tweet:create'), data)

    def test_success_post(self):
        tweet = Tweet.objects.get(contents='ワンピースの映画早く見たい')
        response_post = self.client.post(reverse('tweet:delete', kwargs={'pk': tweet.pk}))
        self.assertRedirects(response_post, reverse('accounts:home'), status_code=302, target_status_code=200)
        self.assertFalse(Tweet.objects.filter(contents='ワンピースの映画早く見たい').exists())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(reverse('tweet:delete', kwargs={'pk': 9999}))
        self.assertEquals(response.status_code, 404)
        self.assertTrue(Tweet.objects.filter(contents='ワンピースの映画早く見たい').exists())

    def test_failure_post_with_incorrect_user(self):
        User.objects.create_user(username='satou', email='wakou@test.com', password='wasuretene1108')
        self.client.login(username='satou', password='wasuretene1108')
        tweet = Tweet.objects.get(contents='ワンピースの映画早く見たい')
        response = self.client.post(reverse('tweet:delete', kwargs={'pk': tweet.pk}))
        self.assertEquals(response.status_code, 403)
        self.assertTrue(Tweet.objects.filter(contents='ワンピースの映画早く見たい').exists())


class TestFavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_favorited_tweet(self):
        pass


class TestUnfavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
