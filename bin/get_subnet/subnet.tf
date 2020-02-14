#########################################################
# resources
#########################################################
data "aws_vpc" "vpc" {
  id = "${var.vpcId}"
}

data "aws_subnet_ids" "subnet" {
  vpc_id = "${data.aws_vpc.vpc.id}"
}

data "aws_subnet" "subnet" {
  #   for_each attribute for creating multiple resources based on a map #17179
  #   for_each = data.aws_subnet_ids.subnet.ids
  #   id       = each.value
  count = "${length(tolist(data.aws_subnet_ids.subnet.ids))}"
  id    = "${element(tolist(data.aws_subnet_ids.subnet.ids), count.index)}"
}

