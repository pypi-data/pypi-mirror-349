SCHEMA = {
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-apigateway.git",
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "handlers" : {
    "read" : {
      "permissions" : [ "apigateway:GET" ]
    },
    "create" : {
      "permissions" : [ "apigateway:PUT", "apigateway:GET", "iam:PassRole" ]
    },
    "update" : {
      "permissions" : [ "apigateway:GET", "apigateway:DELETE", "apigateway:PUT", "iam:PassRole" ]
    },
    "delete" : {
      "permissions" : [ "apigateway:DELETE" ]
    }
  },
  "typeName" : "AWS::ApiGateway::Method",
  "description" : "The ``AWS::ApiGateway::Method`` resource creates API Gateway methods that define the parameters and body that clients must send in their requests.",
  "createOnlyProperties" : [ "/properties/RestApiId", "/properties/ResourceId", "/properties/HttpMethod" ],
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/RestApiId", "/properties/ResourceId", "/properties/HttpMethod" ],
  "definitions" : {
    "MethodResponse" : {
      "description" : "",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ResponseParameters" : {
          "patternProperties" : {
            "[a-zA-Z0-9]+" : {
              "type" : [ "boolean", "string" ]
            }
          },
          "description" : "",
          "additionalProperties" : False,
          "type" : "object"
        },
        "StatusCode" : {
          "description" : "",
          "type" : "string"
        },
        "ResponseModels" : {
          "patternProperties" : {
            "[a-zA-Z0-9]+" : {
              "type" : "string"
            }
          },
          "description" : "",
          "additionalProperties" : False,
          "type" : "object"
        }
      },
      "required" : [ "StatusCode" ]
    },
    "Integration" : {
      "description" : "``Integration`` is a property of the [AWS::ApiGateway::Method](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html) resource that specifies information about the target backend that a method calls.",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CacheNamespace" : {
          "description" : "",
          "type" : "string"
        },
        "ConnectionType" : {
          "description" : "",
          "type" : "string",
          "enum" : [ "INTERNET", "VPC_LINK" ]
        },
        "IntegrationResponses" : {
          "uniqueItems" : True,
          "description" : "",
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/IntegrationResponse"
          }
        },
        "IntegrationHttpMethod" : {
          "description" : "",
          "type" : "string"
        },
        "Uri" : {
          "description" : "",
          "type" : "string"
        },
        "PassthroughBehavior" : {
          "description" : "",
          "type" : "string",
          "enum" : [ "WHEN_NO_MATCH", "WHEN_NO_TEMPLATES", "NEVER" ]
        },
        "RequestParameters" : {
          "patternProperties" : {
            "[a-zA-Z0-9]+" : {
              "type" : "string"
            }
          },
          "description" : "",
          "additionalProperties" : False,
          "type" : "object"
        },
        "ConnectionId" : {
          "description" : "",
          "type" : "string"
        },
        "Type" : {
          "description" : "",
          "type" : "string",
          "enum" : [ "AWS", "AWS_PROXY", "HTTP", "HTTP_PROXY", "MOCK" ]
        },
        "CacheKeyParameters" : {
          "uniqueItems" : True,
          "description" : "",
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "ContentHandling" : {
          "description" : "",
          "type" : "string",
          "enum" : [ "CONVERT_TO_BINARY", "CONVERT_TO_TEXT" ]
        },
        "RequestTemplates" : {
          "patternProperties" : {
            "[a-zA-Z0-9]+" : {
              "type" : "string"
            }
          },
          "description" : "",
          "additionalProperties" : False,
          "type" : "object"
        },
        "TimeoutInMillis" : {
          "description" : "",
          "type" : "integer",
          "minimum" : 50
        },
        "Credentials" : {
          "description" : "",
          "type" : "string"
        }
      },
      "required" : [ "Type" ]
    },
    "IntegrationResponse" : {
      "description" : "``IntegrationResponse`` is a property of the [Amazon API Gateway Method Integration](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html) property type that specifies the response that API Gateway sends after a method's backend finishes processing a request.",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ResponseTemplates" : {
          "patternProperties" : {
            "[a-zA-Z0-9]+" : {
              "type" : "string"
            }
          },
          "description" : "",
          "additionalProperties" : False,
          "type" : "object"
        },
        "SelectionPattern" : {
          "description" : "",
          "type" : "string"
        },
        "ContentHandling" : {
          "description" : "",
          "type" : "string",
          "enum" : [ "CONVERT_TO_BINARY", "CONVERT_TO_TEXT" ]
        },
        "ResponseParameters" : {
          "patternProperties" : {
            "[a-zA-Z0-9]+" : {
              "type" : "string"
            }
          },
          "description" : "",
          "additionalProperties" : False,
          "type" : "object"
        },
        "StatusCode" : {
          "description" : "",
          "type" : "string"
        }
      },
      "required" : [ "StatusCode" ]
    }
  },
  "properties" : {
    "Integration" : {
      "description" : "",
      "$ref" : "#/definitions/Integration"
    },
    "OperationName" : {
      "description" : "",
      "type" : "string"
    },
    "RequestModels" : {
      "patternProperties" : {
        "[a-zA-Z0-9]+" : {
          "type" : "string"
        }
      },
      "description" : "",
      "additionalProperties" : False,
      "type" : "object"
    },
    "RestApiId" : {
      "description" : "",
      "type" : "string"
    },
    "AuthorizationScopes" : {
      "description" : "",
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "RequestValidatorId" : {
      "description" : "",
      "type" : "string"
    },
    "RequestParameters" : {
      "patternProperties" : {
        "[a-zA-Z0-9]+" : {
          "type" : [ "boolean", "string" ]
        }
      },
      "description" : "",
      "additionalProperties" : False,
      "type" : "object"
    },
    "MethodResponses" : {
      "uniqueItems" : True,
      "description" : "",
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/MethodResponse"
      }
    },
    "AuthorizerId" : {
      "description" : "",
      "type" : "string"
    },
    "ResourceId" : {
      "description" : "",
      "type" : "string"
    },
    "ApiKeyRequired" : {
      "description" : "",
      "type" : "boolean"
    },
    "AuthorizationType" : {
      "description" : "The method's authorization type. This parameter is required. For valid values, see [Method](https://docs.aws.amazon.com/apigateway/latest/api/API_Method.html) in the *API Gateway API Reference*.\n  If you specify the ``AuthorizerId`` property, specify ``CUSTOM`` or ``COGNITO_USER_POOLS`` for this property.",
      "type" : "string"
    },
    "HttpMethod" : {
      "description" : "",
      "type" : "string"
    }
  },
  "required" : [ "RestApiId", "ResourceId", "HttpMethod" ]
}