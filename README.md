# Flask Heroku App Template

Starter Flask App with necessary deployment files required for Heroku

Heroku Deployment Files Required
1. Create requirements.txt
include: 
	
	```
	Flask==0.11.1
	Jinja2==2.7.3
	MarkupSafe==0.23
	Werkzeug==0.10.1
	gunicorn==19.6
	```

2. Create a Procfile

	```
	web: gunicorn [app name, e.g., if main.py, use "main"]:app
	```

3. Create heroku app

	```
	heroku create [app name].heroku.com
	```

4. Deply code

	```
	git push heroku master
	```	
note, this will fail if requirements.txt is not created (will say no flask)

5. ensure at least one instance of app is running

	```
	heroku ps:scale web=1
	```	
if so, will show something like "Scaling dynos... done, now running web at 1:Free"

6. revel in glory

	```bash
	heroku open
	```

source: https://devcenter.heroku.com/articles/getting-started-with-python#introduction