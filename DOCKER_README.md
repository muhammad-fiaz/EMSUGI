# EMSUGI Docker Guide

This guide provides steps to set up and run the **EMSUGI** application using Docker. Docker enables easy deployment and isolation of dependencies, making it simpler to get the application up and running without manual installation.

## Project Overview

The **EMSUGI** application is designed to gather and analyze emergency alerts. It uses generative AI to predict future incidents based on historical data and current trends, providing visual analytics and real-time monitoring to improve emergency response efficiency.


## Prerequisites

- **Docker**: Make sure Docker is installed on your machine. You can [download Docker here](https://www.docker.com/get-started).

## Docker Setup Instructions

### Step 1: Clone the Repository

Clone the EMSUGI repository from GitHub:

```bash
git clone https://github.com/muhammad-fiaz/EMSUGI.git
cd EMSUGI
```

### Step 2: Build the Docker Image

From the EMSUGI root directory (where the `Dockerfile` is located), build the Docker image using the following command:

```bash
docker build -t emsugi-app .
```

This command will create an image named `emsugi-app` based on the instructions provided in the `Dockerfile`.

### Step 3: Run the Docker Container

Once the image is built, you can run a container using:

```bash
docker run -p 5000:5000 emsugi-app
```

- The `-p 5000:5000` option maps port 5000 in the Docker container to port 5000 on your local machine. Adjust the ports as needed if there's a conflict with other applications.

### Step 4: Access the Application

After running the container, open your browser and navigate to:

```
http://127.0.0.1:5000/
```

The EMSUGI application should now be running in Docker, accessible from your local browser.

---

## Stopping the Container

To stop the running container, press `Ctrl + C` in the terminal where the Docker container is running or find the container ID with:

```bash
docker ps
```

Then stop it using:

```bash
docker stop <container_id>
```

---


## Troubleshooting

If you encounter any issues, ensure that Docker is running properly on your machine, and check for any errors during the build or run processes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.