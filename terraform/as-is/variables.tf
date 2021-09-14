variable "prefix" {
  default = "as-is"
}

variable "location" {
  default = "West Europe"
}

variable "scfile" {
  type = string
  #default = "scripts\\install-tomcat.sh" #Windows
  default = "scripts//install-tomcat.sh"
}
