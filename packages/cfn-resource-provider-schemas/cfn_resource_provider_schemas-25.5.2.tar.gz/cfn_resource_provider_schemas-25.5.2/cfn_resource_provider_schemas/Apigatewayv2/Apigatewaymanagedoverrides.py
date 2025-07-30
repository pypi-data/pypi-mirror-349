SCHEMA = {
  "typeName" : "AWS::ApiGatewayV2::ApiGatewayManagedOverrides",
  "description" : "Resource Type definition for AWS::ApiGatewayV2::ApiGatewayManagedOverrides",
  "additionalProperties" : False,
  "properties" : {
    "Stage" : {
      "$ref" : "#/definitions/StageOverrides"
    },
    "Integration" : {
      "$ref" : "#/definitions/IntegrationOverrides"
    },
    "Id" : {
      "type" : "string"
    },
    "ApiId" : {
      "type" : "string"
    },
    "Route" : {
      "$ref" : "#/definitions/RouteOverrides"
    }
  },
  "definitions" : {
    "AccessLogSettings" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DestinationArn" : {
          "type" : "string"
        },
        "Format" : {
          "type" : "string"
        }
      }
    },
    "RouteSettings" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DetailedMetricsEnabled" : {
          "type" : "boolean"
        },
        "LoggingLevel" : {
          "type" : "string"
        },
        "DataTraceEnabled" : {
          "type" : "boolean"
        },
        "ThrottlingBurstLimit" : {
          "type" : "integer"
        },
        "ThrottlingRateLimit" : {
          "type" : "number"
        }
      }
    },
    "StageOverrides" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Description" : {
          "type" : "string"
        },
        "AccessLogSettings" : {
          "$ref" : "#/definitions/AccessLogSettings"
        },
        "AutoDeploy" : {
          "type" : "boolean"
        },
        "RouteSettings" : {
          "type" : "object"
        },
        "StageVariables" : {
          "type" : "object"
        },
        "DefaultRouteSettings" : {
          "$ref" : "#/definitions/RouteSettings"
        }
      }
    },
    "RouteOverrides" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AuthorizationScopes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Target" : {
          "type" : "string"
        },
        "AuthorizationType" : {
          "type" : "string"
        },
        "AuthorizerId" : {
          "type" : "string"
        },
        "OperationName" : {
          "type" : "string"
        }
      }
    },
    "IntegrationOverrides" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TimeoutInMillis" : {
          "type" : "integer"
        },
        "Description" : {
          "type" : "string"
        },
        "PayloadFormatVersion" : {
          "type" : "string"
        },
        "IntegrationMethod" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "ApiId" ],
  "createOnlyProperties" : [ "/properties/ApiId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}