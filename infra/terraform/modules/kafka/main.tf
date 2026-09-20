variable "project_name" { type = string }
variable "environment" { type = string }
variable "vpc_id" { type = string }
variable "private_subnet_ids" { type = list(string) }
variable "broker_nodes" { type = number }

resource "aws_security_group" "msk" {
  name        = "${var.project_name}-${var.environment}-msk"
  description = "MSK brokers for LogiStream sensors"
  vpc_id      = var.vpc_id

  ingress {
    description = "Kafka TLS inside VPC"
    from_port   = 9094
    to_port     = 9094
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_msk_configuration" "this" {
  name              = "${var.project_name}-${var.environment}"
  kafka_versions    = ["3.6.0"]
  server_properties = <<-PROPS
    auto.create.topics.enable=false
    log.retention.hours=48
    num.partitions=6
  PROPS
}

resource "aws_msk_cluster" "this" {
  cluster_name           = "${var.project_name}-${var.environment}-sensors"
  kafka_version          = "3.6.0"
  number_of_broker_nodes = var.broker_nodes

  broker_node_group_info {
    instance_type   = "kafka.t3.small"
    client_subnets  = var.private_subnet_ids
    security_groups = [aws_security_group.msk.id]
    storage_info {
      ebs_storage_info {
        volume_size = 100
      }
    }
  }

  encryption_info {
    encryption_in_transit {
      client_broker = "TLS"
      in_cluster    = true
    }
  }

  configuration_info {
    arn      = aws_msk_configuration.this.arn
    revision = aws_msk_configuration.this.latest_revision
  }
}

output "cluster_arn" {
  value = aws_msk_cluster.this.arn
}

output "bootstrap_brokers_tls" {
  value     = aws_msk_cluster.this.bootstrap_brokers_tls
  sensitive = true
}
