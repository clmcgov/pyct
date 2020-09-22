FROM debian:buster

RUN apt update
# prepare for mono install
RUN apt install -y \
    apt-transport-https \
    dirmngr \
    gnupg \
    ca-certificates
# add mono repo
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
RUN echo "deb https://download.mono-project.com/repo/debian stable-buster main" | tee /etc/apt/sources.list.d/mono-official-stable.list
RUN apt update
# install desired packages
RUN apt install -y \
    mono-devel \
    python3 \
    python3-pip \
    # for pycparser
    clang \
    texlive-full \
    # for psycopg binary
    gcc
WORKDIR /src
# copy the dependencies file to the working directory
COPY requirements.txt .
# install first, or pythonnet won't find
RUN pip3 install pycparser 
# install python dependencies
RUN pip3 install -r requirements.txt