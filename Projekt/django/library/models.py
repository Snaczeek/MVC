from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.birth_date})"

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.year})"

class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} -> {self.user.username} ({self.date})"
