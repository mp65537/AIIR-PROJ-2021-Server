FROM python
RUN apt-get update
RUN apt-get -y install gcc python-mpi4py