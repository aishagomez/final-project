# Project Management Application

Welcome to the Project Management Application. This application is designed to help project managers efficiently manage their projects by providing features such as data visualization, insertion, updating, deletion, and report generation.

## Prerequisites

Before you can run the application, make sure you have the following prerequisites installed:

1. **Python 3.8+**
2. **Django 3.2+**
   
## Installation

Follow these steps to set up and run the application on your local environment.

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/project-management-app.git
    cd project-management-app
    ```

2. **Create a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure the database:**
    - Modify the `settings.py` file to configure your database (Choose ENGINE acording to your preferences).
      ```
      DATABASES = {
               'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
            }
      ```
    - Make migrations:
      ```sh
      python manage.py makemigrations
      ```
    - Apply the migrations:
      ```sh
      python manage.py migrate
      ```
    That should create all tables in your database.

5. **Create a superuser to access the Django admin:**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

Access the application in your browser at `http://127.0.0.1:8000`.

If you have any questions or suggestions, feel free to contact us at [aisha.gomez@yachaytech.edu.ec](mailto:aisha.gomez@yachaytech.edu.ec).
