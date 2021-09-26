# User simulator

User simulator will enable Passenger Sign Up/sign In,Taxi Booking and Feedback.

##Instance creation
Create 5 EC instances in cloudformation with User_Simulator.json template
add all 5 EC2's to same autoscaling group(set 5 max capacity)

## Upload
Upload UserSimulator.zip file to an s3 bucket

## Download
Download the UserSimulator.zip file from S3 bucket and unzip file.
cd capstone


## Installation

Use the package manager pip to install python library used by simulator.


sudo pip3 install -r requirements.txt


## Run User simulator 

```python3
python3 main.py
```


## Note
1.use python > 3 version in order to run the simulator

2.To Simulate Rush hour- SSH to EC2 instance from 5 different AWS CLI and invoke main.py and login with 5 different users and book a taxi from 5 diferent locations(different Origin)

3.To Simulate Special events- SSH to EC2 instance from 5 different AWS and invoke main.py and login with 5 different users and book a taxi from same location(same Origin eg: Kanteerava Stadium, bengaluru)

4. if google API's doesnt work please try changing the API key
5. Once backend Lambda is loaded, please make a note of the URL found in the root directory and replace base_url in user_simulator.py




Note: This taxi aggregator works only for Bangalore city





