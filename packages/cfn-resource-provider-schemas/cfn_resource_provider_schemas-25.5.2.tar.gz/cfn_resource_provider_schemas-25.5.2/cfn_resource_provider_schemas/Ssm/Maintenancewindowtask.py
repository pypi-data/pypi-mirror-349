SCHEMA = {
  "typeName" : "AWS::SSM::MaintenanceWindowTask",
  "description" : "Resource Type definition for AWS::SSM::MaintenanceWindowTask",
  "additionalProperties" : False,
  "properties" : {
    "MaxErrors" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    },
    "ServiceRoleArn" : {
      "type" : "string"
    },
    "Priority" : {
      "type" : "integer"
    },
    "MaxConcurrency" : {
      "type" : "string"
    },
    "Targets" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Target"
      }
    },
    "Name" : {
      "type" : "string"
    },
    "TaskArn" : {
      "type" : "string"
    },
    "TaskInvocationParameters" : {
      "$ref" : "#/definitions/TaskInvocationParameters"
    },
    "WindowId" : {
      "type" : "string"
    },
    "TaskParameters" : {
      "type" : "object"
    },
    "TaskType" : {
      "type" : "string"
    },
    "CutoffBehavior" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "LoggingInfo" : {
      "$ref" : "#/definitions/LoggingInfo"
    }
  },
  "definitions" : {
    "TaskInvocationParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaintenanceWindowStepFunctionsParameters" : {
          "$ref" : "#/definitions/MaintenanceWindowStepFunctionsParameters"
        },
        "MaintenanceWindowRunCommandParameters" : {
          "$ref" : "#/definitions/MaintenanceWindowRunCommandParameters"
        },
        "MaintenanceWindowLambdaParameters" : {
          "$ref" : "#/definitions/MaintenanceWindowLambdaParameters"
        },
        "MaintenanceWindowAutomationParameters" : {
          "$ref" : "#/definitions/MaintenanceWindowAutomationParameters"
        }
      }
    },
    "Target" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Values" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Values", "Key" ]
    },
    "CloudWatchOutputConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CloudWatchOutputEnabled" : {
          "type" : "boolean"
        },
        "CloudWatchLogGroupName" : {
          "type" : "string"
        }
      }
    },
    "MaintenanceWindowRunCommandParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TimeoutSeconds" : {
          "type" : "integer"
        },
        "Comment" : {
          "type" : "string"
        },
        "OutputS3KeyPrefix" : {
          "type" : "string"
        },
        "Parameters" : {
          "type" : "object"
        },
        "CloudWatchOutputConfig" : {
          "$ref" : "#/definitions/CloudWatchOutputConfig"
        },
        "DocumentHashType" : {
          "type" : "string"
        },
        "ServiceRoleArn" : {
          "type" : "string"
        },
        "NotificationConfig" : {
          "$ref" : "#/definitions/NotificationConfig"
        },
        "DocumentVersion" : {
          "type" : "string"
        },
        "OutputS3BucketName" : {
          "type" : "string"
        },
        "DocumentHash" : {
          "type" : "string"
        }
      }
    },
    "MaintenanceWindowAutomationParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Parameters" : {
          "type" : "object"
        },
        "DocumentVersion" : {
          "type" : "string"
        }
      }
    },
    "NotificationConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "NotificationEvents" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "NotificationArn" : {
          "type" : "string"
        },
        "NotificationType" : {
          "type" : "string"
        }
      },
      "required" : [ "NotificationArn" ]
    },
    "MaintenanceWindowStepFunctionsParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Input" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      }
    },
    "LoggingInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Region" : {
          "type" : "string"
        },
        "S3Prefix" : {
          "type" : "string"
        },
        "S3Bucket" : {
          "type" : "string"
        }
      },
      "required" : [ "S3Bucket", "Region" ]
    },
    "MaintenanceWindowLambdaParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Qualifier" : {
          "type" : "string"
        },
        "Payload" : {
          "type" : "string"
        },
        "ClientContext" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "WindowId", "Priority", "TaskType", "TaskArn" ],
  "createOnlyProperties" : [ "/properties/WindowId", "/properties/TaskType" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}