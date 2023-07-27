#Deriving the latest base image
FROM python:latest

WORKDIR /app

# Folder and files that are in the dockerignore are not copied
COPY . .
RUN pip3 install -r requirements.txt

#CMD instruction should be used to run the software
CMD [ "python", "./main.py"]

# docker build .
# docker run --env-file ./.env.docker IMAGE