steps to setup the code locally & in aws cloud: (uses the following aws services - Lambda, APiGateway, s3, cloudFormation)

# Create virtualenv
1 python -m venv C:\Users\path\PycharmProjects\Project\venv

# upgrade pip (optional)
2 C:\Users\path\PycharmProjects\Project\venv\Scripts\python.exe -m pip install --upgrade pip

# Activate venv
3 .\venv\Scripts\Activate.ps1

# create requirement.txt (optional)
4 pip freeze | Out-File -Encoding UTF8 requirements.txt

# install serveless plugins
5 serverless plugin install -n serverless-wsgi
6 serverless plugin install -n serverless-python-requirements

# Test in local
7 serverless wsgi serve

# Create a package in local
8 serverless package

# deloy to aws cloud
9 serverless deploy

# delete from aws cloud
10 serverless remove