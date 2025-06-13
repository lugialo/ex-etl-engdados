variable "env" {
  type    = string
  default = ""
}

variable "dbwscope" {
  type    = string
  default = "azkvdbwscope"
}

variable "stgaccname" {
  type    = string
  default = "stacdata"
}

variable "default_location" {
  default     = "Brazil South"
  type = string
}

  variable "company" {
  default = "trabalhoed"
  type = string
}


variable "secretsname" {
    type = map
    default = {
        "databricksappsecret" = "databricksappsecret"
        "databricksappclientid" = "databricksappclientid"
        "tenantid" = "tenantid"
    }
}