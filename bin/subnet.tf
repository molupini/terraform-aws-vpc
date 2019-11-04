#########################################################
# resources
#########################################################
data "aws_vpc" "vpc" {
  id = "${module.vpc.vpc_id}"
  depends_on = module.vpc
}

data "aws_subnet_ids" "subnet" {
  vpc_id = "${data.aws_vpc.vpc.id}"
  # filter {
  #   name = "tag:Name"
  #   values = [
  #     # var.perimeter != "private" || var.perimeter != "public"
  #     # "${var.perimeter == "default" ? "*" : "*-${lower(data.external.perimeter.result[var.perimeter])}-*"}",
  #     # "${var.perimeter == "default" ? "*" : "*-${upper(data.external.perimeter.result[var.perimeter])}-*"}"
  #     # "${var.perimeter == "default" ? data.external.perimeter.result[var.perimeter] : "*-${lower(data.external.perimeter.result[var.perimeter])}-*"}",
  #     # "${var.perimeter == "default" ? data.external.perimeter.result[var.perimeter] : "*-${upper(data.external.perimeter.result[var.perimeter])}-*"}"
  #     "*"
  #   ]
  # }
}

data "aws_subnet" "subnet" {
  #   for_each attribute for creating multiple resources based on a map #17179
  #   for_each = data.aws_subnet_ids.subnet.ids
  #   id       = each.value
  count = "${length(tolist(data.aws_subnet_ids.subnet.ids))}"
  id    = "${tolist(data.aws_subnet_ids.subnet.ids)[count.index]}"
}

