SCHEMA = {
  "typeName" : "AWS::ApiGateway::Authorizer",
  "description" : "The ``AWS::ApiGateway::Authorizer`` resource creates an authorization layer that API Gateway activates for methods that have authorization enabled. API Gateway activates the authorizer when a client calls those methods.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-apigateway.git",
  "properties" : {
    "RestApiId" : {
      "description" : "",
      "type" : "string"
    },
    "AuthorizerId" : {
      "type" : "string",
      "description" : ""
    },
    "AuthType" : {
      "description" : "",
      "type" : "string"
    },
    "AuthorizerCredentials" : {
      "description" : "",
      "type" : "string"
    },
    "AuthorizerResultTtlInSeconds" : {
      "description" : "",
      "type" : "integer"
    },
    "AuthorizerUri" : {
      "description" : "",
      "type" : "string"
    },
    "IdentitySource" : {
      "description" : "",
      "type" : "string"
    },
    "IdentityValidationExpression" : {
      "description" : "",
      "type" : "string"
    },
    "Name" : {
      "description" : "",
      "type" : "string"
    },
    "ProviderARNs" : {
      "description" : "",
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      },
      "insertionOrder" : False
    },
    "Type" : {
      "description" : "",
      "type" : "string"
    }
  },
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "additionalProperties" : False,
  "required" : [ "RestApiId", "Type", "Name" ],
  "createOnlyProperties" : [ "/properties/RestApiId" ],
  "primaryIdentifier" : [ "/properties/RestApiId", "/properties/AuthorizerId" ],
  "readOnlyProperties" : [ "/properties/AuthorizerId" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "apigateway:POST", "iam:PassRole" ]
    },
    "read" : {
      "permissions" : [ "apigateway:GET" ]
    },
    "update" : {
      "permissions" : [ "apigateway:GET", "apigateway:PATCH", "iam:PassRole" ]
    },
    "delete" : {
      "permissions" : [ "apigateway:DELETE" ]
    },
    "list" : {
      "handlerSchema" : {
        "properties" : {
          "RestApiId" : {
            "$ref" : "resource-schema.json#/properties/RestApiId"
          }
        },
        "required" : [ "RestApiId" ]
      },
      "permissions" : [ "apigateway:GET" ]
    }
  }
}