##########################################################
# output 
##########################################################

# VERFICATION / STD OUT FOR API UPDATE
# SERVICE WILL REQUIRE APPLICATION, RESOURCE TYPE, DEPLOYMENT ID, LOGICAL ID
output "application" {
  value = "${data.external.tagging.result["application"]}"
  depends_on = [
    module.get_subnet
  ]
}
output "resourceType" {
  value = "${data.external.tagging.result["resourceType"]}"
  depends_on = [
    module.get_subnet
  ]
}
output "deploymentId" {
  value = "${data.external.tagging.result["deploymentId"]}"
  depends_on = [
    module.get_subnet
  ]
}
output "logicalId" {
  value = "${module.get_subnet.aws_vpc_vpc.id}"
  depends_on = [
    module.get_subnet
  ]
}
output "done" {
  value = 0
  depends_on = [
    module.get_subnet
  ]
}

# RESOURCE SPECFIC 

# VPC

# TESTING VPC OUTPUT
# output "module_vpc" {
#   value = "${module.vpc}"
#   depends_on = [
#     module.vpc
#   ]
# }

# output "module_vpc" {
#   value = [
#     map("name", "${module.vpc.name}"),
#     map("vpc_id", "${module.vpc.vpc_id}"),
#     map("vpc_cidr_block", "${module.vpc.vpc_cidr_block}")
#   ]
#   depends_on = [
#     module.vpc
#   ]
# }
# output "module_vpc" {
#   value = [
#     map("name", "${module.vpc.name}"),
#     map("vpc_enable_dns_hostnames", "${module.vpc.vpc_enable_dns_hostnames}"),
#     map("vpc_enable_dns_support", "${module.vpc.vpc_enable_dns_support}"),
#     map("vpc_id", "${module.vpc.vpc_id}"),
#     map("vpc_instance_tenancy", "${module.vpc.vpc_instance_tenancy}"),
#     map("vpc_main_route_table_id", "${module.vpc.vpc_main_route_table_id}"),
#     map("vpc_cidr_block", "${module.vpc.vpc_cidr_block}")
#   ]
#   depends_on = [
#     module.vpc
#   ]
# }
# output "module_vpc_default" {
#   value = [
#     map("default_network_acl_id", "${module.vpc.default_network_acl_id}"),
#     map("default_route_table_id", "${module.vpc.default_route_table_id}")
#   ]
#   depends_on = [
#     module.vpc
#   ]
# }
# output "module_vpc_nat" {
#   value = [
#     map("nat_ids", "${module.vpc.nat_ids}"),
#     map("nat_public_ips", "${module.vpc.nat_public_ips}")
#   ]
#   depends_on = [
#     module.vpc
#   ]
# }
# output "module_vpc_private" {
#   value = [
#     map("private_route_table_ids", "${module.vpc.private_route_table_ids}"),
#     # names, see module output below 
#   ]
#   depends_on = [
#     module.vpc
#   ]
# }

# output "module_vpc_public" {
#   value = [
#     map("public_route_table_ids", "${module.vpc.public_route_table_ids}"),
#   ]
#   depends_on = [
#     module.vpc
#   ]
# }

# TESTING GET_SUBNET OUTPUT
# output "aws_subnet" {
#   value = "${module.get_subnet}"
#   depends_on = [
#     module.get_subnet
#   ]
# }

# VPC & POST CREATE GET_SUBNET 
# ADDED RESOURCES NEEDS TO BE PARSED IN A STD OUT FOR THE API
# SEED FLAG USERDEFINED FASLE IN THE MODEL 

output "vpc_resourceId" {
  value = "${data.external.vpc.result["resourceId"]}"
  depends_on = [
    # aws_instance.ec2
  ]
}

# output "aws_vpc_id" {
#   value = "${zipmap(module.vpc.tags.resourceId, module.vpc.id)}"
#   depends_on = [
#     # module.vpc
#   ]
# }

output "aws_vpc_id" {
  value = map(module.get_subnet.aws_vpc_vpc.tags.resourceId, module.get_subnet.aws_vpc_vpc.id)
  depends_on = [
    module.get_subnet
  ]
}

output "aws_subnet_id" {
  value = "${zipmap(module.get_subnet.aws_subnet_tags.*.Name, module.get_subnet.aws_subnet_subnet_id)}"
  depends_on = [
    module.get_subnet
  ]
}

output "aws_subnet_cidr" {
  value = "${zipmap(module.get_subnet.aws_subnet_tags.*.Name, module.get_subnet.aws_subnet_subnet_cidr_block)}"
  depends_on = [
    module.get_subnet
  ]
}
