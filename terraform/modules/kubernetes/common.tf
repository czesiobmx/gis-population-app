resource "kubernetes_namespace" "app_ns" {
  metadata {
    name = "gis-population-app"
  }
}