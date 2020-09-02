FROM debian:buster-slim

RUN apt update

# mono, python
RUN apt install -y apt-transport-https dirmngr gnupg ca-certificates
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
RUN echo "deb https://download.mono-project.com/repo/debian stable-buster main" | tee /etc/apt/sources.list.d/mono-official-stable.list
RUN apt update
RUN apt install -y mono-devel python3 python3-pip clang git
# have to separate, or pythonnet won't find pycparser
RUN pip3 install pycparser
RUN pip3 install pythonnet ipython

# set the working directory in the container
WORKDIR /code
