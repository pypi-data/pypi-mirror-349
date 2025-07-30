SCHEMA = {
  "typeName" : "AWS::Inspector::ResourceGroup",
  "description" : "Resource Type definition for AWS::Inspector::ResourceGroup",
  "additionalProperties" : False,
  "properties" : {
    "Arn" : {
      "type" : "string"
    },
    "ResourceGroupTags" : {
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
  "required" : [ "ResourceGroupTags" ],
  "readOnlyProperties" : [ "/properties/Arn" ],
  "createOnlyProperties" : [ "/properties/ResourceGroupTags" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "taggable" : False,
  "handlers" : {
    "create" : {
      "permissions" : [ "inspector:CreateResourceGroup" ]
    },
    "read" : {
      "permissions" : [ "inspector:CreateResourceGroup" ]
    },
    "delete" : {
      "permissions" : [ "inspector:CreateResourceGroup" ]
    }
  }
}