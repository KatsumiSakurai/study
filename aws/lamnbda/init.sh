aws lambda create-function --region ap-northeast-1 \
    --function-name sakurai-get-data \
    --zip-file fileb://lambda_get_data.zip \
    --role arn:aws:iam::391518890631:role/service-role/sakurai-regist-data-role-wbkyqyth \
    --handler lambda_function.lambda_handler \
    --runtime python3.8 \
    --vpc-config SubnetIds=subnet-0c269e44,subnet-3b739961,subnet-96c84abd,SecurityGroupIds=sg-9816e4dd \
    --layers arn:aws:lambda:ap-northeast-1:770693421928:layer:Klayers-python38-aws-psycopg2:1

aws lambda create-function --region ap-northeast-1 \
    --function-name sakurai-get-detail \
    --zip-file fileb://lambda_get_detail.zip \
    --role arn:aws:iam::391518890631:role/service-role/sakurai-regist-data-role-wbkyqyth \
    --handler lambda_function.lambda_handler \
    --runtime python3.8 \
    --vpc-config SubnetIds=subnet-0c269e44,subnet-3b739961,subnet-96c84abd,SecurityGroupIds=sg-9816e4dd \
    --layers arn:aws:lambda:ap-northeast-1:770693421928:layer:Klayers-python38-aws-psycopg2:1
