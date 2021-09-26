# MyTravelCare/taxi Backend APIs

### File structure
1. api-calls-lambda-files - > contains the lambda index.js files in respective folders corresponding to their api paths.
2. environment_variables.txt - > contains the lambda-> Configuration-> Environment Variables used for each lambda. The fields vary as per the usage.
3. glcapstone-taxi-api-dev-**.json/**.yaml - > contains the various alternative for API Gateway documents. 
It contains the information about api paths and the response and request models for each call

### Usage:
1. Create API Gateway Resource and Stage using the document.
2. Create lambdas using the api-calls-lambda index.js files in AWS
3. Connect the API path to lambdas via lambda proxy integration
4. 'Test' each path call in AWS API Gateway UI by providing the 'Request' and checking the 'Response'
5. Deploy API to Stage as 'prod' or 'dev' or 'test'
6. Get the link to be used at front end to make the calls
