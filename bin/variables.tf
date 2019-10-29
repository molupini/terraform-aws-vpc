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
variable "link" {
  default = ""
}

#########################################################
# external
#########################################################

data "external" "bucket" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "S3", "resources", "", "${link}"]
}
data "external" "noSql" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "DYN", "resources", "", "${link}"]
}
data "external" "readUser" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "RUSR", "resources", "", "${link}"]
}
data "external" "adminUser" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "AUSR", "resources", "", "${link}"]
}
data "external" "readGroup" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "RGRP", "resources", "", "${link}"]
}
data "external" "adminGroup" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "AGRP", "resources", "", "${link}"]
}
data "external" "state" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "STATE", "resources", "", "${link}"]
}
data "external" "tagging" {
  program = ["python3", "./util/helper.py", "tagging", "${var.id}"]
}