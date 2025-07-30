SCHEMA = {
  "typeName" : "AWS::VerifiedPermissions::IdentitySource",
  "description" : "Definition of AWS::VerifiedPermissions::IdentitySource Resource Type",
  "definitions" : {
    "CognitoGroupConfiguration" : {
      "type" : "object",
      "properties" : {
        "GroupEntityType" : {
          "type" : "string",
          "maxLength" : 200,
          "minLength" : 1,
          "pattern" : "^([_a-zA-Z][_a-zA-Z0-9]*::)*[_a-zA-Z][_a-zA-Z0-9]*$"
        }
      },
      "required" : [ "GroupEntityType" ],
      "additionalProperties" : False
    },
    "CognitoUserPoolConfiguration" : {
      "type" : "object",
      "properties" : {
        "UserPoolArn" : {
          "type" : "string",
          "maxLength" : 255,
          "minLength" : 1,
          "pattern" : "^arn:[a-zA-Z0-9-]+:cognito-idp:(([a-zA-Z0-9-]+:\\d{12}:userpool/[\\w-]+_[0-9a-zA-Z]+))$"
        },
        "ClientIds" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "maxLength" : 255,
            "minLength" : 1,
            "pattern" : "^.*$"
          },
          "maxItems" : 1000,
          "minItems" : 0,
          "insertionOrder" : False
        },
        "GroupConfiguration" : {
          "$ref" : "#/definitions/CognitoGroupConfiguration"
        }
      },
      "required" : [ "UserPoolArn" ],
      "additionalProperties" : False
    },
    "IdentitySourceConfiguration" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "CognitoUserPoolConfiguration",
        "properties" : {
          "CognitoUserPoolConfiguration" : {
            "$ref" : "#/definitions/CognitoUserPoolConfiguration"
          }
        },
        "required" : [ "CognitoUserPoolConfiguration" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "OpenIdConnectConfiguration",
        "properties" : {
          "OpenIdConnectConfiguration" : {
            "$ref" : "#/definitions/OpenIdConnectConfiguration"
          }
        },
        "required" : [ "OpenIdConnectConfiguration" ],
        "additionalProperties" : False
      } ]
    },
    "IdentitySourceDetails" : {
      "type" : "object",
      "properties" : {
        "ClientIds" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "maxLength" : 255,
            "minLength" : 1,
            "pattern" : "^.*$"
          },
          "maxItems" : 1000,
          "minItems" : 0,
          "insertionOrder" : False
        },
        "UserPoolArn" : {
          "type" : "string",
          "maxLength" : 255,
          "minLength" : 1,
          "pattern" : "^arn:[a-zA-Z0-9-]+:cognito-idp:(([a-zA-Z0-9-]+:\\d{12}:userpool/[\\w-]+_[0-9a-zA-Z]+))$"
        },
        "DiscoveryUrl" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^https://.*$"
        },
        "OpenIdIssuer" : {
          "$ref" : "#/definitions/OpenIdIssuer"
        }
      },
      "additionalProperties" : False
    },
    "OpenIdConnectAccessTokenConfiguration" : {
      "type" : "object",
      "properties" : {
        "PrincipalIdClaim" : {
          "type" : "string",
          "default" : "sub",
          "minLength" : 1
        },
        "Audiences" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "maxLength" : 255,
            "minLength" : 1
          },
          "maxItems" : 255,
          "minItems" : 1,
          "insertionOrder" : False
        }
      },
      "additionalProperties" : False
    },
    "OpenIdConnectConfiguration" : {
      "type" : "object",
      "properties" : {
        "Issuer" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^https://.*$"
        },
        "EntityIdPrefix" : {
          "type" : "string",
          "maxLength" : 100,
          "minLength" : 1
        },
        "GroupConfiguration" : {
          "$ref" : "#/definitions/OpenIdConnectGroupConfiguration"
        },
        "TokenSelection" : {
          "$ref" : "#/definitions/OpenIdConnectTokenSelection"
        }
      },
      "required" : [ "Issuer", "TokenSelection" ],
      "additionalProperties" : False
    },
    "OpenIdConnectGroupConfiguration" : {
      "type" : "object",
      "properties" : {
        "GroupClaim" : {
          "type" : "string",
          "minLength" : 1
        },
        "GroupEntityType" : {
          "type" : "string",
          "maxLength" : 200,
          "minLength" : 1,
          "pattern" : "^([_a-zA-Z][_a-zA-Z0-9]*::)*[_a-zA-Z][_a-zA-Z0-9]*$"
        }
      },
      "required" : [ "GroupClaim", "GroupEntityType" ],
      "additionalProperties" : False
    },
    "OpenIdConnectIdentityTokenConfiguration" : {
      "type" : "object",
      "properties" : {
        "PrincipalIdClaim" : {
          "type" : "string",
          "default" : "sub",
          "minLength" : 1
        },
        "ClientIds" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "maxLength" : 255,
            "minLength" : 1,
            "pattern" : "^.*$"
          },
          "maxItems" : 1000,
          "minItems" : 0,
          "insertionOrder" : False
        }
      },
      "additionalProperties" : False
    },
    "OpenIdConnectTokenSelection" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "AccessTokenOnly",
        "properties" : {
          "AccessTokenOnly" : {
            "$ref" : "#/definitions/OpenIdConnectAccessTokenConfiguration"
          }
        },
        "required" : [ "AccessTokenOnly" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "IdentityTokenOnly",
        "properties" : {
          "IdentityTokenOnly" : {
            "$ref" : "#/definitions/OpenIdConnectIdentityTokenConfiguration"
          }
        },
        "required" : [ "IdentityTokenOnly" ],
        "additionalProperties" : False
      } ]
    },
    "OpenIdIssuer" : {
      "type" : "string",
      "enum" : [ "COGNITO" ]
    }
  },
  "properties" : {
    "Configuration" : {
      "$ref" : "#/definitions/IdentitySourceConfiguration"
    },
    "Details" : {
      "$ref" : "#/definitions/IdentitySourceDetails"
    },
    "IdentitySourceId" : {
      "type" : "string",
      "maxLength" : 200,
      "minLength" : 1,
      "pattern" : "^[a-zA-Z0-9-]*$"
    },
    "PolicyStoreId" : {
      "type" : "string",
      "maxLength" : 200,
      "minLength" : 1,
      "pattern" : "^[a-zA-Z0-9-]*$"
    },
    "PrincipalEntityType" : {
      "type" : "string",
      "maxLength" : 200,
      "minLength" : 1,
      "pattern" : "^.*$"
    }
  },
  "required" : [ "Configuration", "PolicyStoreId" ],
  "readOnlyProperties" : [ "/properties/Details", "/properties/IdentitySourceId" ],
  "createOnlyProperties" : [ "/properties/PolicyStoreId" ],
  "deprecatedProperties" : [ "/properties/Details" ],
  "primaryIdentifier" : [ "/properties/IdentitySourceId", "/properties/PolicyStoreId" ],
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-avp",
  "handlers" : {
    "create" : {
      "permissions" : [ "verifiedpermissions:CreateIdentitySource", "verifiedpermissions:GetIdentitySource", "cognito-idp:DescribeUserPool", "cognito-idp:ListUserPoolClients" ]
    },
    "read" : {
      "permissions" : [ "verifiedpermissions:GetIdentitySource", "cognito-idp:DescribeUserPool", "cognito-idp:ListUserPoolClients" ]
    },
    "update" : {
      "permissions" : [ "verifiedpermissions:UpdateIdentitySource", "verifiedpermissions:GetIdentitySource", "cognito-idp:DescribeUserPool", "cognito-idp:ListUserPoolClients" ]
    },
    "delete" : {
      "permissions" : [ "verifiedpermissions:DeleteIdentitySource", "verifiedpermissions:GetIdentitySource", "cognito-idp:DescribeUserPool", "cognito-idp:ListUserPoolClients" ]
    },
    "list" : {
      "permissions" : [ "verifiedpermissions:ListIdentitySources", "verifiedpermissions:GetIdentitySource", "cognito-idp:DescribeUserPool", "cognito-idp:ListUserPoolClients" ],
      "handlerSchema" : {
        "properties" : {
          "PolicyStoreId" : {
            "$ref" : "resource-schema.json#/properties/PolicyStoreId"
          }
        },
        "required" : [ "PolicyStoreId" ]
      }
    }
  },
  "additionalProperties" : False
}