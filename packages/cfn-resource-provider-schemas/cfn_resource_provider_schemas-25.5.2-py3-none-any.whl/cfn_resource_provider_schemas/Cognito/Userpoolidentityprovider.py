SCHEMA = {
  "typeName" : "AWS::Cognito::UserPoolIdentityProvider",
  "description" : "Resource Type definition for AWS::Cognito::UserPoolIdentityProvider",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "properties" : {
    "UserPoolId" : {
      "type" : "string"
    },
    "ProviderName" : {
      "type" : "string"
    },
    "ProviderType" : {
      "type" : "string"
    },
    "ProviderDetails" : {
      "type" : "object",
      "patternProperties" : {
        "^([\\p{L}\\p{Z}\\p{N}_.:/=+\\-@]*)$" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "IdpIdentifiers" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "AttributeMapping" : {
      "type" : "object",
      "patternProperties" : {
        "^([\\p{L}\\p{Z}\\p{N}_.:/=+\\-@]*)$" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    }
  },
  "additionalProperties" : False,
  "required" : [ "UserPoolId", "ProviderName", "ProviderType", "ProviderDetails" ],
  "createOnlyProperties" : [ "/properties/UserPoolId", "/properties/ProviderName", "/properties/ProviderType" ],
  "primaryIdentifier" : [ "/properties/UserPoolId", "/properties/ProviderName" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "cognito-idp:CreateIdentityProvider", "cognito-idp:DescribeIdentityProvider" ],
      "timeoutInMinutes" : 2
    },
    "read" : {
      "permissions" : [ "cognito-idp:DescribeIdentityProvider" ]
    },
    "update" : {
      "permissions" : [ "cognito-idp:UpdateIdentityProvider", "cognito-idp:DescribeIdentityProvider" ],
      "timeoutInMinutes" : 2
    },
    "delete" : {
      "permissions" : [ "cognito-idp:DeleteIdentityProvider", "cognito-idp:DescribeIdentityProvider" ],
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
      "permissions" : [ "cognito-idp:ListIdentityProviders" ]
    }
  }
}