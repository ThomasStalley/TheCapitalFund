variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-2"
}

variable "app_name" {
  description = "Application name (used for all resource names)"
  type        = string
  default     = "thecapitalfund"
}

variable "app_port" {
  description = "Port the container listens on"
  type        = number
  default     = 10000
}

variable "api_key" {
  description = "API key for api.auchester.com"
  type        = string
  sensitive   = true
}
