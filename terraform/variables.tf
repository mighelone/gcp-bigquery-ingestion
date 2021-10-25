variable "project" {
    type = string
    default = "adept-fountain-329517"
    description = "Specifiy the GCP environment"
}


variable "api_url" {
    type = string
    description = "API url"
    default = "https://api.publicapis.org/entries"
}

variable "table" {
    type = string
    description = "(optional) describe your variable"
    default = "entries"
}

variable "dataset" {
    type = string
    description = "(optional) describe your variable"
    default = "mobkoi"
}