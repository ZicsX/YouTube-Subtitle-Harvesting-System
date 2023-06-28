YouTube Subtitle Harvester
==========================

This is a project for harvesting subtitles from YouTube videos based on specified search queries. The project uses Django, Celery, RabbitMQ, YouTube Data API, and YouTube Transcript API.

Getting Started
---------------

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python
* Celery
* PostgreSQL
* RabbitMQ as a message broker for Celery

### Installation

Clone the repository:

```console
git clone git@github.com:ZicsX/yt_subtitle_harvester.git
```

Change into the project directory:

```console
cd yt_subtitle_harvester
```

Install the requirements:

```console
pip install -r requirements.txt
```

Setup the PostgreSQL database:

Update the .env file with your database and celery settings. Here is an example:

```properties
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=your_port
CELERY_BROKER_URL=amqp://localhost
CELERY_RESULT_BACKEND=rpc://
```

Migrate the database:

```console
python manage.py makemigrations
python manage.py migrate
```

Run the seeder to populate initial queries:

```console
python seeder.py
```

Running the Application
-----------------------

Run the Django server:

```console
python manage.py runserver
```

In another terminal window, run the Celery worker:

```console
celery -A web_interface worker --loglevel=info --logfile=logs/celery.log --pool=solo
```

Now, you can start harvesting subtitles from the web interface.

Built With
----------

* Django - The web framework used
* Celery - Task Queue
* RabbitMQ - Message Broker
* PostgreSQL - Database
* YouTube Data API - Used to search for YouTube videos
* YouTube Transcript API - Used to download subtitles from YouTube videos
