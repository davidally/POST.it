# POST.it - IS211_FinalProject

## About POST.it

Users can register and create their own accounts. Once logged in 
they are able to make posts to the main page where others are also visible. Users can edit or delete their posts and account information.

## Usage

Simply run:
```sh
python run.py
```
Then open localhost:5000 on your browser to view the web application.

## How It Works

This is a blogging application written in Python using the Flask framework.  
Design Pattern: MVC 

The application is packaged in a folder which includes 3 modules for each part of the MVC
pattern. The `models.py` contains the classes that form the structure each user's data including their posts. The views are contained in `forms.py` using the FlaskForm module from the flask addon WTForms. The classes in this module are what build the forms you see on the front-end, albeit accessed through the Jinja templating. Finally, the controller connecting the two would be our `routes.py`. Several methods and decorators here do various things from tracking user sessions, redirects, authentication, image resizing, and more. The backbone of this application utilizes SQLAlchemy and Sqlite3 for the database as well as the package LoginManager which also is used for authentication.