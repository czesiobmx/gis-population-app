resource "kubernetes_deployment" "population_app" {
  metadata {
    name      = "population-app"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "population-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "population-app"
        }
      }

      spec {
        container {
          name  = "population-app"
          image = "population-app:latest"
          image_pull_policy = "IfNotPresent"
          stdin = true
          tty   = true

          volume_mount {
            name       = "app-code"
            mount_path = "/app"
          }
        }

        volume {
          name = "app-code"

          host_path {
            path = "/app" # Mounted from Kind worker node
            type = "Directory"
          }
        }
      }
    }
  }

  depends_on = [kubernetes_namespace.app_ns, kubernetes_deployment.mysql_db, kubernetes_service.mysql_db]
}