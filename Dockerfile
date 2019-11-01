FROM mhart/alpine-node:12.13.0

#ENV NODE_VERSION 12.13.0

#RUN ["apk", "update"]
#RUN ["apk", "add", "--no-cache", "nodejs", "nodejs-npm", "python3", "zsh"]
RUN apk update && apk add --no-cache python3 zsh

#FROM node:12
#RUN ["apt-get", "update"]
#RUN ["apt-get", "install", "-y", "zsh", "python3"]

#ENV PATH="/opt/gtk/bin:${PATH}"
# WORKDIR /usr/src/app
# COPY package*json ./
# COPY rollup*config*js ./
# RUN npm install
# EXPOSE 3000
#RUN npm install -g svelte sapper
