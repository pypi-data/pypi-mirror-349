SCHEMA = {
  "typeName" : "AWS::VerifiedPermissions::PolicyStore",
  "description" : "Represents a policy store that you can place schema, policies, and policy templates in to validate authorization requests",
  "definitions" : {
    "ValidationMode" : {
      "type" : "string",
      "enum" : [ "OFF", "STRICT" ]
    },
    "ValidationSettings" : {
      "type" : "object",
      "properties" : {
        "Mode" : {
          "$ref" : "#/definitions/ValidationMode"
        }
      },
      "required" : [ "Mode" ],
      "additionalProperties" : False
    },
    "SchemaJson" : {
      "type" : "string"
    },
    "SchemaDefinition" : {
      "type" : "object",
      "properties" : {
        "CedarJson" : {
          "$ref" : "#/definitions/SchemaJson"
        }
      },
      "additionalProperties" : False
    },
    "DeletionMode" : {
      "type" : "string",
      "default" : "DISABLED",
      "enum" : [ "ENABLED", "DISABLED" ]
    },
    "DeletionProtection" : {
      "type" : "object",
      "properties" : {
        "Mode" : {
          "$ref" : "#/definitions/DeletionMode"
        }
      },
      "required" : [ "Mode" ],
      "additionalProperties" : False
    },
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
      "required" : [ "Key", "Value" ]
    }
  },
  "properties" : {
    "Arn" : {
      "type" : "string",
      "maxLength" : 2500,
      "minLength" : 1,
      "pattern" : "^arn:[^:]*:[^:]*:[^:]*:[^:]*:.*$"
    },
    "Description" : {
      "type" : "string",
      "maxLength" : 150,
      "minLength" : 0
    },
    "PolicyStoreId" : {
      "type" : "string",
      "maxLength" : 200,
      "minLength" : 1,
      "pattern" : "^[a-zA-Z0-9-]*$"
    },
    "ValidationSettings" : {
      "$ref" : "#/definitions/ValidationSettings"
    },
    "Schema" : {
      "$ref" : "#/definitions/SchemaDefinition"
    },
    "DeletionProtection" : {
      "$ref" : "#/definitions/DeletionProtection"
    },
    "Tags" : {
      "description" : "The tags to add to the policy store",
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "required" : [ "ValidationSettings" ],
  "readOnlyProperties" : [ "/properties/Arn", "/properties/PolicyStoreId" ],
  "primaryIdentifier" : [ "/properties/PolicyStoreId" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "verifiedpermissions:TagResource", "verifiedpermissions:ListTagsForResource", "verifiedpermissions:UntagResource" ]
  },
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-avp",
  "propertyTransform" : {
    "/properties/Schema/CedarJson" : "$join([CedarJson, \"{}\"])"
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "verifiedpermissions:CreatePolicyStore", "verifiedpermissions:TagResource", "verifiedpermissions:GetPolicyStore", "verifiedpermissions:PutSchema" ]
    },
    "read" : {
      "permissions" : [ "verifiedpermissions:GetPolicyStore", "verifiedpermissions:ListTagsForResource", "verifiedpermissions:GetSchema" ]
    },
    "update" : {
      "permissions" : [ "verifiedpermissions:UpdatePolicyStore", "verifiedpermissions:GetPolicyStore", "verifiedpermissions:TagResource", "verifiedpermissions:UntagResource", "verifiedpermissions:GetSchema", "verifiedpermissions:PutSchema" ]
    },
    "delete" : {
      "permissions" : [ "verifiedpermissions:DeletePolicyStore", "verifiedpermissions:GetPolicyStore" ]
    },
    "list" : {
      "permissions" : [ "verifiedpermissions:ListPolicyStores", "verifiedpermissions:GetPolicyStore", "verifiedpermissions:GetSchema" ]
    }
  },
  "additionalProperties" : False
}