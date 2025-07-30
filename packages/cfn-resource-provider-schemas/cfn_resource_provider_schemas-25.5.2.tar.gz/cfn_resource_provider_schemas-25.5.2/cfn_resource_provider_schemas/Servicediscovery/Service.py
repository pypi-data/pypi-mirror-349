SCHEMA = {
  "typeName" : "AWS::ServiceDiscovery::Service",
  "description" : "Resource Type definition for AWS::ServiceDiscovery::Service",
  "additionalProperties" : False,
  "properties" : {
    "Type" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    },
    "HealthCheckCustomConfig" : {
      "$ref" : "#/definitions/HealthCheckCustomConfig"
    },
    "DnsConfig" : {
      "$ref" : "#/definitions/DnsConfig"
    },
    "ServiceAttributes" : {
      "type" : "object"
    },
    "Id" : {
      "type" : "string"
    },
    "NamespaceId" : {
      "type" : "string"
    },
    "HealthCheckConfig" : {
      "$ref" : "#/definitions/HealthCheckConfig"
    },
    "Arn" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "HealthCheckCustomConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "FailureThreshold" : {
          "type" : "number"
        }
      }
    },
    "DnsConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DnsRecords" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/DnsRecord"
          }
        },
        "RoutingPolicy" : {
          "type" : "string"
        },
        "NamespaceId" : {
          "type" : "string"
        }
      },
      "required" : [ "DnsRecords" ]
    },
    "HealthCheckConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "ResourcePath" : {
          "type" : "string"
        },
        "FailureThreshold" : {
          "type" : "number"
        }
      },
      "required" : [ "Type" ]
    },
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    },
    "DnsRecord" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TTL" : {
          "type" : "number"
        },
        "Type" : {
          "type" : "string"
        }
      },
      "required" : [ "Type", "TTL" ]
    }
  },
  "createOnlyProperties" : [ "/properties/HealthCheckCustomConfig", "/properties/Name", "/properties/Type", "/properties/NamespaceId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Arn" ]
}