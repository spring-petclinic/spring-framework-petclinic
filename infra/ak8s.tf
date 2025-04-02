resource "azurerm_resource_group" "base" {
  name     = var.resource_group_name
  location = var.region
  tags = {
    Env = terraform.workspace
  }
}

resource "azurerm_kubernetes_cluster" "base" {
  name                = var.aks_cluster_info.name
  location            = azurerm_resource_group.base.location
  resource_group_name = azurerm_resource_group.base.name
  dns_prefix          = var.aks_cluster_info.dns_prefix

  default_node_pool {
    name       = "default"
    node_count = var.aks_cluster_info.node_count
    vm_size    = var.aks_cluster_info.vm_size
  }
  identity {
    type = "SystemAssigned"
  }
  depends_on = [azurerm_resource_group.base]
}

resource "null_resource" "config" {
  triggers = {
    build_id = var.build_id
  }
  provisioner "local-exec" {
    command = "az aks get-credentials --resource-group ${azurerm_resource_group.base.name} --name ${azurerm_kubernetes_cluster.base.name}"

  }
  depends_on = [azurerm_kubernetes_cluster.base]
}



