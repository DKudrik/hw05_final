
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache


from posts.models import User, Post, Group, Comment


class TestPostsApp(TestCase):

    def setUp(self):
        self.client_anon = Client()
        self.client_auth = Client()
        self.author = User.objects.create_user(username="Author")
        self.group = Group.objects.create(title="Тестовая группа", slug="test")
        self.text = "Текст"
        self.client_auth.force_login(self.author)

    def tearDown(self):
        cache.clear()

    def test_anon_user_post(self):
        """ Testing if an unauthorized user can create a post"""
        response = self.client_anon.post(
            reverse("new_post"),
            {"text": self.text, "author": AnonymousUser})
        url = f"{reverse('login')}?next={reverse('new_post')}"
        self.assertRedirects(response, url)

    def test_new_post_created(self):
        """Testing if a new post was created"""
        data = {
            'text': self.text,
            'group': self.group.id,
        }
        self.client_auth.post(
            reverse('new_post'), data)
        post = Post.objects.get(pk=1)
        with self.subTest():
            self.assertEqual(self.author, post.author)
        with self.subTest():
            self.assertEqual(self.group, post.group)
        with self.subTest():
            self.assertEqual(self.text, post.text)

    def test_correct_post_exists_at_linked_pages(self):
        """ Checking a new post appeared at all the pages """
        post = Post.objects.create(
            text=self.text,
            author=self.author,
            group=self.group
        )
        pages = (
            reverse("index"),
            reverse("profile", args=[self.author.username]),
            reverse("post", args=(self.author.username, post.pk)),
            reverse("group", args=[self.group.slug])
            )
        for page in pages:
            response = self.client_auth.get(page)
            with self.subTest("Пост не был добавлен на страницу " + page):
                if "paginator" in response.context:
                    self.assertIn(
                        post, response.context["paginator"].object_list)
                else:
                    self.assertEquals(post, response.context["post"])

    def test_post_edit(self):
        """ Checking post correction """
        post = Post.objects.create(
            author=self.author,
            group=self.group,
            text=self.text,
        )
        posts_before = Post.objects.all().count()
        data = {
            "text": "Новый текст",
            "group": "Новая группа",
        }
        response = self.client_auth.post(reverse(
            "post_edit",
            args=(self.author, post.id)),
            data,
            follow=True)
        posts_after = Post.objects.all().count()
        with self.subTest():
            self.assertEqual(response.status_code, 200)
        with self.subTest():
            self.assertEqual(posts_before, posts_after,
                             msg="Пост был создан заново, а не пересохранен")
        post.refresh_from_db()
        self.assertEqual(response.context["post"], post,
                         msg="Пост не был обновлен")

    def test_post_contains_image_tag(self):
        """Checking that after uploding a post with an image file
        the post page will contain an '<img' tag
        """
        with open("media/123.jpg", "rb") as img:
            response = self.client_auth.post(reverse("new_post"), {
                "author": self.author,
                "text": "post with image",
                "image": img},
                follow=True
            )
        self.assertContains(response, "<img")

    def test_index_profile_group_contain_image_tags(self):
        """Checking that after uploding a post with an image file
        the index, profile and group pages will contain an '<img' tag
        """
        with open("media/123.jpg", "rb") as img:
            response = self.client_auth.post(reverse("new_post"), {
                "author": self.author,
                "group": self.group.id,
                "text": "post with image",
                "image": img},
                follow=True
            )
        pages = (
            reverse("index"),
            reverse("profile", args=[self.author.username]),
            reverse("group", args=[self.group.slug])
        )
        for page in pages:
            response = self.client_auth.get(page)
            with self.subTest("Тега нет на странице " + page):
                self.assertContains(response, "<img")

    def test_not_image_upload(self):
        """ Checking that uploading of a non-image file is impossible"""
        with open("media/123.jpg", "rb") as img:
            response = self.client_auth.post(reverse("new_post"), {
                "author": self.author,
                "text": "post with image",
                "image": img},
                follow=True
            )
        self.assertFormError(
            response,
            "form",
            "image",
            "Загрузите правильное изображение. "
            "Файл, который вы загрузили, "
            "поврежден или не является изображением.",
            )

    def test_index_cache(self):
        """ Testing cache function will store an info"""
        response_1 = self.client_auth.get(reverse("index"))
        Post.objects.create(
            author=self.author,
            group=self.group,
            text=self.text,
        )
        response_2 = self.client_auth.get(reverse("index"))
        self.assertEqual(response_1.content, response_2.content)
        cache.clear()
        response_3 = self.client_auth.get(reverse("index"))
        self.assertNotEqual(response_1.content, response_3.content)

    def test_auth_user_subscribe_process(self):
        """ Testing subscribe system allow to follow/unfollow a user"""
        author = User.objects.create_user(username="author")
        self.client_auth.post(reverse(
            "profile_follow", args=[author.username]))
        response = self.client_auth.get(reverse(
            "profile", args=[author.username]))
        with self.subTest(" Подписка не удалась"):
            self.assertEqual(response.context["follower"], 1)
        self.client_auth.post(reverse(
            "profile_unfollow", args=[author.username]))
        response = self.client_auth.get(reverse(
            "profile", args=[author.username]))
        with self.subTest(" Отписка не удалась"):
            self.assertEqual(response.context["follower"], 0)

    def test_posts_from_subscribes(self):
        """ Testing that only a subscribed user will see a post
        of a following author in his follow page
        """
        author = User.objects.create_user(username="author_1")
        post = Post.objects.create(
            text=self.text,
            author=author,
            group=self.group
            )
        user_1 = User.objects.create_user(username="user_1")
        self.client_auth.force_login(user_1)
        self.client_auth.post(reverse(
            "profile_follow", args=[author.username]))
        response_1 = self.client_auth.get(reverse(
            "follow_index"))
        user_2 = User.objects.create_user(username="user_2")
        self.client_auth.force_login(user_2)
        response_2 = self.client_auth.get(reverse(
            "follow_index"))
        self.assertIn(post, response_1.context["paginator"].object_list)
        self.assertNotIn(post, response_2.context["paginator"].object_list)

    def test_auth_user_make_comment(self):
        """ Testing that only an authorized user can leave
        a comment
        """
        post = Post.objects.create(
            author=self.author,
            group=self.group,
            text=self.text,
        )
        self.client_auth.post(reverse(
            "add_comment",
            args=[
                post.author,
                post.id]),
            {"text": "Коммент"},
            follow=True)
        self.assertEqual(Comment.objects.count(), 1)


class TestServerResponses(TestCase):

    def test_response_404(self):
        url = "/kj3klfgmk65ov/"
        response = Client().get(url)
        self.assertEqual(response.status_code, 404)
