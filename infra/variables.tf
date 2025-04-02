variable "resource_group_name" {
  type = string

}

variable "region" {
  type = string

}

variable "aks_cluster_info" {
  type = object({
    name       = string
    dns_prefix = string
    node_count = optional(number, 1)
    vm_size    = optional(string, "Standard_B2ms")

  })

}

variable "build_id" {
  type    = string
  default = "1"

}
