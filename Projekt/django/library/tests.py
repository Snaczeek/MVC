from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Author, Book, Borrow

class BorrowViewTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Sienkiewicz", birth_date="1846-05-05")
        self.user = User.objects.create_user(username='kowalski', password='123')
        self.book = Book.objects.create(title="Quo Vaids", author=self.author, year=1896)

    def test_borrow_book_view(self):
        self.client.login(username='kowalski', password='123')
        respone = self.client.post(reverse('book_borrow', args=[self.book.id]))
        self.book.refresh_from_db()
        self.assertEqual(respone.status_code, 302)
        self.assertTrue(self.book.is_borrowed)
        self.assertEqual(Borrow.objects.count(), 1)

    def test_return_book_view(self):
        self.client.login(username='kowalski', password='123')
        borrow = Borrow.objects.create(book=self.book, user=self.user)
        self.book.is_borrowed = True
        self.book.save()
        response = self.client.post(reverse('book_return', args=[borrow.id]))
        self.book.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.book.is_borrowed)
        self.assertEqual(Borrow.objects.count(), 0)

    def test_borrow_already_borrowed_book(self):
        self.book.is_borrowed = True
        self.book.save()
        self.client.login(username='kowalski', password='123')
        respone = self.client.post(reverse('book_borrow', args=[self.book.id]))
        self.assertEqual(respone.status_code, 302)
        self.assertEqual(Borrow.objects.count(), 0)
        self.book.refresh_from_db()
        self.assertTrue(self.book.is_borrowed)

    def test_borrow_when_not_logged_in(self):
        response = self.client.post(reverse('book_borrow', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
        self.book.refresh_from_db()
        self.assertFalse(self.book.is_borrowed)
        self.assertEqual(Borrow.objects.count(), 0)

class BookCRUDViewTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Prus", birth_date="1847-08-20")
        self.superuser = User.objects.create_superuser(username='admin', password='123')
        self.normal_user = User.objects.create_user(username='kowalski', password='123')
        self.book = Book.objects.create(title="Lalka", author=self.author, year=1890)

    def test_superuser_can_add_book(self):
        self.client.login(username='admin', password='123')
        response = self.client.post(reverse('book_create'), {
            'title': 'Nowa ksiazka',
            'author': self.author.id,
            'year': 2023,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 2)
        self.assertTrue(Book.objects.filter(title="Nowa ksiazka").exists())

    def test_normal_user_cannot_add_book(self):
        self.client.login(username='kowalski', password='123')
        response = self.client.post(reverse('book_create'), {
            'title': 'Nielegalna ksiazka',
            'author': self.author.id,
            'year': 2023,
        })
        self.assertIn(reverse('login'), response.url) # view zamiast zwrocic 403 po prostu przekierowuje konta bez uprawnien do formularza z logowaniem
        self.assertEqual(Book.objects.count(), 1)

    def test_superuser_can_edit_book(self):
        self.client.login(username='admin', password='123')
        response = self.client.post(reverse('book_edit', args=[self.book.id]), {
            'title': 'Lalka – poprawiona',
            'author': self.author.id,
            'year': 1890,
        })
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Lalka – poprawiona')

    def test_normal_user_cannot_edit_book(self):
        self.client.login(username='kowalski', password='123')
        response = self.client.post(reverse('book_edit', args=[self.book.id]), {
            'title': 'Zmiana nielegalna',
            'author': self.author.id,
            'year': 1890,
        })
        self.assertIn(reverse('login'), response.url) 
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Lalka')

    def test_superuser_can_delete_book(self):
        self.client.login(username='admin', password='123')
        response = self.client.post(reverse('book_delete', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_normal_user_cannot_delete_book(self):
        self.client.login(username='kowalski', password='123')
        response = self.client.post(reverse('book_delete', args=[self.book.id]))
        self.assertIn(reverse('login'), response.url) 
        self.assertTrue(Book.objects.filter(id=self.book.id).exists())

class AuthorViewTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='123')
        self.normal_user = User.objects.create_user(username='kowalski', password='123')

    def test_superuser_can_create_author(self):
        self.client.login(username='admin', password='123')
        response = self.client.post(reverse('author_create'), {
            'name': 'Juliusz Słowacki',
            'birth_date': '1809-09-04',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.first().name, 'Juliusz Słowacki')

    def test_normal_user_cannot_create_author(self):
        self.client.login(username='kowalski', password='123')
        response = self.client.post(reverse('author_create'), {
            'name': 'Nielegalny Autor',
            'birth_date': '2000-01-01',
        })
        self.assertIn(reverse('login'), response.url) 
        self.assertEqual(Author.objects.count(), 0)
