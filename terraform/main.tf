terraform {
  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "0.9.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.38.0"
    }
  }
}

provider "kind" {}

module "kind_cluster" {
  source = "./modules/kind-cluster"
  host_workdir = abspath("${path.root}/../app")
}

resource "local_file" "kubeconfig" {
  content  = module.kind_cluster.kubeconfig
  filename = "${path.module}/kind_kubeconfig.yaml"
}

provider "kubernetes" {
  config_path = local_file.kubeconfig.filename
}

module "kubernetes_resources" {
  source = "./modules/kubernetes"
}