#########################################################
# modules
#########################################################
# TODO NEED TO PARAM SETTINGS BELOW SEE, https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/2.15.0
# TODO NEED TO INTERGRATE IPAM, ISSUE WITH CIDR AND SUB RANGE, https://www.hashicorp.com/blog/hashicorp-terraform-0-12-preview-for-and-for-each see first example
# SEE, https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/2.15.0

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = var.vpc[0]["Name"]

  # TODO MAKE BELOW API PARAM
  cidr = var.networkAddress

  # EXAMPLE
  # azs             = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  azs = [
    for az in var.azs :
    "${var.aws_region}${az}"

  ]

  # EXAMPLE
  # private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnet_suffix = var.privateSuffix
  private_subnets = [
    for privateSub in var.privateSubs :
    # concat(data.external.vpc.result["region"], a)
    # "${data.external.vpc.result["region"]}${a}"
    cidrsubnet(var.networkAddress, 8, privateSub)

  ]

  # EXAMPLE
  # public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  public_subnet_suffix = var.publicSuffix
  public_subnets = [
    for publicSub in var.publicSubs :
    # concat(data.external.vpc.result["region"], a)
    # "${data.external.vpc.result["region"]}${a}"
    cidrsubnet(var.networkAddress, 8, publicSub)
  ]

  # TODO MAKE BELOW API PARAM
  enable_nat_gateway     = true
  single_nat_gateway     = true
  one_nat_gateway_per_az = false

  # ROUTE TABLE PROPAGATION
  # TODO MAKE BELOW API PARAM
  # propagate_private_route_tables_vgw = true
  # propagate_public_route_tables_vgw  = true

  # TODO MAKE BELOW API PARAM
  # enable_vpn_gateway = true

  # TAGGING 
  tags = var.vpc[0]
}

# IF NECESSARY, UNTESTED 
# module "get_subnet" {
#   source = "./get_subnet"
#   vpcId          = module.vpc.vpc_id
# }
