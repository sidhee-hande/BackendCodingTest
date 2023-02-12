# base image  
FROM python:3.8   

# where your code lives  
WORKDIR  /application

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# Copy the dependencies
COPY requirements.txt /application/

# Copy the files
COPY . .

# install dependencies  
RUN pip install --upgrade pip  


# run this command to install all dependencies  
RUN pip install -r requirements.txt  

# port where the Django app runs  
EXPOSE 8000

# Executable commands
CMD python manage.py runserver 0.0.0.0:8000

