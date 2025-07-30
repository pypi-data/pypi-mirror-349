SCHEMA = {
  "typeName" : "AWS::ApiGateway::BasePathMapping",
  "description" : "The ``AWS::ApiGateway::BasePathMapping`` resource creates a base path that clients who call your API must use in the invocation URL.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-apigateway",
  "additionalProperties" : False,
  "properties" : {
    "BasePath" : {
      "type" : "string",
      "description" : ""
    },
    "DomainName" : {
      "type" : "string",
      "description" : ""
    },
    "RestApiId" : {
      "type" : "string",
      "description" : ""
    },
    "Stage" : {
      "type" : "string",
      "description" : ""
    }
  },
  "required" : [ "DomainName" ],
  "createOnlyProperties" : [ "/properties/DomainName", "/properties/BasePath" ],
  "primaryIdentifier" : [ "/properties/DomainName", "/properties/BasePath" ],
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "apigateway:POST", "apigateway:GET" ]
    },
    "read" : {
      "permissions" : [ "apigateway:GET" ]
    },
    "update" : {
      "permissions" : [ "apigateway:GET", "apigateway:DELETE", "apigateway:PATCH" ]
    },
    "delete" : {
      "permissions" : [ "apigateway:DELETE" ]
    },
    "list" : {
      "handlerSchema" : {
        "properties" : {
          "DomainName" : {
            "$ref" : "resource-schema.json#/properties/DomainName"
          }
        },
        "required" : [ "DomainName" ]
      },
      "permissions" : [ "apigateway:GET" ]
    }
  }
}