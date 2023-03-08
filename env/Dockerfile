FROM ubuntu:20.04
# Fix timezone issue
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -y update && apt-get -y install build-essential \
	bison \
	zlib1g-dev \
	libtool \
	cmake \
	vim \
	gcc-multilib \
	g++-multilib \
	libc6-dev-i386 \
	autoconf \
	automake \
	curl \
	wget \
	git \
	make \
	unzip

RUN mkdir /cisb_docker
WORKDIR /cisb_docker
RUN git clone https://github.com/H0w1/CISB-dataset.git
WORKDIR CISB-dataset
RUN bash ./env/auto_get_compiler.sh
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
