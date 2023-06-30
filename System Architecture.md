# System Architecture

## Components

- **YouTube Data API**: Used to search for videos with Hindi subtitles and to download the subtitles.
- **Message queue and Message broker**: To allowing application to do background processing.
- **Search and Download Service**: A service that communicates with the YouTube Data API to search for videos and download subtitles.
- **Database (PostgreSQL)**: A PostgreSQL database to store the video metadata (VideoID) and subtitles.
- **Grafana (optional)**: A tool for monitoring and visualization, integrated with the PostgreSQL database to create dashboards.
- **Feedback Loop Service**: A service that analyzes the subtitles downloaded to enhance the search queries for subsequent requests.

## Data Flow

1. The Scheduler triggers the Search and Download Service at specified intervals.
2. The Search and Download Service sends requests to the YouTube Data API to search for videos with Hindi subtitles.
3. For each video found, the Search and Download Service downloads the subtitles and video metadata.
4. The service stores the subtitles and video metadata in the PostgreSQL database. It uses the video's unique ID as a hash key to avoid downloading duplicate subtitles.
5. The Feedback Loop Service analyzes the subtitles to identify trends, keywords, and phrases. It uses this information to improve and refine the search queries used by the Search and Download Service.
6. Grafana is connected to the PostgreSQL database. Dashboards are set up to monitor the data being stored and to visualize metrics like the number of subtitles downloaded, API quota usage, etc.

### **Feedback Loop Service**

This service is responsible for analyzing the subtitles downloaded and using this data to improve the search queries for subsequent requests.

### Optional

1. **Natural Language Processing (NLP)**: Use NLP techniques to process the subtitles and extract keywords, phrases, and topics.
2. **Query Enhancement**: Use the extracted information to refine or expand the search queries used by the Search and Download Service.
3. **Monitoring and Metrics**: Monitor the impact of the updated search queries on the quality and relevance of the subtitles downloaded. Use Grafana to visualize these metrics.

## Technology Stack

- **YouTube Data API**: For searching and downloading subtitles.
- **Python**: As a programming language for the Search and Download Service.
- **PostgreSQL**: As a database to store video metadata and subtitles.
- **Celery:** Task Queue
- **RabbitMQ** - Message Broker
- **Grafana**: For monitoring and visualization.
- **Docker**: For containerization, which will help in scaling and deploying the services.

## Deployment

The services can be containerized using Docker and deployed on a cloud platform like AWS, Azure, or GCP.

- **AWS RDS**: For hosting the PostgreSQL database.
- **AWS EC2**: For hosting the Search and Download Service.
- **Grafana Cloud or self-hosted on EC2**: For monitoring and visualization.

## Security & Compliance

- Ensure that the system complies with the terms of service of the YouTube Data API.
- Secure the PostgreSQL database by restricting access and encrypting data.
- Regularly monitor and audit the logs.