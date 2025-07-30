SCHEMA = {
  "typeName" : "AWS::ServiceDiscovery::PublicDnsNamespace",
  "description" : "Resource Type definition for AWS::ServiceDiscovery::PublicDnsNamespace",
  "additionalProperties" : False,
  "properties" : {
    "Description" : {
      "type" : "string"
    },
    "HostedZoneId" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "Properties" : {
      "$ref" : "#/definitions/Properties"
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
    "SOA" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TTL" : {
          "type" : "number"
        }
      }
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
    "Properties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DnsProperties" : {
          "$ref" : "#/definitions/PublicDnsPropertiesMutable"
        }
      }
    },
    "PublicDnsPropertiesMutable" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SOA" : {
          "$ref" : "#/definitions/SOA"
        }
      }
    }
  },
  "required" : [ "Name" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/HostedZoneId", "/properties/Arn" ]
}