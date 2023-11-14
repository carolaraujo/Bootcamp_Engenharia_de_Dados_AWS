provider "aws" {
  profile = "default"
  region = "us-east-1"
}

resource "aws_s3_bucket" "bucket-producao" {
  bucket = "bucket-da-pastel-producao"
  tags = {
    "Area" = "Produtos"
    "Enviroment" = "Production"
  }
}

resource "aws_s3_bucket" "bucket-desenvolvimento" {
  bucket = "bucket-da-pastel-desenvolvimento"
  tags = {
    "Area" = "Produtos"
    "Enviroment" = "Development"
  }
}