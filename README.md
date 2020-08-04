# PizzaShop
Demo project of an ecommerce website on Django.

# Build:
Recommended to install venv with django and pillow.
1. In the project directory:

```
python -m venv venv
source venv/bin/activate
pip install django
pip install pillow
```

2. then run

``` 
cd pizzaShop
python manage.py migrate
python manage.py runserver
```

3. Main page is available at 127.0.0.1:8000

# Features
* You can start adding your pizzas to cart immediately, your order will be saved in your cookies, then after completing it, it will also be saved.
* You can also sign up and then log in at any time, then your orders and cart will be attached to your account.
* You can switch between currencies using currency switch at the navbar.



