output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.app.name
}

output "ecs_service_name" {
  value = aws_ecs_service.app.name
}

output "nameservers" {
  value = aws_route53_zone.app.name_servers
}

output "hosted_zone_id" {
  value = aws_route53_zone.app.zone_id
}
