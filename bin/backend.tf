#########################################################
# resource
#########################################################
terraform {
  backend "s3" {
    key    = "automation.state"
    bucket = "s3-myloft-sbx-000002"
    dynamodb_table = "dyn-myloft-sbx-000002"
    # region = "eu-west-1"
    # encrypt = "true"
  }
}
