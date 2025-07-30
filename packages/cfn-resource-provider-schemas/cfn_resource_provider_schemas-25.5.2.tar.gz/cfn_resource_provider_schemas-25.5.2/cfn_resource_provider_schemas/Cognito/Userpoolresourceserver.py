SCHEMA = {
  "typeName" : "AWS::Cognito::UserPoolResourceServer",
  "description" : "Resource Type definition for AWS::Cognito::UserPoolResourceServer",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "definitions" : {
    "ResourceServerScopeType" : {
      "type" : "object",
      "properties" : {
        "ScopeDescription" : {
          "type" : "string"
        },
        "ScopeName" : {
          "type" : "string"
        }
      },
      "required" : [ "ScopeDescription", "ScopeName" ],
      "additionalProperties" : False
    }
  },
  "properties" : {
    "UserPoolId" : {
      "type" : "string"
    },
    "Identifier" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    },
    "Scopes" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/ResourceServerScopeType"
      }
    }
  },
  "additionalProperties" : False,
  "required" : [ "UserPoolId", "Identifier", "Name" ],
  "createOnlyProperties" : [ "/properties/UserPoolId", "/properties/Identifier" ],
  "primaryIdentifier" : [ "/properties/UserPoolId", "/properties/Identifier" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "cognito-idp:CreateResourceServer" ],
      "timeoutInMinutes" : 2
    },
    "read" : {
      "permissions" : [ "cognito-idp:DescribeResourceServer" ]
    },
    "update" : {
      "permissions" : [ "cognito-idp:UpdateResourceServer" ],
      "timeoutInMinutes" : 2
    },
    "delete" : {
      "permissions" : [ "cognito-idp:DeleteResourceServer" ],
      "timeoutInMinutes" : 2
    },
    "list" : {
      "handlerSchema" : {
        "properties" : {
          "UserPoolId" : {
            "$ref" : "resource-schema.json#/properties/UserPoolId"
          }
        },
        "required" : [ "UserPoolId" ]
      },
      "permissions" : [ "cognito-idp:ListResourceServers" ]
    }
  }
}