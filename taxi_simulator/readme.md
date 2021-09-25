# Taxi simulator

Taxi simulator will generate initial taxi location and move taxi at every minute.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install python library which used in simulator.

```bash
pip install boto3 numpy schedule requests Shapely
```

## Run Taxi simulator 

```python
python main.py
```

## Note
> - use python > 3 version in order to run the simulator
> - Please Add URL in code after you setup **backend_lambda** (You will find that in root of this repository) in aws. 

## Setup process for AWS infrastructure

- In cloudFormation template you will find CF Template. You can use that to spin up infrastructure for taxi simulator in AWS.(Please add valid parameters in CF template and also Create valid Roles EC2 instance before spinning up CF template)
- Pre-requisite for CF template is S3 bucket where EC2 code zip and KinesisLambda Zip require. Please add this before creating infrastructure for taxi simulator.
- You will find KinesisLambda code in **'Kinesis_Lambda_Insert_Stream_code'** folder.
- One Option is You will find **'KinesisLambda.zip'** in folder just upload that in S3 bucket to avoid second option.
- Second option is create Deployment package and put that in zip then upload to S3 bucket or you can just ZIP **'Kinesis_Lambda_Insert_Stream_code'** folder content and add that in S3 bucket both ways will work.
- For EC2 zip just exclude **CloudFormationTemplate and 'Kinesis_Lambda_Insert_Stream_code'** folder for the root folder and make zip for remaining folder and upload that to S3 so you can download that from S3 after EC2 instance started.
