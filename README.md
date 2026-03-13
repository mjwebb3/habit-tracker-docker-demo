# Cloud Habit Tracker

A simple containerized web application used to demonstrate how to go from a local application on your laptop to a cloud-ready container using Docker.

This project is used as a demo for the talk:

De tu laptop a AWS: introducción práctica a Docker
AWS Students Community Day

---

## What this project demonstrates

This repository shows how to:

* Build a simple web application
* Package the application using Docker
* Run it locally using Docker Compose
* Persist data using Docker volumes
* Prepare the application to run on AWS container services

---

## Application features

* User registration and login
* Personal habit tracking
* Streak counter
* Admin panel
* SQLite persistence
* Docker containerization

---

## Local architecture

Browser
↓
Docker Container
↓
Flask Web Application
↓
SQLite Database (Docker volume)

---

## Running the application locally

### Requirements

* Docker
* Docker Compose

---

### Start the application

Run the following command from the project root:

docker compose up -d --build

Then open your browser and go to:

[http://localhost:8080](http://localhost:8080)

---

## Demo accounts

Admin user

Email: [admin@demo.com](mailto:admin@demo.com)
Password: PruebaTestA

Demo user

Email: [user@demo.com](mailto:user@demo.com)
Password: PruebaTestE

Admin panel:

[http://localhost:8080/admin](http://localhost:8080/admin)

---

## Stop the application

docker compose down

---

## Reset demo data

If you want to reset the database and start with fresh demo data:

docker compose down
rm -f instance/habits.db
docker compose up --build

---

## Docker concepts demonstrated

This project illustrates several important Docker concepts:

* Docker images
* Containers
* Docker volumes
* Docker Compose
* Health checks

---

## From laptop to AWS

Once containerized, this application could be deployed to AWS using services such as:

* Amazon Elastic Container Registry (ECR)
* AWS App Runner
* Amazon Elastic Container Service (ECS)

Typical deployment flow:

Developer Laptop
↓
Docker Image
↓
Container Registry (ECR)
↓
Container Runtime (ECS or App Runner)

---

## Project structure

cloud-habit-tracker/

app/
  app.py
  db.py
  templates/

instance/
  habits.db

Dockerfile
docker-compose.yml
README.md

---

## Educational purpose

This project is intentionally simple so students can:

* Understand container basics
* Reproduce the demo locally
* Experiment with Docker
* Learn how containerized applications can move to the cloud

---

## License

MIT
