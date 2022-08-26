# Weather_App_with_Auth0

Weather App is implemented using [openweathermap.org](openweather.org) to retrieve weather condition of various cities with caching of sussequent requests. User login and logout is implemented through Auth0 authentication along with Multi Factor authentication over sms and email, where the application is only accessible to registered users.

**Setting the environment**

       git clone https://github.com/iamsims/Weather_App_with_Auth0.git
       virtualenv venv
       source venv/bin/activate
       pip install -r requirements.txt
       python manage.py makemigrations 
       python manage.py migrate
       python manage.py createcachetable
       
       
 **Setup environment file**
 
       touch .env
       #Add AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN
       
       
 **Run the webserver**
 
       python manage.py runserver 3000
       
       
