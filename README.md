# YouEtix|Community

This is a community system built using Python's Django framework and MySQL database. The system allows to insert community members, reward point assignment, checking user community countries & friends

## Installation

To install the project, first clone the repository:

```
   $ git clone https://github.com/YouEtixDev/Community.git
```

Then, create a virtual environment and activate it :

```
   $ cd Registration
   $ python -m venv .venv
```

To activate environment for _Windows_:

```
   $ cd .venv/Scripts
   $ .\activate
```

To activate environment for _Linux & Mac_:

```
   $ source venv/bin/activate
```

Install the project dependencies using pip:

```
   $ python -m pip install --upgrade pip
   $ pip install -r requirements.txt
```

Finally, run the database migrations and start the Django development server:

```
   $ python manage.py migrate
   $ python manage.py runserver
```

The application will be available at http://localhost:8001.

## Running the application with Docker

To run the application with Docker, first make sure you have Docker and Docker Compose installed on your machine. Then, navigate to the project directory and run the following command:

```
   $ docker-compose up -d
```

For downgrading container,

```
   $ docker-compose down
```

This will build the Docker image for the application and start the services defined in the docker-compose.yml file. The application will be available at http://localhost:8001.

## Accessing Swagger UI

To access the Swagger UI documentation, follow these steps:

1. Make sure the application is running locally or deployed to a server.
2. Open a web browser and enter the URL to your API, e.g., `http://localhost:8001`.
3. Append `/swagger/` to the base URL, e.g., `http://localhost:8001/swagger/`.
4. The Swagger UI interface will open in the browser, displaying a list of available endpoints.

### Exploring Endpoints

Once you have accessed the Swagger UI interface, you can browse through the available endpoints and their corresponding operations. Each endpoint is listed with its HTTP method (GET, POST, etc.) and a brief description.

Clicking on an endpoint will expand it, providing more details such as request and response schemas, parameters, and example data. You can explore the different sections and interact with the endpoint by filling in parameters and executing requests directly from the Swagger UI.

### Testing Endpoints

Swagger UI allows you to test your API endpoints directly from the interface. You can input parameter values, specify request bodies, and execute requests to see the responses. This provides a convenient way to validate your API behavior and troubleshoot any issues.

Please note that Swagger UI is primarily intended for development and testing purposes. It's recommended to secure your production APIs appropriately and follow best practices for API documentation and user access.
