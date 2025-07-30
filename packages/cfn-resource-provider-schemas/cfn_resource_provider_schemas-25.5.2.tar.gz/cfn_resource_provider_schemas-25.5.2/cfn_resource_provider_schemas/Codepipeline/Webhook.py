SCHEMA = {
  "typeName" : "AWS::CodePipeline::Webhook",
  "description" : "Resource Type definition for AWS::CodePipeline::Webhook",
  "additionalProperties" : False,
  "properties" : {
    "AuthenticationConfiguration" : {
      "$ref" : "#/definitions/WebhookAuthConfiguration"
    },
    "Filters" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/WebhookFilterRule"
      }
    },
    "Authentication" : {
      "type" : "string"
    },
    "TargetPipeline" : {
      "type" : "string"
    },
    "TargetAction" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "Url" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    },
    "TargetPipelineVersion" : {
      "type" : "integer"
    },
    "RegisterWithThirdParty" : {
      "type" : "boolean"
    }
  },
  "definitions" : {
    "WebhookFilterRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "JsonPath" : {
          "type" : "string"
        },
        "MatchEquals" : {
          "type" : "string"
        }
      },
      "required" : [ "JsonPath" ]
    },
    "WebhookAuthConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AllowedIPRange" : {
          "type" : "string"
        },
        "SecretToken" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "AuthenticationConfiguration", "Filters", "Authentication", "TargetPipeline", "TargetAction", "TargetPipelineVersion" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Url" ]
}