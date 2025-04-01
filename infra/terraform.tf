# Azure Provider source and version being used
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 4.14.0"
    }
  }
  
  # backend "azurerm" {
  #   # Can be passed via `-backend-config=`"resource_group_name=<resource group name>"` in the `init` command.
  #   resource_group_name = "tfstate"
  #   # Can be passed via `-backend-config=`"storage_account_name=<storage account name>"` in the `init` command.
  #   storage_account_name = "tfstatesdemo"
  #   # Can be passed via `-backend-config=`"container_name=<container name>"` in the `init` command.
  #   container_name = "workshop-tfstate"
  #   # Can be passed via `-backend-config=`"key=<blob key name>"` in the `init` command.
  #   key = "Wokshop.tfstate"

  # }

  required_version = ">= 1.10.0" 
}

