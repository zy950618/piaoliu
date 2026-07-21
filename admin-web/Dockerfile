FROM node:22-alpine AS build
WORKDIR /workspace
ARG VITE_API_BASE_URL=/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
COPY package.json package-lock.json ./
RUN npm ci
COPY tsconfig.json vite.config.ts index.html ./
COPY src ./src
COPY admin-web ./admin-web
RUN npm run build:admin

FROM nginx:1.27-alpine
COPY --from=build /workspace/dist-admin /usr/share/nginx/html
COPY admin-web/nginx.conf /etc/nginx/conf.d/default.conf
