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

## Features

### Main Pages

- **Home**: Overview of all projects and their current status.
- **About**: Information about the Project Management Application.

### Data Management Features

- **View Table**: View detailed data of tables related to projects, employees, tasks, budgets, and more.
- **Insert**: Add new entries to various tables for creating projects, tasks, budgets, and other entities.
- **Get**: Retrieve attributes from specified tables to find and display specific information.
- **Update**: Modify existing entries in any table to keep information up to date and accurate.
- **Delete**: Delete entries from tables that are no longer needed or were added by mistake.

### Reports

- **Generate Report**: Select a project to generate a detailed report that includes activities, budgets, expenses, and deliverables.

## Endpoints

### `manage`

This endpoint handles the display of details and related entities for specific tables such as `Project`, `Activity`, `Budget`, `Employee`, and `Expense`.

### `export_pdf`

This endpoint allows exporting project reports in PDF format.

### `show_table`

Displays the data of the selected table.

### `insert_table`

Inserts new records into the selected table.

### `delete_object`

Deletes a specific record from the selected table.

### `get_object`

Retrieves attributes from specified tables.

### `update_object`

Updates specific records in the selected table.

## Contact

If you have any questions or suggestions, feel free to contact us at [aisha.gomez@yachaytech.edu.ec](mailto:aisha.gomez@yachaytech.edu.ec).
