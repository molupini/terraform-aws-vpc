#########################################################
# modules
#########################################################
# TODO NEED TO PARAM SETTINGS BELOW SEE, https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/2.15.0
# TODO NEED TO INTERGRATE IPAM, ISSUE WITH CIDR AND SUB RANGE, https://www.hashicorp.com/blog/hashicorp-terraform-0-12-preview-for-and-for-each see first example
# SEE, https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/2.15.0

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "${data.external.vpc.result["logicalName"]}"

  # TODO MAKE BELOW API PARAM
  cidr = "${var.networkAddress}"

  # EXAMPLE
  # azs             = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  azs = [
    for az in var.azs :
    # concat(data.external.vpc.result["region"], a)
    "${data.external.vpc.result["region"]}${az}"

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
  tags = "${
    merge("${data.external.tagging.result}",
      map(
        "resourceId", "${data.external.vpc.result["resourceId"]}"
      )
  )}"

}

module "get_subnet" {
  source = "../../get/subnet"

  aws_access_key = var.aws_access_key
  aws_secret_key = var.aws_secret_key
  aws_region     = var.aws_region
  vpcId          = module.vpc.vpc_id
  perimeter      = "default"
  id             = var.id
}
