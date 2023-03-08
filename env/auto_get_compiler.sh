#! /bin/bash 
echo "obtain compiliers now"
cp /etc/apt/sources.list /etc/apt/sources.list.bak
echo  "deb http://dk.archive.ubuntu.com/ubuntu/ focal main universe"  >> /etc/apt/sources.list
echo  "deb http://dk.archive.ubuntu.com/ubuntu/ bionic main universe" >> /etc/apt/sources.list
echo  "deb http://dk.archive.ubuntu.com/ubuntu/ xenial main universe" >> /etc/apt/sources.list
echo  'deb http://archive.ubuntu.com/ubuntu/ trusty main universe' >> /etc/apt/sources.list
echo  'deb http://archive.ubuntu.com/ubuntu/ jammy main universe' >> /etc/apt/sources.list
apt-get update
apt-get install clang-12 clang-14 gcc-4.4 gcc-4.9 gcc-7 gcc-12 -y

# get gcc-4.1.1 binary from a repo
git clone https://github.com/linkeLi0421/gcc-4.1.1.git
ln -s /cisb_docker/CISB-dataset/gcc-4.1.1/bin/gcc-4.1 /usr/bin
ln -s /usr/lib/x86_64-linux-gnu/crt1.o .
ln -s /usr/lib/x86_64-linux-gnu/crti.o .
ln -s /usr/lib/x86_64-linux-gnu/crtn.o .