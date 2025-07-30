SCHEMA = {
  "typeName" : "AWS::Cognito::IdentityPool",
  "description" : "Resource Type definition for AWS::Cognito::IdentityPool",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "additionalProperties" : False,
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/IdentityPoolTags",
    "permissions" : [ "cognito-identity:TagResource", "cognito-identity:UntagResource" ]
  },
  "definitions" : {
    "Tag" : {
      "description" : "A key-value pair to associate with a resource.",
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "description" : "The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "type" : "string",
          "description" : "The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.",
          "minLength" : 0,
          "maxLength" : 256
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    },
    "PushSync" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ApplicationArns" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        },
        "RoleArn" : {
          "type" : "string"
        }
      }
    },
    "CognitoIdentityProvider" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ServerSideTokenCheck" : {
          "type" : "boolean"
        },
        "ProviderName" : {
          "type" : "string"
        },
        "ClientId" : {
          "type" : "string"
        }
      },
      "required" : [ "ProviderName", "ClientId" ]
    },
    "CognitoStreams" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "StreamingStatus" : {
          "type" : "string"
        },
        "StreamName" : {
          "type" : "string"
        },
        "RoleArn" : {
          "type" : "string"
        }
      }
    }
  },
  "properties" : {
    "PushSync" : {
      "$ref" : "#/definitions/PushSync"
    },
    "CognitoIdentityProviders" : {
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/CognitoIdentityProvider"
      }
    },
    "DeveloperProviderName" : {
      "type" : "string"
    },
    "CognitoStreams" : {
      "$ref" : "#/definitions/CognitoStreams"
    },
    "SupportedLoginProviders" : {
      "type" : "object"
    },
    "Name" : {
      "type" : "string"
    },
    "CognitoEvents" : {
      "type" : "object"
    },
    "Id" : {
      "type" : "string"
    },
    "IdentityPoolName" : {
      "type" : "string"
    },
    "AllowUnauthenticatedIdentities" : {
      "type" : "boolean"
    },
    "SamlProviderARNs" : {
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "type" : "string"
      }
    },
    "OpenIdConnectProviderARNs" : {
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "type" : "string"
      }
    },
    "AllowClassicFlow" : {
      "type" : "boolean"
    },
    "IdentityPoolTags" : {
      "description" : "An array of key-value pairs to apply to this resource.",
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "required" : [ "AllowUnauthenticatedIdentities" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Name" ],
  "writeOnlyProperties" : [ "/properties/PushSync", "/properties/CognitoStreams", "/properties/CognitoEvents" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "cognito-identity:CreateIdentityPool", "cognito-sync:SetIdentityPoolConfiguration", "cognito-sync:SetCognitoEvents", "cognito-identity:TagResource", "iam:PassRole" ]
    },
    "read" : {
      "permissions" : [ "cognito-identity:DescribeIdentityPool" ]
    },
    "update" : {
      "permissions" : [ "cognito-identity:UpdateIdentityPool", "cognito-identity:DescribeIdentityPool", "cognito-sync:SetIdentityPoolConfiguration", "cognito-sync:SetCognitoEvents", "cognito-identity:TagResource", "cognito-identity:UntagResource", "iam:PassRole" ]
    },
    "delete" : {
      "permissions" : [ "cognito-identity:DeleteIdentityPool" ]
    },
    "list" : {
      "permissions" : [ "cognito-identity:ListIdentityPools" ]
    }
  }
}