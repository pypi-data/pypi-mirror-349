SCHEMA = {
  "typeName" : "AWS::DocDB::DBSubnetGroup",
  "description" : "Resource Type definition for AWS::DocDB::DBSubnetGroup",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "DBSubnetGroupName" : {
      "type" : "string"
    },
    "DBSubnetGroupDescription" : {
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
        "Key" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    }
  },
  "required" : [ "DBSubnetGroupDescription", "SubnetIds" ],
  "createOnlyProperties" : [ "/properties/DBSubnetGroupName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}