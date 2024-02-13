FROM node:alpine

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN npm install -g @angular/cli

RUN npm install

# only necessary because of workaround until the server does not start with ng serve
RUN cp src/environments/environment.prod.ts src/environments/environment.ts

CMD ["ng", "serve", "--host", "0.0.0.0"]
