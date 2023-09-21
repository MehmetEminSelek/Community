FROM python:3.10

# switch working directory
RUN mkdir -p /usr/src/app

# switch working directory
WORKDIR /usr/src/app

# copy the requirements file into the image
COPY requirements.txt /usr/src/app/requirements.txt

# Prerequisites installation
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

EXPOSE 80 8001

COPY . /usr/src/app

CMD ["manage.py", "runserver"]