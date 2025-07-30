SCHEMA = {
  "typeName" : "AWS::Pinpoint::ApplicationSettings",
  "description" : "Resource Type definition for AWS::Pinpoint::ApplicationSettings",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "QuietTime" : {
      "$ref" : "#/definitions/QuietTime"
    },
    "Limits" : {
      "$ref" : "#/definitions/Limits"
    },
    "ApplicationId" : {
      "type" : "string"
    },
    "CampaignHook" : {
      "$ref" : "#/definitions/CampaignHook"
    },
    "CloudWatchMetricsEnabled" : {
      "type" : "boolean"
    }
  },
  "definitions" : {
    "CampaignHook" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Mode" : {
          "type" : "string"
        },
        "WebUrl" : {
          "type" : "string"
        },
        "LambdaFunctionName" : {
          "type" : "string"
        }
      }
    },
    "QuietTime" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Start" : {
          "type" : "string"
        },
        "End" : {
          "type" : "string"
        }
      },
      "required" : [ "Start", "End" ]
    },
    "Limits" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Daily" : {
          "type" : "integer"
        },
        "MaximumDuration" : {
          "type" : "integer"
        },
        "Total" : {
          "type" : "integer"
        },
        "MessagesPerSecond" : {
          "type" : "integer"
        }
      }
    }
  },
  "required" : [ "ApplicationId" ],
  "createOnlyProperties" : [ "/properties/ApplicationId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}