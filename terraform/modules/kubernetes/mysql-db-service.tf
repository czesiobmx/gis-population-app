resource "kubernetes_service" "mysql_db" {
  metadata {
    name      = "mysql-db"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  spec {
    selector = {
      app = "mysql-db"
    }

    port {
      port        = 3306
      target_port = 3306
    }

    type = "ClusterIP"
  }

  depends_on = [kubernetes_deployment.mysql_db]
}