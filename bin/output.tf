##########################################################
# output 
##########################################################

# USED WHEN SEEDING API 
output "aws_vpc_id" {
  value = map("${var.vpc[0]["resourceId"]}", "${module.vpc.vpc_id}")
  depends_on = [
    module.get_subnet
  ]
}

