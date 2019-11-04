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

output "logicalId" {
  value = "${module.vpc.vpc_id}"
}

output "vpc_resourceId" {
  value = "${data.external.vpc.result["resourceId"]}"
}

output "done" {
  value = 0
  depends_on = [
    module.vpc
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