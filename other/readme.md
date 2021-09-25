This script deploys some of the lambda functions and its dependencies as provided under backend_lambda dir. also this will be the standard deployment for all the lambda function
Place the required lambda functions inside the dir and place the serverless.yml at the root dir and modify the function paramaeters accordingly, additionally make sure aws session credentials are not espired prior to deployment.

Pre-requisite:

	# install serverless
	1.choco install serverless (or) 1. npm install -g serverless
	2.Need an IAM role with relevant permissions and trust entities(Lambda, events etc)

Steps to build the code locally & deploy in aws cloud: (uses the following aws resources - Lambda, APiGateway, s3, cloudFormation)
	
	# modify the IAM role under functions in serverless.yml accordingly:
	3. role: arn:aws:iam:::role/abc

	# Test in local
	4. serverless wsgi serve

	# Create a package in local
	5. serverless package

	# deloy to aws cloud
	6. serverless deploy

	# delete from aws cloud
	7. serverless remove
