resource "kubernetes_deployment" "mysql_db" {
  metadata {
    name      = "mysql-db"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "mysql-db"
      }
    }

    template {
      metadata {
        labels = {
          app = "mysql-db"
        }
      }

      spec {
        container {
          name  = "mysql-db"
          image = "mysql-db:latest"
          image_pull_policy = "IfNotPresent"

          env_from {
            secret_ref {
              name = "mysql-secret"
            }
          }

          port {
            container_port = 3306
          }

          readiness_probe {
            exec {
              command = ["mysqladmin", "ping", "-h", "localhost"]
            }
            initial_delay_seconds = 5
            period_seconds        = 5
          }

          volume_mount {
            name       = "mysql-storage"
            mount_path = "/var/lib/mysql"
          }
        }

        volume {
          name = "mysql-storage"
          empty_dir {}
        }
      }
    }
  }

  depends_on = [kubernetes_namespace.app_ns]
}