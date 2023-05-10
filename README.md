Stock Management System
Introduction

The Stock Management System is a comprehensive inventory management system that provides businesses with a centralized location to monitor the movement of their goods. It is user-friendly, customizable, and provides a range of features to help businesses optimize their inventory levels and reduce waste, leading to cost savings and increased profitability.
Features

    Authentication: Allows users to authenticate with the system and manage their profile.
    Password Recovery: Enables users to recover lost passwords.
    Profile Update: Allows users to update their profile information.
    Order History: Provides a record of past orders.
    Create Shop: Allows users to create a new shop.
    CRUD Products: Provides create, read, update, and delete functionality for products.
    CRUD Orders: Provides create, read, update, and delete functionality for orders.
    Search: Enables users to search for products or orders.
    Pagination: Provides pagination functionality for large lists.

Installation

To install the Stock Management System, follow these steps:

    Clone the repository to your local machine.
    Create a virtual environment using python3 -m venv venv.
    Activate the virtual environment using source venv/bin/activate.
    Install the required dependencies using pip install -r requirements.txt.
    Run database migrations using python3 manage.py migrate.
    Start the server using python3 manage.py runserver.

Usage

The Stock Management System has three main components: Core App, User Authentication, and Vendor.

    Core App: Handles client purchases and related functionality.
    User Authentication: Handles user authentication and profile management.
    Vendor: Handles vendor CRUD functionality.

To use the system, simply follow the on-screen instructions and navigate to the relevant sections of the system. Screenshots and examples are provided where appropriate to help guide you.
Dependencies

    Pillow: Required for media uploads.

License

This project is licensed under the MIT License.
