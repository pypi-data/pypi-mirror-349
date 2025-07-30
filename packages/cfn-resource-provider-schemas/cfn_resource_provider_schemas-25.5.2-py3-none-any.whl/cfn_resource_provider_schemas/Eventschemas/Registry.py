SCHEMA = {
  "typeName" : "AWS::EventSchemas::Registry",
  "description" : "Resource Type definition for AWS::EventSchemas::Registry",
  "additionalProperties" : False,
  "properties" : {
    "RegistryName" : {
      "type" : "string",
      "description" : "The name of the schema registry."
    },
    "Description" : {
      "type" : "string",
      "description" : "A description of the registry to be created."
    },
    "RegistryArn" : {
      "type" : "string",
      "description" : "The ARN of the registry."
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/TagsEntry"
      },
      "description" : "Tags associated with the resource."
    }
  },
  "definitions" : {
    "TagsEntry" : {
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
  "primaryIdentifier" : [ "/properties/RegistryArn" ],
  "readOnlyProperties" : [ "/properties/RegistryArn" ],
  "createOnlyProperties" : [ "/properties/RegistryName" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "schemas:TagResource", "schemas:UntagResource", "schemas:ListTagsForResource" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "schemas:DescribeRegistry", "schemas:CreateRegistry", "schemas:TagResource" ]
    },
    "read" : {
      "permissions" : [ "schemas:DescribeRegistry" ]
    },
    "update" : {
      "permissions" : [ "schemas:DescribeRegistry", "schemas:UpdateRegistry", "schemas:TagResource", "schemas:UntagResource", "schemas:ListTagsForResource" ]
    },
    "delete" : {
      "permissions" : [ "schemas:DescribeRegistry", "schemas:DeleteRegistry" ]
    },
    "list" : {
      "permissions" : [ "schemas:ListRegistries" ]
    }
  }
}