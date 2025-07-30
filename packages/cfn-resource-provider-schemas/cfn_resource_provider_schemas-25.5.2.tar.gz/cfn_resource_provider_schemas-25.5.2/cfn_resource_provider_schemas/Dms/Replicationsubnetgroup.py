SCHEMA = {
  "typeName" : "AWS::DMS::ReplicationSubnetGroup",
  "description" : "Resource Type definition for AWS::DMS::ReplicationSubnetGroup",
  "additionalProperties" : False,
  "properties" : {
    "ReplicationSubnetGroupDescription" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "ReplicationSubnetGroupIdentifier" : {
      "type" : "string"
    },
    "SubnetIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
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
  "required" : [ "ReplicationSubnetGroupDescription", "SubnetIds" ],
  "createOnlyProperties" : [ "/properties/ReplicationSubnetGroupIdentifier" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}