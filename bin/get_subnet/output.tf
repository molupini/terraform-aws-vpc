
##########################################################
# output 
##########################################################
output "aws_vpc_vpc" {
  value = "${data.aws_vpc.vpc}"
}
output "aws_subnet_subnet_id" {
  value = "${data.aws_subnet.subnet.*.id}"
}
output "aws_subnet_subnet_cidr_block" {
  value = "${data.aws_subnet.subnet.*.cidr_block}"
}
output "aws_subnet_tags" {
  value = "${data.aws_subnet.subnet.*.tags}"
}
