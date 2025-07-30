SCHEMA = {
  "typeName" : "AWS::QLDB::Ledger",
  "description" : "Resource Type definition for AWS::QLDB::Ledger",
  "additionalProperties" : False,
  "properties" : {
    "PermissionsMode" : {
      "type" : "string"
    },
    "DeletionProtection" : {
      "type" : "boolean"
    },
    "Id" : {
      "type" : "string"
    },
    "KmsKey" : {
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
  "required" : [ "PermissionsMode" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}