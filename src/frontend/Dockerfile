FROM node:latest as build

WORKDIR /usr/src/app
 
COPY package-lock.json ./
COPY package.json ./
 
# Installs all node packages
RUN npm install

# Copies everything over to Docker environment
COPY . .

RUN npm run build

FROM nginx:alpine
COPY --from=build /usr/src/app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
