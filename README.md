# Flask Heroku App Template

This is a starter Flask app with necessary files required for a Heroku deployment. This app includes a form for creating "widgets" (anything you'd like), an attached sqlite db to store all of the "widgets", and a homepage for browsing through all of the created "widgets". View at 



Before starting, make sure to have a heroku account and install the Heroku CLI (command line interface): https://devcenter.heroku.com/articles/heroku-command-line

## Flask App

Steps to get Flask App working locally and configured to your desires

**1. login to virtual environment**

**2. Git Pull Repo
```bash
mkdir app_name_of_your_choosing
cd app_name_of_your_choosing
git init
git pull https://github.com/davcheng/flask-heroku-template.git
```
alternatively, cd into a project folder and run:
```bash
git clone https://github.com/davcheng/flask-heroku-template.git
```

**3. Initialize DB**
Update schema.sql to the model you would like
```
FLASK_APP=app.py flask initdb
```

**4. Run app locally to test**
```
FLASK_APP=app.py FLASK_DEBUG=1 flask run --host=0.0.0.0
```

**5. Push changes to git**


## Heroku Deployment Steps
**1. Update requirements.txt**
The requirements.txt notifies Heroku of what dependenices to install.
	```
	Flask==0.11.1
	Jinja2==2.7.3
	MarkupSafe==0.23
	Werkzeug==0.10.1
	gunicorn==19.6
	```

**2. Create a Procfile**
The Procfile is the equivalent of the "follow these procedures when you start up" file. Update it to use the name of your app (currently app.py yields "web: gunicorn app:app".
	```
	web: gunicorn [app name, e.g., if main.py, use "main"]:app
	```

**3. Create heroku app**

	```
	heroku create [app name]
	```

**4. Deply code**

	```
	git push heroku master
	```	
note, this will fail if requirements.txt is not created (will say no flask)

**5. ensure at least one instance of the app is running**

	```
	heroku ps:scale web=1
	```	
if so, will show something like "Scaling dynos... done, now running web at 1:Free"

**6. revel in glory**

	```bash
	heroku open
	```

**6b. wonder what happened**
if something is broken, use this command to view log files:

	```bash
	heroku logs
	```

source: https://devcenter.heroku.com/articles/getting-started-with-python#introduction