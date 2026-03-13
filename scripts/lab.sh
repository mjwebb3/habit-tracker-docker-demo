#!/bin/bash
echo "Building image..."
docker build -t habit-tracker .

echo "Running app on http://localhost:8080"
docker run --rm -p 8080:5000 habit-tracker

#!/bin/bash
docker compose up --build