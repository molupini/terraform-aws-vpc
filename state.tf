##########################################################
# data  
##########################################################
data "aws_iam_user" "run-user" {
  user_name = data.external.state.result["runAs"]
}

##########################################################
# template - polices
##########################################################
data "template_file" "s3-policy" {
  template = file("./templates/aws-s3-policy.tpl")

  vars = {
    admin-user-arn = aws_iam_user.admin-user.arn
    run-user-arn   = data.aws_iam_user.run-user.arn
    read-user-arn  = aws_iam_user.read-user.arn
    s3-bucket-name = data.external.bucket.result["logicalName"] # can't use arn as policy is applied during creation.
  }
}

data "template_file" "admin-user-policy" {
  template = file("./templates/aws-admin-user.tpl")

  vars = {
    s3-bucket-arn = aws_s3_bucket.s3_state.arn
    dyn-table-arn = aws_dynamodb_table.dyn_state.arn
  }
}

data "template_file" "read-user-policy" {
  template = file("./templates/aws-read-user.tpl")

  vars = {
    s3-bucket-arn = aws_s3_bucket.s3_state.arn
    dyn-table-arn = aws_dynamodb_table.dyn_state.arn
  }
}

##########################################################
# resources - dynamodb, s3
##########################################################
resource "aws_dynamodb_table" "dyn_state" {
  name           = data.external.noSql.result["logicalName"]
  read_capacity  = 20
  write_capacity = 20
  hash_key       = data.external.noSql.result["hashKey"]
  attribute {
    name = data.external.noSql.result["hashKey"]
    type = "S"
  }

  tags = "${data.external.tagging.result}"
}

resource "aws_s3_bucket" "s3_state" {
  bucket        = data.external.bucket.result["logicalName"]
  acl           = "private"
  force_destroy = true
  versioning {
    enabled = true
  }
  policy = data.template_file.s3-policy.rendered

  tags = "${data.external.tagging.result}"
}

##########################################################
# resources - groups, users
##########################################################
resource "aws_iam_group" "admin-group" {
  name = data.external.adminGroup.result["logicalName"]
}

resource "aws_iam_group" "read-group" {
  name = data.external.readGroup.result["logicalName"]
}

resource "aws_iam_user" "admin-user" {
  name = data.external.adminUser.result["logicalName"]
}

resource "aws_iam_user" "read-user" {
  name = data.external.readUser.result["logicalName"]
}

resource "aws_iam_access_key" "admin-user" {
  user = aws_iam_user.admin-user.name
}

resource "aws_iam_access_key" "read-user" {
  user = aws_iam_user.read-user.name
}

resource "aws_iam_group_membership" "admin-user" {
  name = "add-${aws_iam_group.admin-group.name}"
  users = [
    aws_iam_user.admin-user.name,
    data.aws_iam_user.run-user.user_name,
  ]
  group = aws_iam_group.admin-group.name
}

resource "aws_iam_group_membership" "read-user" {
  name = "add-${aws_iam_group.read-group.name}"
  users = [
    aws_iam_user.read-user.name,
  ]
  group = aws_iam_group.read-group.name
}

resource "aws_iam_group_policy" "admin-group" {
  name   = "pol-${aws_iam_group.admin-group.name}"
  group  = aws_iam_group.admin-group.name
  policy = data.template_file.admin-user-policy.rendered
}

resource "aws_iam_group_policy" "read-group" {
  name   = "pol-${aws_iam_group.read-group.name}"
  group  = aws_iam_group.read-group.name
  policy = data.template_file.read-user-policy.rendered
}