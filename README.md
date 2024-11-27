<h1 style="text-align: center; color: yellow;">HouseHold Service Application</h1>

## Table of Contents
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Roles](#roles)
- [Core Functionalities](#core-functionalities)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction
The Household Services Application is a multi-user platform designed to connect customers with service professionals offering various home services. The application allows for seamless service management, user administration, and service request handling. This project aims to streamline the process of booking and managing household services.

## Technologies Used
- **Flask**: A micro web framework for Python used to build the application.
- **Jinja2**: Templating engine for rendering HTML pages.
- **Bootstrap**: Front-end framework for styling and responsive design.
- **SQLite**: Lightweight database for data storage and management.
- **HTML/CSS**: Markup and styling for the user interface.

## Features
- **User Roles**: Three distinct user roles - Admin, Service Professional, and Customer.
- **Admin Dashboard**: Manage users, services, and service requests.
- **Service Management**: Admin can create, update, and delete services.
- **Service Request Handling**: Customers can create and manage service requests.
- **User Authentication**: Secure login and registration for different user types.
- **Search Functionality**: Users can search for services by name or location.

## Roles
- **Admin**: 
  - Monitors and manages all users and services.
  - Approves and verifies service professionals.
  - Has access to the admin dashboard.

- **Service Professional**: 
  - Offers specific services to customers.
  - Manages service requests, accepting or rejecting them.

- **Customer**: 
  - Books service requests based on available services.
  - Provides feedback and reviews for completed services.

## Core Functionalities
1. **User Authentication**: Login and registration forms for all user types.
2. **Admin Dashboard**: A centralized hub for managing users and services.
3. **Service Management**: Create, edit, and delete services.
4. **Service Request Management**: Customers can create, edit, and close service requests.
5. **User and Service Search**: Enables users to find services and professionals efficiently.

## Installation
To set up the Household Services Application locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mohitrajrathor/HouseHold-Service-App.git
   cd household-Service-App
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   flask run
   ```

## Usage
- Navigate to `http://127.0.0.1:5000` in your web browser.
- Log in as the admin to manage users and services or register as a service professional or customer to use the service features.

## Contributing
Contributions are welcome! If you would like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Make your changes and commit them: `git commit -m 'Add YourFeature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a pull request.

## Contact
For inquiries or feedback, please contact:
- **Name**: Mohit Raj Rathor
- **Email**: mohitrajrathor@gmail.com
- **GitHub**: [@mohitrajrathor](https://github.com/mohitrajrathor)

<h5 style="text-align: center; color: yellow;">THE END</h5>