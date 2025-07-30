SCHEMA = {
  "typeName" : "AWS::ElastiCache::SecurityGroup",
  "description" : "Resource Type definition for AWS::ElastiCache::SecurityGroup",
  "additionalProperties" : False,
  "properties" : {
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "Description" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    }
  },
  "definitions" : {
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
    }
  },
  "required" : [ "Description" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}