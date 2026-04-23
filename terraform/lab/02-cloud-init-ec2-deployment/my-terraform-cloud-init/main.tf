module "networking" {
  source = "./modules/vpc"
  vpc_cidr = var.vpc_cidr
  subnet_cidr = var.subnet_cidr
  availability_zone = var.availability_zone
  environment = var.environment
}

module "compute" {
    source = "./modules/ec2"
    environment = var.environment
    instance_type = var.instance_type
    vpc_id = module.networking.vpc_id
    subnet_id = module.networking.subnet_id
    user_data = file("${path.root}/cloud-init.yaml")
}