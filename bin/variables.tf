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
  default = "null"
}

#########################################################
# external
#########################################################

data "external" "bucket" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "S3", "resources", "null", "${var.link}"]
}
data "external" "noSql" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "DYN", "resources", "null", "${var.link}"]
}
data "external" "readUser" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "RUSR", "resources", "null", "${var.link}"]
}
data "external" "adminUser" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "AUSR", "resources", "null", "${var.link}"]
}
data "external" "readGroup" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "RGRP", "resources", "null", "${var.link}"]
}
data "external" "adminGroup" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "AGRP", "resources", "null", "${var.link}"]
}
data "external" "state" {
  program = ["python3", "./util/helper.py", "resources", "${var.id}", "STATE", "resources", "null", "${var.link}"]
}
data "external" "tagging" {
  program = ["python3", "./util/helper.py", "tagging", "${var.id}"]
}