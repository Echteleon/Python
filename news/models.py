from django.db import models
from datetime import datetime

name1 = 'name1 last_name1'
name2 = 'name2 last_name2'

AUTHORS = [
    (name1, 'name1'),
    (name2, 'name2')
]


class Author(models.Model):
    full_name = models.CharField(max_length=255, choices=AUTHORS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now=True)
    article = models.ManyToManyField(Category, through='PostCategory')
    rating = models.FloatField(default=0)

    @property
    def preview(self):
        return self.preview

    @preview.setter
    def preview(self):
        new_str = ""
        n = 0
        while (n < 124):
            for i in self.text:
                new_str[i] = self.text[i]

        new_str[125] = '...'
        return new_str


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    time_in = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0)

    @property
    def like(self):
        return self.like

    @like.setter
    def like(self):
        return self.rating - 1

    @property
    def dislike(self):
        return self.like

    @like.setter
    def dislike(self):
        return self.rating - 1