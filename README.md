# library-service

A backend for a curious library that charges people for borrowing books.
Written in python using Django REST Framework.

## Features
* Browsable REST API with an incomplete swagger documentation;
* Create books, set prices, borrow them;
* View your borrow history as a user;
* View everyone's borrow history as an admin, having access to various filtering;
* Pay for the borrowings using Stripe.

## Installation

### Pre-requisites
* Python 3.10+
* Text editor

### Steps to install
1. Clone the repo:
    ```shell
    git clone https://github.com/mltdll/library-service.git
    ```
2. Acquire necessary tokens for your `.env` file:
    1. Stripe secret key: https://stripe.com;
    2. Telegram bot token: https://t.me/BotFather;
    3. Telegram chat id;
3. Create new `.env` file and past those values therein, as shown in `.env.example` file;
4. Install requirements:
    ```shell
    pip install -r requirements.txt
    ```
5. Configure Django project:
    ```shell
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Run the server (you'll need two terminal windows/tabs open):
    1. First:
        ```shell
         python manage.py qcluster
        ```
    2. Second:
        ```shell
         python manage.py runserver
        ```
