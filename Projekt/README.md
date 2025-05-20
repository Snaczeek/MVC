# 📚 System zarządzania cyfrową biblioteką

## 📄 Spis treści

* [Opis projektu](#opis-projektu)
* [Funkcjonalności](#funkcjonalności)
* [Struktura katalogów](#struktura-katalogów)
* [Instrukcja uruchomienia w Dockerze](#instrukcja-uruchomienia-w-dockerze)
* [Użytkowanie](#użytkowanie)
* [Testowanie](#testowanie)
* [Konta domyślne](#konta-domyślne)

---

## Opis projektu

**Biblioteka Cyfrowa** to aplikacja webowa stworzona w Django, służąca do zarządzania książkami, autorami i wypożyczeniami. Użytkownicy mogą wypożyczać i oddawać książki, a administratorzy zarządzać katalogiem.

Projekt uruchamiany jest za pomocą kontenerów Docker.

---

## Funkcjonalności

* 🔐 Rejestracja i logowanie użytkowników
* 📚 Przeglądanie listy książek
* 📖 Wypożyczanie i zwracanie książek
* 🎒 Przeglądanie aktualnie wypożyczonych książek (ekwipunek użytkownika)
* 🧑‍💼 Tylko administrator może:

  * dodawać, edytować i usuwać książki
  * dodawać autorów
* 🛡️ Ochrona widoków z użyciem `@login_required` i `@user_passes_test(is_admin)`
* 🧪 Testy jednostkowe pokrywające widoki

---

## Struktura katalogów

```
Projekt/
├── django/
│   ├── library/           # aplikacja Django (modele, widoki)
│   ├── mvc/               # główny projekt Django
│   ├── templates/         # szablony html
│   ├── db.sqlite3
│   └── manage.py
├── Dockerfile             # definicja obrazu Dockera
├── docker-compose.yml     # uruchamianie aplikacji przez Docker
├── requirements.txt       # zależności Pythona
└── README.md              # dokumentacja
```

---

## Instrukcja uruchomienia w Dockerze

1. Zainstaluj docker desktop: https://www.docker.com/

2. Wejdź do folderu Projekt/

3. Zbuduj kontener:

   ```bash
   docker-compose build
   ```

4. Wykonaj migracje bazy danych:

   ```bash
   docker-compose run web python manage.py migrate
   ```

5. Uruchom aplikację:

   ```bash
   docker-compose up
   ```

6. Wejdź na stronę: [http://localhost:8000](http://localhost:8000)

---

## Użytkowanie

* 🔐 Zaloguj się lub zarejestruj
* 📚 Przeglądaj dostępne książki
* 🔄 Wypożyczaj i zwracaj książki
* 🎒 Przejdź do "Moje książki" aby zobaczyć swój ekwipunek
* 🧑‍💼 Administrator może zarządzać biblioteką z poziomu interfejsu


---

## Testowanie

Aby uruchomić testy jednostkowe:

```bash
docker-compose run web python manage.py test
```

---

## Wymagania

* Docker
* Docker Compose


---

## Konta domyślne
[konto administratora]
* login: admin 
* hasło: 123

---

Projekt wykonany w ramach zaliczenia z programowania webowego (architektura MVC).
