# Dockerfile for assignment1-app
# Platform: Docker running on 64bit Amazon Linux 2023 (Elastic Beanstalk)
#
# Serves the sample application over Nginx. Elastic Beanstalk builds this
# image and runs it behind an Application Load Balancer, listening on
# port 80, across a Min 1 / Max 2 Auto Scaling group in the public subnets.

FROM nginx:alpine

# Remove the default nginx welcome page and copy in the app's static content
RUN rm -rf /usr/share/nginx/html/*
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
