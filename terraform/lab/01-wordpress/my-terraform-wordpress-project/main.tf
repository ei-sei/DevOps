resource "aws_security_group" "sg" {
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "wordpress-sg"
    Environment = var.environment
  }
}

resource "aws_instance" "my_ec2" {
  ami                         = "ami-052c9005e24cd7236"
  instance_type               = var.instance_type
  vpc_security_group_ids      = [aws_security_group.sg.id]
  user_data                   = file("${path.module}/user_data.sh")
  associate_public_ip_address = true

  tags = {
    Name        = "wordpress-ec2"
    Environment = var.environment
  }
}