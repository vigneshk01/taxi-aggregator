Pre-requisite:

	# install serverless
	1.choco install serverless (or) 1. npm install -g serverless
	2.Need an IAM role with relevant permissions and trust entities(Lambda, events etc)

Steps to build the code locally & deploy in aws cloud: (uses the following aws resources - Lambda, APiGateway, s3, cloudFormation)

	# Create virtualenv
	2. python -m venv C:\Users\path\PycharmProjects\TaxiProject\venv    #modify path according to your dir

	# upgrade pip (optional)
	3. C:\Users\path\PycharmProjects\TaxiProject\venv\Scripts\python.exe -m pip install --upgrade pip

	# Activate venv
	4. .\venv\Scripts\Activate.ps1

	# install requirements in venv 
	5. pip install -r requirements.txt

	# install serveless plugins
	6. serverless plugin install -n serverless-wsgi
	7. serverless plugin install -n serverless-python-requirements
	
	# modify the IAM role under functions in serverless.yml accordingly:
	8. role: arn:aws:iam:::role/abc

	# Test in local
	9. serverless wsgi serve

	# Create a package in local
	10. serverless package

	# deloy to aws cloud
	11. serverless deploy

	# delete from aws cloud
	12. serverless remove

Additional steps when you use/import additional packages in the code:
	
	5.1 pip freeze > requirements.txt
	continue with steps 6 to 12
