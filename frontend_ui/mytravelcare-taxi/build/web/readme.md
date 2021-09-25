# MyTravelCare/taxi WebApp Deployment

1. check if Dockerfile is correctly edited
2. login to aws using following command - > 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws-id>.dkr.ecr.us-east-1.amazonaws.com'
3. build image in local linux - > 'docker build -t travelcare-taxi-ui .'
4. add tag 'latest' to the image - > 'docker tag travelcare-taxi-ui:latest <aws-id>.dkr.ecr.us-east-1.amazonaws.com/travelcare-taxi-ui:latest'
5. push image to ECR - > 'docker push <aws-id>.dkr.ecr.us-east-1.amazonaws.com/travelcare-taxi-ui:latest'
6. create container service using ECS fargate with application load balancer for 'travelcare-taxi-ui:latest' image
7. use the application load balancer dns url to access to front-end UI over the internet
    
