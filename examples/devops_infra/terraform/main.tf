terraform {
  required_version = ">= 1.4.0"
}

provider "null" {}

resource "null_resource" "example" {}
