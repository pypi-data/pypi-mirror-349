SCHEMA = {
  "typeName" : "AWS::Config::RemediationConfiguration",
  "description" : "Resource Type definition for AWS::Config::RemediationConfiguration",
  "additionalProperties" : False,
  "properties" : {
    "TargetVersion" : {
      "type" : "string"
    },
    "ExecutionControls" : {
      "$ref" : "#/definitions/ExecutionControls"
    },
    "Parameters" : {
      "type" : "object"
    },
    "TargetType" : {
      "type" : "string"
    },
    "ConfigRuleName" : {
      "type" : "string"
    },
    "ResourceType" : {
      "type" : "string"
    },
    "RetryAttemptSeconds" : {
      "type" : "integer"
    },
    "MaximumAutomaticAttempts" : {
      "type" : "integer"
    },
    "Id" : {
      "type" : "string"
    },
    "TargetId" : {
      "type" : "string"
    },
    "Automatic" : {
      "type" : "boolean"
    }
  },
  "definitions" : {
    "ExecutionControls" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SsmControls" : {
          "$ref" : "#/definitions/SsmControls"
        }
      }
    },
    "SsmControls" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ErrorPercentage" : {
          "type" : "integer"
        },
        "ConcurrentExecutionRatePercentage" : {
          "type" : "integer"
        }
      }
    }
  },
  "required" : [ "TargetType", "ConfigRuleName", "TargetId" ],
  "createOnlyProperties" : [ "/properties/ConfigRuleName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}