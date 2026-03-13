# Workshop: From your laptop to Docker

This workshop walks you through running a containerized web application locally and understanding the basic Docker concepts behind it.

The goal is to help students understand how an application can move from a developer laptop to a containerized environment.

---

# Step 1 — Clone the repository

First, clone the project repository and move into the project directory.

git clone [https://github.com/ArturoGallart/habit-tracker-docker-demo.git](https://github.com/ArturoGallart/habit-tracker-docker-demo.git)
cd cloud-habit-tracker

---

# Step 2 — Inspect the project

Before running the application, explore the structure of the project.

Look at the following files:

Dockerfile
docker-compose.yml
app/app.py

Think about the following questions:

* What does the Dockerfile do?
* Which port is exposed by the container?
* Where is the database stored?

---

# Step 3 — Build the Docker image

Build the container image using Docker Compose.

docker compose build

This step reads the Dockerfile and prepares the image that will run the application.

---

# Step 4 — Run the container

Start the application using Docker Compose.

docker compose up

Once the container starts, open your browser and go to:

[http://localhost:8080](http://localhost:8080)

You should see the Cloud Habit Tracker application.

---

# Step 5 — Inspect the running container

Open a new terminal and run:

docker ps

You should see a container running called:

habit-tracker

This means Docker is running your application inside a container.

---

# Step 6 — View container logs

You can see the application logs using:

docker compose logs

Logs help you understand what the application is doing inside the container.

---

# Step 7 — Inspect the container

You can open a shell inside the container to explore its filesystem.

docker exec -it habit-tracker bash

Once inside the container, run:

ls /app

You will see the application code that was copied during the Docker build process.

---

# Step 8 — Stop the application

To stop the running containers, run:

docker compose down

This stops and removes the containers, but keeps the Docker image and volumes.

---

# Step 9 — Persistence demonstration

Start the application again:

docker compose up

Notice that your previously created habits are still there.

This happens because Docker volumes persist the database data even if the container stops.

---

# Next steps

Try experimenting with the project:

* Modify the Dockerfile and rebuild the image
* Add new habits in the application
* Restart the containers
* Explore Docker commands such as docker images and docker logs

This simple exercise demonstrates how containerized applications work and how they can be moved from a local environment to a cloud environment.
