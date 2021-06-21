FROM nginx as production-stage
RUN mkdir /app
COPY ./front /app
RUN rm /etc/nginx/conf.d/default.conf
COPY ./deploy/frontend/front.conf /etc/nginx/conf.d/front.conf
CMD ["nginx", "-g", "daemon off;"]