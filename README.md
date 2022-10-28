# Food Delivery Application

## Installation Steps

Please review the ```technologies_used.txt``` file before getting started to know the exact versions of technologies used to build this project.

1. Clone the project from the repository using given command below<br><br>
    ```
    git clone https://github.com/harivamshi81189/adv_final_project.git
    ```
2. Create a Python Virtual Environment for installing all necessary packages for this project. Create the virtual environment using command below<br><br>
    ```
    python -m venv adv_django_venv
    ```
3. Activate the virtual environment to start working on the project<br><br>
    On Windows:
    ```
    adv_django_venv\Scripts\activate.bat
    ```
    On Unix or MacOS:
    ```
    source adv_django_venv/bin/activate
    ```
4. After successfully activating the virtual environment. Install Django package.<br><br>
    ```
    python -m pip install Django
    ```
5. Check if you have successfully installed Django using the command<br><br>
    ```
    python -m django --version
    ```
6. When you run the above command, you will ge the version number for the Django installed in the virtual environment. If you get an error or did not get the version number displayed. Please check the installation steps clearly and try again.
7. Using the ```requirements.txt``` file install the necessary packages required for this project. Use the command below to install the packages required for this project from requirements.txt file<br><br>
    ```
    pip install -r requirements.txt
    ```
8. After successful installation of all necessary packages, continue to the Execution Steps to run the application
<br><br>

## Database Setup
1. Install the latest version of postgreSQL
2. Setup the database for the project with name ```food_delivery_db```
3.  Configure the settings for database in settings.py<br>

    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'food_delivery_db',
            'USER': 'postgres',
            'PASSWORD': 'root',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
    ```

## Execution Steps
1. Make sure that you are in the directory of adv_final_project, if not change the directory using ```cd <path to adv_final_project>```
2.  Activate the virtual environment, if not already activated using the command below<br><br>
    On Windows:
    ```
    adv_django_venv\Scripts\activate.bat
    ```
    On Unix or MacOS:
    ```
    source adv_django_venv/bin/activate
    ```
3. If you activated the virtual environment you will see your terminal like this<br><br>
    ```
    (adv_django_venv) ...\adv_final_project>
    ```
4. Now, change the directory to food_delivery_app<br><br>
    ```
    cd food_delivery_app
    ```
5. Now, execute the command below to run the application.<br><br>
    ```
    python manage.py runserver
    ```
6. If you see the output like this, that means your application is running and you can click on the link given there to open the application in the browser.<br><br>
    ```
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    July 28, 2022 - 20:08:54
    Django version 4.0.6, using settings 'food_delivery_app.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
    ```
7. When you run the above command, if you something like below in your terminal output, run the command given in next step.<br><br>
    ```
    You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.
    ```
8. Run this command to apply the migrations to database.
    ```
    python manage.py migrate
    ```

## Loading dummy data to the website (recommended)
1. There is a file named ```data_script.py``` in the path food_delivery_app/foodie/default_data/data_script.py
2. Run the file using following command when you are in the project folder and activated the environment
    ```
    python manage.py < foodie/default_data/data_script.py
    ```
3. After running all the dummy data will be stored in the database, the default password for all the emails is ```foodie123```. Find the emails in the database under table ```auth_users```