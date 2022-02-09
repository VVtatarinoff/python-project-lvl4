## Docker usage:

After cloning of repository you could use docker for emulation of Task manager website.
For this:
1. Go to the directory docker
2. Build the images:
   docker-compose build
3. Run the app:
   docker-compose up -d
4. The application should run at 0.0.0.0:8000
5. To close the session:
    docker-compose down

Notes
    - you could specify your own environment variables in file .env_example
    - the docker would create volume postgres_tm
    - if you want the admin panel to be shown you should create a superuser:
        docker exec -it django_task_manager python manage.py createsuperuser

                            |
