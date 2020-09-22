FROM postgres:12

RUN apt update
# install python3, pip3 and plpython3
RUN apt install -y \
    python3 \
    python3-pip \
    gcc \
    graphviz \
    graphviz-dev

# set the working directory in the container
WORKDIR /src
# copy the dependencies file to the working directory
COPY requirements.txt .
# install python dependencies
RUN pip3 install -r requirements.txt