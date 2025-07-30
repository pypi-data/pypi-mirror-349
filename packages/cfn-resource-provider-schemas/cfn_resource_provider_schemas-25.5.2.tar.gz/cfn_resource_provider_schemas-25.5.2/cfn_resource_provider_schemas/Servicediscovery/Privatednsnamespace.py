SCHEMA = {
  "typeName" : "AWS::ServiceDiscovery::PrivateDnsNamespace",
  "description" : "Resource Type definition for AWS::ServiceDiscovery::PrivateDnsNamespace",
  "additionalProperties" : False,
  "properties" : {
    "Description" : {
      "type" : "string"
    },
    "HostedZoneId" : {
      "type" : "string"
    },
    "Vpc" : {
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
    "PrivateDnsPropertiesMutable" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SOA" : {
          "$ref" : "#/definitions/SOA"
        }
      }
    },
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
          "$ref" : "#/definitions/PrivateDnsPropertiesMutable"
        }
      }
    }
  },
  "required" : [ "Vpc", "Name" ],
  "createOnlyProperties" : [ "/properties/Vpc", "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/HostedZoneId", "/properties/Arn" ]
}