[Link to the website](https://aldebaran-rahman-gloriousgoalsshop.pbp.cs.ui.ac.id/)

Explain how you implemented the checklist above step-by-step (not just by following the tutorial).

Answer:
1. Creating a new Django project
In this step, I created a new Django project. This is where I had to work with Windows Powershell and Git. One part of this step was to create an application "main" in the project. I then configured the routing in the project to run the "main" application by adding urlpatterns = [path('', show_main, name='show_main'),] in urls.py in the "main" directory.

2. Creating a new model
After creating a new Django project, I continued by creating a new model named "Product" with "name", "price", "description", "thumbnail", "category", and "is_featured" as mandatory attributes as well as "id", "stock", and "rating" as optional attributes. After this, I ran "python manage.py makemigrations" and "python manage.py migrate" to apply the model.

3. Creating a function in views.py
After creating a new model, I went on to create a function in views.py to return a page that displays the name of the application, my name, and my class. This part (views.py) can be thought as the step in which the logic of the website is written.

4. Creating a template
The file views.py should return a page that displays information. To actually display the information, I had to create an HTML file (main.html) to organise how the information should be displayed whenever someone accesses my website. If views.py manages what should be shown, then the template manages how it should be shown.

5. Deploying to Pacil Web Service (PWS)
After writing code, managing logic, and managing how the information should be shown on the website, I deployed my project to Pacil Web Service. This step is important because it allows other people to access my website.


Create a diagram showing the client request to the Django-based web application and its response, and explain the relationship between urls.py, views.py, models.py, and the HTML file in the diagram.

Answer:
![MVT/MTV Diagram](basic-django.png)
[Link to source:](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Home_page)

urls.py, views.py, models.py, and HTML file(s) work together as a system in order to show a Django-based website. First of all, when the website receives an HTTP request from a user, it is given to urls.py and urls.py sends that request to the correct part in views.py. Depending on the request, views.py can read data from models.py or write data to models.py. The HTML file(s) work with views.py in order to put information on a page. That page is then forwarded to the user based on their initial request. Overall, urls.py, views.py, models.py, and HTML(s) coordinate with each other to receive HTTP requests from users and respond accordingly to those requests.


Explain the role of settings.py in a Django project!

Answer:
For me, one description that works best in understanding the settings.py file in Django is that it is analogous to the settings on a mobile phone. The settings of a mobile phone can set the brightness of the phone, set how notifications should be displayed, set the phone is on silent mode, set the phone is on airplane mode, set it to use mobile data, and much more. The settings.py file in a Django project behaves similarly because, for example, allowed hosts can be edited so that it contains more host or domain names, time zone could be set to 'UTC', the language code can be set to 'en-us', and more. From these examples, I think that the role of the settings.py file  in a Django project allows Django developers to configure how their project should work and/or behave such that it aligns with their goals.


How does database migration work in Django?

Answer:
From what I understand, a Django model is a representation of a database table in Python. Migrations is how Django tracks any changes made to its database models. Specifically, migrations are orders to change the structure of the database table which is defined in the latest code for the model. In Django, "python manage.py makemigrations" and "python manage.py migrate" are two commands that must run in order so that a database migration can work. The command "python manage.py makemigrations" is usually used after a model has been changed and is used to create migrations for those changes. However, this does not apply the changes made to the database. To apply the changes made to the database, the command "python manage.py migrate" should be used. At its core, database migrations in Django work by using two commands that must be run sequentially where "python manage.py makemigrations" creates migration files based on the changes made to the model and "python manage.py migrate" applies the migration files to the database which updates its schema.


In your opinion, among all existing frameworks, why is the Django framework chosen as the starting point for learning software development?

Answer:
There many frameworks for software development. However, I think the main reason as to why
Django is chosen is the same reason a beginner would first learn programming. Based on my experience, learning Python is not as complicated as learning other programming languages due to its human-friendly syntax. Beginners can practice computational thinking using Python and apply it to other languages. Are there better programming languages than Python in terms of speed? Of course! C++ is one of them. C++ is a great language when speed matters a lot. For instance, competitive programming puts a lot of emphasis on speed because many solutions must perform under a certain time limit. However, C++ is not as beginner friendly as Python. How does this relate to Django? I think of Django as the Python version of a framework. Beginners who understand Python can quickly transition to Django to develop software and use the thinking process of developing websites in Django to other frameworks. Overall, in my opinion, Django is a good starting point for people to learn software development because it puts more emphasis on how to think as a software developer/engineer rather than focusing on the tiny details.


Do you have any feedback for the teaching assistant for Tutorial 1 that you previously completed?

Answer:
I think my teaching assistant during tutorial 1 was great! He is quite communicative and he responds to my questions nicely. Thank you!