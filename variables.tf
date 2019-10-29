##########################################################
# Create remote state configuration 
##########################################################


##########################################################
# variables
##########################################################

variable "aws_access_key" {
}
variable "aws_secret_key" {
}
variable "aws_region" {
}
variable "id" {
}

# variable "resources" {
# }

# variable "tagging" {
# }

#########################################################
# external
#########################################################

data "external" "bucket" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "S3"]
}
data "external" "noSql" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "DYN"]
}
data "external" "readUser" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "RUSR"]
}
data "external" "adminUser" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "AUSR"]
}
data "external" "readGroup" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "RGRP"]
}
data "external" "adminGroup" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "AGRP"]
}
data "external" "state" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "STATE"]
}
data "external" "tagging" {
  program = ["python3", "./util/helper.py", "tagging", "${var.id}"]
}