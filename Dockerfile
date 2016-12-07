FROM ubuntu:16.04
MAINTAINER Jonathan B Coe <jbcoe@me.com>

RUN apt-get -y update && apt-get install -y python-software-properties software-properties-common
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test
RUN apt-get -y update && apt-get install -y python-pip git cmake ninja-build ruby pypy python3 clang libclang-3.8-dev libc++1 libc++-dev ruby-dev

RUN pip install django clang jupyter notebook asciitree
RUN gem install ffi

RUN apt-get autoremove -y
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN useradd c-api-user && mkdir -p /home/c-api-user && chown c-api-user /home/c-api-user
ENV HOME /home/c-api-user
ENV LD_LIBRARY_PATH /usr/lib/llvm-3.8/lib:$LD_LIBRARY_PATH

USER c-api-user
RUN git clone --recurse-submodules https://github.com/jbcoe/C_API_generation /home/c-api-user/demo

EXPOSE 8888
WORKDIR /home/c-api-user/demo/demos
VOLUME /home/c-api-user/demo/demos
COPY docker/run-server.sh .
CMD ["./run-server.sh"]

