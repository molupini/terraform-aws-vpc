##########################################################
# variables
##########################################################
variable "aws_access_key" {
}
variable "aws_secret_key" {
}
variable "aws_region" {
}
variable "vpc" {
  type = list(any)
}
variable "privateSuffix" {
  type    = string
  default = "int"
}
variable "publicSuffix" {
  type    = string
  default = "ext"
}
# TODO, PUBLIC SUBS SHOULD HANDLE WITHIN IP ADDRESS MANAGEMENT 
variable "publicSubs" {
  type    = list(string)
  default = [101, 102, 103]
}
# TODO, PRIVATE SUBS SHOULD HANDLE WITHIN IP ADDRESS MANAGEMENT 
variable "privateSubs" {
  type    = list(string)
  default = [1, 2, 3]
}
# TODO, NETWORK ADDRESS SUBS SHOULD HANDLE WITHIN IP ADDRESS MANAGEMENT 
variable "networkAddress" {
  type    = string
  default = "10.0.0.0/16"
}
variable "azs" {
  type    = list(string)
  default = ["a", "b", "c"]
}
