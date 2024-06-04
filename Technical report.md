# Project Management Application

Welcome to the Project Management Application Technical report, here you can check some technical information about tools used and features. 
## Tools

This project management application is built using a combination of powerful technologies:

* **Backend Framework:**
    * **Django:** This project utilizes Django, a high-level Python web framework. Django is known for its rapid development features, clean design principles, and robust security measures. It provides a structured approach to building web applications, handling tasks like database interactions, URL routing, and user authentication.

* **Programming Language:**
    * **Python:** Python serves as the foundation for this application. It's a versatile and beginner-friendly language, making it a popular choice for web development. Python's readability and clear syntax contribute to the maintainability and scalability of this project.

* **Libraries:**
    * **Django Libraries:** The project leverages various built-in Django libraries for functionalities like handling HTTP requests and responses (django.http), interacting with database models (models.py), and rendering web pages using templates (django.shortcuts, django.template.loader).
    * **xhtml2pdf:** This library facilitates the generation of PDF reports from HTML templates. It converts the visual structure and content of the HTML into a well-formatted PDF document.

* **Frontend Technologies:**
    * **HTML:** HyperText Markup Language (HTML) forms the core structure of the user interface. HTML elements define the content and layout of web pages.
    * **CSS:** Cascading Style Sheets (CSS) manage the presentation of the application. CSS styles control the visual appearance of HTML elements, including fonts, colors, and layout.
    * **JavaScript (Optional):** While not explicitly mentioned, JavaScript can be used to enhance the user experience by adding interactivity and dynamic behavior to the web pages.
    * **json**: The json library is used for encoding and decoding JSON data. It enables the application to handle data exchange in JSON format, which is commonly used for web APIs and inter-application communication.

* **Template Engine:**
    * **Django Templates:** Django's templating system allows for efficient creation and management of user interfaces. HTML templates combined with Django template tags and logic provide a flexible way to structure web pages and integrate dynamic content.

By combining these technologies, this project management application offers a robust and user-friendly platform for managing projects, data, and reports.

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
