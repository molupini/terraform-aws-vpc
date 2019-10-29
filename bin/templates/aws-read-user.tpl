{
    "Version": "2012-10-17",
    "Statement": [{
            "Effect": "Allow",
            "Action": [
                "s3:Get*", 
                "s3:List*"
            ],
            "Resource": [
                "${s3-bucket-arn}",
                "${s3-bucket-arn}/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:Get*",
                "dynamodb:List*"
            ],
            "Resource": [
                "${dyn-table-arn}"
            ]
        }
    ]
}