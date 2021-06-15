FROM debian:buster-slim

ENV USER mpirun

ENV DEBIAN_FRONTEND=noninteractive \
    HOME=/home/${USER} 

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends sudo apt-utils && \
    apt-get install -y --no-install-recommends openssh-server \
        python3-dev python3-pip python3-virtualenv \
        build-essential libopenmpi-dev openmpi-bin openmpi-common openmpi-doc binutils \
        python3-msgpack python3-yaml python3-mpi4py && \
    apt-get clean && apt-get purge && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /var/run/sshd
RUN echo 'root:${USER}' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN adduser --disabled-password --gecos "" ${USER} && \
    echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

ENV SSHDIR ${HOME}/.ssh/

RUN mkdir -p ${SSHDIR}

ADD mpi/ssh/config ${SSHDIR}/config
ADD mpi/ssh/id_rsa.mpi ${SSHDIR}/id_rsa
ADD mpi/ssh/id_rsa.mpi.pub ${SSHDIR}/id_rsa.pub
ADD mpi/ssh/id_rsa.mpi.pub ${SSHDIR}/authorized_keys

RUN chmod -R 600 ${SSHDIR}* && \
    chown -R ${USER}:${USER} ${SSHDIR}

RUN pip3 install --upgrade pip

#USER ${USER}
#RUN pip3 install -U setuptools \
#    && pip3 install mpi4py \
#    && pip3 install pyyaml \
#   && pip3 install msgpack

#USER root

RUN rm -fr ${HOME}/.openmpi && mkdir -p ${HOME}/.openmpi
ADD mpi/default-mca-params.conf ${HOME}/.openmpi/mca-params.conf
RUN chown -R ${USER}:${USER} ${HOME}/.openmpi

ENV TRIGGER 1

ENV BUILDER_DIR ${HOME}/work
ENV BUILDER_HTTP_PORT 8080

ADD src ${HOME}/builder
RUN mkdir -p ${BUILDER_DIR} && chown -R ${USER}:${USER} ${BUILDER_DIR}

#USER ${USER}

EXPOSE 22
EXPOSE ${BUILDER_HTTP_PORT}
CMD ["/usr/sbin/sshd", "-D"]
