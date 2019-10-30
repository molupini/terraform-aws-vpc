#########################################################
# resource
#########################################################
terraform {
  backend "s3" {
    key    = "automation.state"
    # region = "eu-west-1"
    # encrypt = "true"
  }
}
