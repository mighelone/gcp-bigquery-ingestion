variable "project" {
    type = string
    default = "adept-fountain-329517"
    description = "Specifiy the GCP environment"
}


variable "table" {
    type = string
    description = "(optional) describe your variable"
    default = "meteostat"
}

variable "dataset" {
    type = string
    description = "(optional) describe your variable"
    default = "mobkoi"
}