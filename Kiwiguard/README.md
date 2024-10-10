# Kiwiguard

Real-time system monitoring dashboard for servers and containers

## Overview
kiwiguard is a real-time system monitoring dashboard that collects, processes, and displays server and container metrics. It helps users track CPU, memory, and disk usage in real-time from multiple servers or containers.

The project consists of two main components:
* Collector: The dashboard and API responsible for receiving and visualizing the metrics.
* Agent: A lightweight script running on each server/container that gathers system metrics and sends them to the collector.

## Features

* **Real-time Monitoring**: Track CPU, memory, and disk usage across multiple servers and containers.
* **Lightweight Agents**: Minimal performance impact on monitored systems.
* **Scalable Architecture**: Easily add new agents to monitor additional systems.
* **User-Friendly Dashboard**: Visualize metrics with an intuitive web interface built with FastAPI.
* **Dockerized Deployment**: Simplify setup and deployment using Docker containers.

## Prerequisites

* Docker - The easiest way to install Docker is to install Docker Desktop which does all the hard parts for you.
https://www.docker.com/products/docker-desktop/
* GitHub installed locally unless you just download the repo through the website.

## Installation
### Clone the Repository

```
git clone https://github.com/yourusername/kiwiguard.git
```
```
cd kiwiguard 
```

## Install Docker


## Setting Up the Collector
1. Navigate to the collector directory:
```
cd collector
```
2. Build the Docker image for the collector:

```
docker build -t kiwiguard-collector .
```
3. Run the Collector container:
```
docker run -d --name collector -p 80:80 kiwiguard-collector
```
The collector API and dashboard will be accessible at http://localhost.


## Setting Up the Agent
For each server or container you wish to monitor:

1. Navigate to the agent directory:
```
cd agent
```
2. Build the Docker image for the agent:

```
docker build -t kiwiguard-agent .
```
3. Run the agent container:
```
docker run -d --add-host=host.docker.internal:host-gateway kiwiguard-agent
```

The agent will start collecting metrics and sending them to the collector.

## Usage
* Access the kiwiguard dashboard at http://localhost:8000 to view real-time metrics.
* Use the dashboard to monitor CPU, memory, and disk usage across all connected agents.

## Directory Structure

```
kiwiguard/
├── agent/
│   ├── app/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── collector/
│   ├── app/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── dashboard/
│   ├── app/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
└── README.md
```


## Contributing
This project is for Max McGregors portfolio use only.

## License
This project is proprietary and for Max McGregor's portfolio use only. No copying, distribution, or personal use is permitted without explicit permission from the author.

## Acknowledgements
FastAPI for the web framework.
Docker for containerization.
Inspired by the need for simple and effective system monitoring tools.