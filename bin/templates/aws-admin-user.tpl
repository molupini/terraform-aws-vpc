{
    "Version": "2012-10-17",
    "Statement": [
        {
        "Effect": "Allow",
        "Action": "s3:*",
        "Resource": [
            "${s3-bucket-arn}",
            "${s3-bucket-arn}/*"
        ]
    },
    {
        "Effect": "Allow",
        "Action": "dynamodb:*",
        "Resource": [
            "${dyn-table-arn}"
        ]
    }, 
    {
        "Effect": "Allow",
        "Action": [
            "codecommit:*"
        ],
        "Resource": "*"
    }
    ]
}