from rest_framework import serializers
from django.conf import settings
import requests
from django.utils.crypto import get_random_string
import json
import random
from post.models import Post, Like
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


class BotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ''

    def create(self, validated_data):
        number_of_users = settings.NUMBER_OF_USERS

        result = {'users': [], 'posts': [], 'likes': []}
        users = []
        for i in range(0, number_of_users):
            number_posts_per_user = random.randint(1, settings.MAX_POSTS_PER_USER)
            number_likes_per_user = random.randint(1, settings.MAX_LIKES_PER_USER)
            try:
                [username, password] = self.generate_username_password()
                result['users'].append(self.register_user(username, password))
                logger.debug('New user was registered. Username: %s' % username)
            except:
                logger.warning('There is some problem with user signup!')
                return ' {"success": False, "message": "There is some problem with user signup"}'
            try:
                token = self.get_token(username, password)
                logger.debug('Token was generated for user: %s' % username)
                users.append({'username': username,
                              'token': token,
                              "number_likes_per_user": number_likes_per_user,
                              "number_posts_per_user": number_posts_per_user})
            except:
                logger.warning('There is some problem with token creating')
                return '{"success": False, "message": "There is some problem with token creating"}'

            try:
                for post_index in range(0, number_posts_per_user):
                    result['posts'].append(self.create_post(token, username))
            except:
                logger.warning('There is some problem with post sending')
                return ' {"success": False, "message": "There is some problem with post sending"}'

        while self.exist_post_without_likes() and users:
            max_posts_lists = []
            for user in users:
                max_posts_lists.append(user["number_posts_per_user"])
            index_user_with_max_post = max_posts_lists.index(max(max_posts_lists))
            user_first = users[index_user_with_max_post]
            try:
                for like_index in range(0, user_first['number_likes_per_user']):
                    result['likes'].append(self.like_post(user_first['token'], user_first['username']))
                users.remove(user_first)
            except:
                logger.warning('There is some problem with liking posts')
                return ' {"success": False, "message": "There is some problem with like"}'
        return result

    @staticmethod
    def create_post(token, username):
        title_choice = ['Thank you', "%s is happy" % username, "You are the best", "This is a great honor for me",
                        "It is great", "Hi", "Hey", "Hello from %s" % username, "What a wonderful day",
                        "Hi from %s" % username]
        greeting = ['Hi', 'Hello', 'Hey', 'Morning', 'Good Morning']
        appeal = ['guys!', 'friends!', 'team!', 'ladies and gentlemen!']
        thanks = ['Thank you very much', 'Thank you so much', "Thank you a lot"]
        content1 = ['Good news', 'I have great news', 'What I wanted to say is',
                    'I am pleased to inform you']
        content2 = ['I am not a bot', 'I am a true %s' % username[:-2]]

        title = random.choice(title_choice)
        text = random.choice(greeting) + ' ' + random.choice(appeal) + '\n' + random.choice(
            thanks) + ' ' + random.choice(
            content1) + ' ' + random.choice(content2)
        payload = {'title': title, 'text': text}
        headers = {'Content-Type': 'application/json', 'Authorization': 'JWT %s' % token}
        result = requests.post(settings.URL_POST, data=json.dumps(payload), headers=headers)
        logger.debug('New post was created: %s' % title)
        if result.status_code == 201:
            return {'title': title, 'text': text, 'author': username}
        else:
            return {'result.status_code': result.status_code}

    @staticmethod
    def like_post(token, username):
        like = 1
        user_id = User.objects.get(username=username).id
        # users cannot like their own posts
        list_posts_id = Post.objects.exclude(author=user_id).values_list('pk', flat=True)

        post_id = random.choice(list_posts_id)
        # one user can like a certain post only once
        more_then_one_like_per_user = User.objects.get(username=username).id in Like.objects.filter(
            post=post_id).values_list("user", flat=True)
        user_has_post_without_likes = BotSerializer.if_user_has_post_without_likes(post_id)
        while more_then_one_like_per_user and user_has_post_without_likes:
            post_id = random.choice(list_posts_id)
            more_then_one_like_per_user = User.objects.get(username=username).id in Like.objects.filter(
                post=post_id).values_list("user", flat=True)
            user_has_post_without_likes = BotSerializer.if_user_has_post_without_likes(post_id)

        payload = {'post': post_id, 'like': like}
        headers = {'Content-Type': 'application/json', 'Authorization': 'JWT %s' % token}
        result = requests.post(settings.URL_LIKE, data=json.dumps(payload), headers=headers)
        logger.debug('User like post %s' % Post.objects.get(pk=post_id))

        if result.status_code == 201:
            return {'post_id': post_id, 'title': Post.objects.get(pk=post_id).title, 'like': like, 'user': username}
        else:
            return {'result.status_code': result.status_code}

    @staticmethod
    def generate_username_password():
        unique_id = get_random_string(length=2)
        names = ['Archimedes', 'Aristotle', 'Boyle', 'Darwin', 'Einstein', 'Faraday', 'Fibonacci', 'Franklin',
                 'Galilei',
                 'Gauss', 'Nobel', 'Pythagoras']
        username = random.choice(names) + '_' + unique_id
        password = "qwe123qwe123"
        return [username, password]

    @staticmethod
    def register_user(username, password):
        payload = {'username': username, 'email': username + '@test.te', 'password1': password,
                   'password2': password}
        headers = {'Content-Type': 'application/json'}
        result = requests.post(settings.URL_SIGNUP, data=json.dumps(payload), headers=headers)
        if result.status_code == 201:
            return {'username': username, 'email': username + '@test.te'}
        else:
            return {'success': False, 'username': username, 'email': username + '@test.te'}

    @staticmethod
    def get_token(username, password):
        payload = {'username': username, 'password': password}
        headers = {'Content-Type': 'application/json'}
        result = requests.post(settings.URL_TOKEN, data=json.dumps(payload), headers=headers)
        return json.loads(result.text)['token']

    @staticmethod
    def exist_post_without_likes():
        list_posts_id = Post.objects.all().values_list('pk', flat=True)
        list_post_with_likes = Like.objects.all().values_list('post_id', flat=True)
        for post_id in list_posts_id:
            if post_id not in list_post_with_likes:
                return True
        return False

    @staticmethod
    def if_user_has_post_without_likes(post_id):
        # user can only like random posts from users who have at least one post with 0 likes
        author = Post.objects.get(pk=post_id).author
        # Post.objects.filter(post=post_id).values_list("user", flat=True)
        list_posts_id = Post.objects.filter(author=author).values_list('pk', flat=True)
        list_post_with_likes = Like.objects.all().values_list('post_id', flat=True)
        for post_id in list_posts_id:
            if post_id not in list_post_with_likes:
                return True
        return False
