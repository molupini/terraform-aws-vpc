{
    "Version": "2012-10-17",
    "Statement": [
        {
        "Effect": "Allow",
        "Principal": {
            "AWS": [
                "${admin-user-arn}", 
                "${run-user-arn}"
            ]
        },
        "Action": "s3:*",
        "Resource": [
            "arn:aws:s3:::${s3-bucket-name}",
            "arn:aws:s3:::${s3-bucket-name}/*"
        ]
    },
    {
        "Effect": "Allow",
        "Principal": {
            "AWS": [
                "${read-user-arn}"
            ]
        },
        "Action": [
                "s3:Get*", 
                "s3:List*"
            ],
        "Resource": [
            "arn:aws:s3:::${s3-bucket-name}",
            "arn:aws:s3:::${s3-bucket-name}/*"
        ]
    }
]
}