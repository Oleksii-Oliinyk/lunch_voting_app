### Lunch App
A Django project for restaurant management and employee lunch decision-making.

### Getting Started
These instructions will help you set up the project locally using Docker.

### Prerequisites
Docker and Docker Compose installed on your machine.

### Installation

1. Clone the Repository

Clone the repository from GitHub and navigate to the project directory:

        git clone https://github.com/Oleksii-Oliinyk/lunch_voting_app.git
        cd YourRepository

2. Create a .env File

Example .env file:

        SECRET_KEY=your_secret_key
        DATABASE_NAME=lunch_app_db
        DATABASE_USER=postgres
        DATABASE_PASSWORD=your_password
        DATABASE_HOST=db
        DATABASE_PORT=5432
        DEBUG=True

4. Build and start the services defined in docker-compose.yml. This command sets up both the PostgreSQL database and the Django app:

        docker-compose up --build

5. Apply Migrations

Run the database migrations to set up the database schema:

        docker-compose exec web python manage.py migrate
