FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN apt update
RUN apt-get -y install python3-pip
RUN pip install Flask-WTF GitPython flask-cors