
# Task Management System Setup Instructions

1. **Clone the Repository**  
   Run the following commands:
   ```bash
   git clone https://github.com/Forevgit/TestProject.git
   cd TestProject
   ```

2. **Set Up the Environment Variables**  
   Create a `.env` file in the root directory with the following content:
   ```bash
   DB_NAME=task_management
   DB_USER=task_user
   DB_PASSWORD=secret
   DB_HOST=db
   DB_PORT=5432
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

3. **Build and Run Docker Containers**  
   Run the following command:
   ```bash
   docker-compose up --build
   ```

4. **Run Database Migrations**  
   Run the following command to apply migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a Superuser**  
   Run the following command to create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Access the Project**  
   Your web application should now be accessible at [http://localhost:8000](http://localhost:8000).

7. **API Endpoints**  
   You can use [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) to see primary endpoints.
