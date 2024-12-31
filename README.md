# Photofy
#### Video Demo:  [Youtube video](https://www.youtube.com/watch?v=-61FIshVU3M)
#### Code: [GitHub repository](https://github.com/blu3army/cs50_final)
#### Description:

This is my CS50 final project, I designed and created a web application dedicated to photografy. It shows pictures that users upload and allow to ranking them by likes and sorting by hashtags. Photofy is a micro social network.

I used Python for the backend with the framework Flask. Sqlite3 for database. The frontend was made with Flask, Jinja2, Vanilla JS and of course, HTML.

**How Photofy works?**

Once we are in the app, firstly we can create an account going into /sign_up page, with an username and a password.

Then we can upload pictures by clicking on upload button and give it a caption with hashtags. The hashtags are important because users can filter pictures by them.

In the home page we can watch all pictures had been uploaded, sort them by likes, by creation date or by hashtags. Also we can enter on any profile user to watch all pictures that it uploaded.

Logged users can give likes to the pictures, so this is going to affect when sorting by likes.


**How frontend works?**

The frontend is divided into several html templates, each one is a response from a route in app.py. It has a layout and navbar file, they are present in all templates using Jinja2 template inherit.
For the behavior I have used Vanilla JavaScript (without framework), you can see when a user click on a button like or when search for a hashtag, JavaScript is responsible for open that search window or refresh like buttons. Also when user upload a picture, JavaScript changes neutral background for an imagen that user selected.


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


**Likes System**

This is one of the main Photofy characteristics, any user can give like to any picture, wheter it's his or someone else's. For that in the backend I created one tables for likes, each one has a references to an user_id and a photo_id, the table has an unique restriction between photo_id and user_id then cannot duplicate a like, it's mean that one user only can give one per picture. When a user take off a like, this is deleted from table. In this way we can sort photos by likes, and like it has creation date, we also sort by date range (weekly, monthly, yearly, all times)

**Hashtags System**

When a user create a post, it can upload a picture and add a caption. In caption user should add hashtags (#whatever_word). Then we can filter pictures by hashtags. To achieve this, I created two tables: one for hashtags (id and title) and other that related photos with hashtags (I called it hashtags_photos). It last has these columns: id | photo_id | hashtag_id, so when user create a post, the app catch every hashtag from caption, deleted duplicates, check if doesn't exist, create hashtags and for last linked them with the post by the table hashtags_photos. Hashtag table has a unique restriction for title, so we never can two hashtags with the same title. Hashtags_photos tables has an unique multiple column restriction bewteen photo_id and hashtag_id. In this we can sort photos by hashtags and we can make a hashtag ranking, to see what hashtag is more popular or be on trend?


