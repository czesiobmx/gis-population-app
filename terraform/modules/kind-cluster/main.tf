terraform {
  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "0.9.0"
    }
  }
}

resource "kind_cluster" "kind_cluster" {
  name       = "kind"
  node_image = "kindest/node:v1.34.0"
  wait_for_ready = true

  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    node {
      role = "control-plane"
    }

    node {
      role = "worker"

      # Mount host directory into the worker node container
      extra_mounts {
        host_path      = "${var.host_workdir}"
        container_path = "/app"
      }
    }
  }
}