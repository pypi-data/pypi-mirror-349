SCHEMA = {
  "typeName" : "AWS::PinpointEmail::DedicatedIpPool",
  "description" : "Resource Type definition for AWS::PinpointEmail::DedicatedIpPool",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "PoolName" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tags"
      }
    }
  },
  "definitions" : {
    "Tags" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      }
    }
  },
  "createOnlyProperties" : [ "/properties/PoolName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}