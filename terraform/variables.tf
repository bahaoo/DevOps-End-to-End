variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "key_name" {
  type        = string
  description = "Existing AWS EC2 key pair name."
}

variable "ssh_cidr_blocks" {
  type        = list(string)
  description = "CIDR blocks allowed to SSH. Restrict this to your public IP."
  default     = []
}

variable "container_image" {
  type    = string
  default = "ghcr.io/your-github-user/devops-demo:latest"
}