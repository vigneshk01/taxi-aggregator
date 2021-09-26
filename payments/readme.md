# Payments

This application will let you interact with PayU payment portal to completed the transaction for availing TravelCare facilites

## Installation

```bash
pip install Flask
```
## Running application in local

```bash
python3 api.py
```
# Running application in EC2

##  Install the apache webserver and mod_wsgi on EC2 instance

```bash
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
```
Please refer [link](https://github.com/vigneshk01/taxi-aggregator/blob/final/screenshots/PaymentScreens_screenshots.docx) for further setup

### Url to access via EC2
'your EC2 endpoint/?cost=costamount'
Example:
http://ec2-3-142-40-237.us-east-2.compute.amazonaws.com/?cost=34.58

## Note
- Use your own merchantKey and merchant salt
- surl & furl in api.py has to be replaced as where you are planning run the application
- In payment/model-->status.html at Line 41 you repective url has to be updated depending on where you want to run the app
