##########################################################
# output 
##########################################################

# VERFICATION / STD OUT FOR API UPDATE
# SERVICE WILL REQUIRE APPLICATION, RESOURCE TYPE, DEPLOYMENT ID, LOGICAL ID
output "application" {
  value = "${data.external.tagging.result["application"]}"
}

output "resourceType" {
  value = "${data.external.tagging.result["resourceType"]}"
}

output "deploymentId" {
  value = "${data.external.tagging.result["deploymentId"]}"
}

# SEE BELOW OUTPUT
# output "logicalId" {
#   value = "${module.vpc.vpc_id}"
# }
# output "vpc_resourceId" {
#   value = "${data.external.vpc.result["resourceId"]}"
# }

# USED WHEN SEEDING API 
output "aws_vpc_id" {
  value = map("${data.external.vpc.result["resourceId"]}", "${module.vpc.vpc_id}")
  depends_on = [
    module.get_subnet
  ]
}

output "done" {
  value = 0
  depends_on = [
    module.vpc
  ]
}

# RESOURCE SPECFIC 

# VPC
# output "module_vpc" {
#   value = "${module.vpc}"
# }

