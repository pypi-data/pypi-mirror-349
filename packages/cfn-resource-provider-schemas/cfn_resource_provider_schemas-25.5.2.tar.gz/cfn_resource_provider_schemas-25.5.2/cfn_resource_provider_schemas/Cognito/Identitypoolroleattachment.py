SCHEMA = {
  "typeName" : "AWS::Cognito::IdentityPoolRoleAttachment",
  "description" : "Resource Type definition for AWS::Cognito::IdentityPoolRoleAttachment",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "additionalProperties" : False,
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "definitions" : {
    "MappingRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Claim" : {
          "type" : "string"
        },
        "MatchType" : {
          "type" : "string"
        },
        "RoleARN" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "required" : [ "Claim", "MatchType", "RoleARN", "Value" ]
    },
    "RulesConfigurationType" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Rules" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/MappingRule"
          }
        }
      },
      "required" : [ "Rules" ]
    },
    "RoleMapping" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "AmbiguousRoleResolution" : {
          "type" : "string"
        },
        "RulesConfiguration" : {
          "$ref" : "#/definitions/RulesConfigurationType"
        },
        "IdentityProvider" : {
          "type" : "string"
        }
      },
      "required" : [ "Type" ]
    }
  },
  "properties" : {
    "IdentityPoolId" : {
      "type" : "string"
    },
    "Roles" : {
      "patternProperties" : {
        "^.+$" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "Id" : {
      "type" : "string"
    },
    "RoleMappings" : {
      "patternProperties" : {
        "^.+$" : {
          "$ref" : "#/definitions/RoleMapping"
        }
      },
      "additionalProperties" : False
    }
  },
  "required" : [ "IdentityPoolId" ],
  "createOnlyProperties" : [ "/properties/IdentityPoolId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ],
  "additionalIdentifiers" : [ [ "/properties/IdentityPoolId" ] ],
  "handlers" : {
    "create" : {
      "permissions" : [ "cognito-identity:GetIdentityPoolRoles", "cognito-identity:SetIdentityPoolRoles", "iam:PassRole" ]
    },
    "read" : {
      "permissions" : [ "cognito-identity:GetIdentityPoolRoles" ]
    },
    "update" : {
      "permissions" : [ "cognito-identity:GetIdentityPoolRoles", "cognito-identity:SetIdentityPoolRoles", "iam:PassRole" ]
    },
    "delete" : {
      "permissions" : [ "cognito-identity:GetIdentityPoolRoles", "cognito-identity:SetIdentityPoolRoles" ]
    },
    "list" : {
      "handlerSchema" : {
        "properties" : {
          "IdentityPoolId" : {
            "$ref" : "resource-schema.json#/properties/IdentityPoolId"
          }
        },
        "required" : [ "IdentityPoolId" ]
      },
      "permissions" : [ "cognito-identity:GetIdentityPoolRoles" ]
    }
  }
}