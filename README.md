# Photofy
#### Video Demo:  [Youtube video](https://www.youtube.com/watch?v=-61FIshVU3M)
#### Description:

This is my CS50 final project, I designed and created a web application dedicated to photografy. It shows pictures that users upload and allow to ranking them by likes and sorting by hashtags. Photofy is a micro social network.

I used Python for the backend with the framework Flask. Sqlite3 for database. The frontend was made with Flask, Jinja2, Vanilla JS and of course, HTML.

**How Photofy works?**

Once we are in the app, firstly we can create an account going into /sign_up page, with an username and a password.

Then we can upload pictures by clicking on upload button and give it a caption with hashtags. The hashtags are important because users can filter pictures by them.

In the home page we can watch all pictures had been uploaded, sort them by likes, by creation date or by hashtags. Also we can enter on any profile user to watch all pictures that it uploaded.

Logged users can give likes to the pictures, so this is going to affect when sorting by likes.


**How backend works?**

app.py: this is the hearth of the application, this file has objective of handling routes, serving templates files, connecting with database classes. App starts here.

/database: here we can find classes that handle the relation between the app and the database, each class can connect to database to get, create or update info. I ordered in different files, each one related to an "object", ex: users.db handles all the transactions that an user need when the app runs by UsersDB class.
I used sqlite3 to storage databases.
In init_database.py file we can find the tables schemas.

/services: this init the storage that is used when a picture is upload. I chose Supabase for this task.

/templates: In there are the collection of templates. layout.html is the layout of every other templates and navbar.html is the nav. In /components folders are templates that had been embedded into others.

/src: I used TailwindCSS to manage CSS styles. input.css is the file that will proccess in every modification. Tailwind needs NodeJS for that

/static: files that's going serving in static manner

photofy_design.drawio: shows a simple wireframe of the app
