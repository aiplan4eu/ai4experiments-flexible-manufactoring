# Stage 1 - BUILD
FROM node:20 AS build
WORKDIR fm-frontend
COPY frontend .

ENV NG_CLI_ANALYTICS=ci
RUN npm install
RUN npm run build --prod

# Stage 2 - DEPLOY

FROM nginx:latest as ngi
COPY --from=build /fm-frontend/dist/gui /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80


#FROM ubuntu:23.10
#
#WORKDIR /up-service
#COPY . /up-service
#
##RUN ln -s /up-service/backend/src /up-service/src/backend
##
##RUN cp /up-service/backend/src/* /up-service/src
#
#RUN apt update  \
#    && apt install -y python3-full  pipx\
#    && apt install -y nginx  \
#    && apt install -y nodejs npm
#
#RUN pipx ensurepath
### Preparing the front end with Angular
#
#RUN npm install -g @angular/cli
#
#RUN cd frontend && ng build --configuration production && cp -r dist/gui /usr/share/nginx/html && cd ..
#
#COPY nginx.conf /etc/nginx/nginx.conf
#
#EXPOSE 80
#
### Preparing the backend with poetry
#
#RUN pipx install poetry
#
#RUN cd backend && /root/.local/bin/poetry install
#
### starting the service with poetry
#RUN chmod 755 ./start.sh
#CMD ["./start.sh"]