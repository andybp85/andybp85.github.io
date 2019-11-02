FROM node:12

RUN apt-get update && \
    apt-get install -y zsh python3 python3-pip rsync zip wget && \
    pip3 install awscli boto3 && \
    cd /root && \
    wget https://mirror.racket-lang.org/installers/7.4/racket-7.4-x86_64-linux.sh && \
    sh racket-7.4-x86_64-linux.sh --unix-style --dest /usr/local && \
    rm racket-7.4-x86_64-linux.sh &&\
    apt-get remove -y wget