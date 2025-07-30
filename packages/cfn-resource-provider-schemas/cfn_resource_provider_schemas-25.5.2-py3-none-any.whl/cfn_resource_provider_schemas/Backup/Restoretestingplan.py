SCHEMA = {
  "tagging" : {
    "permissions" : [ "backup:TagResource", "backup:UntagResource", "backup:ListTags" ],
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "tagProperty" : "/properties/Tags",
    "cloudFormationSystemTags" : True
  },
  "handlers" : {
    "read" : {
      "permissions" : [ "backup:GetRestoreTestingPlan", "backup:ListTags" ],
      "timeoutInMinutes" : 5
    },
    "create" : {
      "permissions" : [ "backup:CreateRestoreTestingPlan", "backup:TagResource", "backup:GetRestoreTestingPlan", "backup:ListTags" ],
      "timeoutInMinutes" : 5
    },
    "update" : {
      "permissions" : [ "backup:UpdateRestoreTestingPlan", "backup:TagResource", "backup:UntagResource", "backup:GetRestoreTestingPlan", "backup:ListTags" ],
      "timeoutInMinutes" : 5
    },
    "list" : {
      "permissions" : [ "backup:ListRestoreTestingPlans" ],
      "timeoutInMinutes" : 5
    },
    "delete" : {
      "permissions" : [ "backup:DeleteRestoreTestingPlan", "backup:GetRestoreTestingPlan" ],
      "timeoutInMinutes" : 5
    }
  },
  "typeName" : "AWS::Backup::RestoreTestingPlan",
  "readOnlyProperties" : [ "/properties/RestoreTestingPlanArn" ],
  "description" : "Definition of AWS::Backup::RestoreTestingPlan Resource Type",
  "createOnlyProperties" : [ "/properties/RestoreTestingPlanName" ],
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/RestoreTestingPlanName" ],
  "definitions" : {
    "RestoreTestingRecoveryPointSelection" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SelectionWindowDays" : {
          "type" : "integer"
        },
        "RecoveryPointTypes" : {
          "insertionOrder" : False,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/RestoreTestingRecoveryPointType"
          }
        },
        "IncludeVaults" : {
          "insertionOrder" : False,
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "ExcludeVaults" : {
          "insertionOrder" : False,
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "Algorithm" : {
          "$ref" : "#/definitions/RestoreTestingRecoveryPointSelectionAlgorithm"
        }
      },
      "required" : [ "Algorithm", "RecoveryPointTypes", "IncludeVaults" ]
    },
    "Tag" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "minLength" : 0,
          "description" : "The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.",
          "type" : "string",
          "maxLength" : 256
        },
        "Key" : {
          "minLength" : 1,
          "description" : "The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.",
          "type" : "string",
          "maxLength" : 128
        }
      },
      "required" : [ "Key", "Value" ]
    },
    "RestoreTestingRecoveryPointSelectionAlgorithm" : {
      "type" : "string",
      "enum" : [ "LATEST_WITHIN_WINDOW", "RANDOM_WITHIN_WINDOW" ]
    },
    "RestoreTestingRecoveryPointType" : {
      "type" : "string",
      "enum" : [ "SNAPSHOT", "CONTINUOUS" ]
    }
  },
  "required" : [ "RecoveryPointSelection", "ScheduleExpression", "RestoreTestingPlanName" ],
  "properties" : {
    "ScheduleExpression" : {
      "type" : "string"
    },
    "StartWindowHours" : {
      "type" : "integer"
    },
    "RecoveryPointSelection" : {
      "$ref" : "#/definitions/RestoreTestingRecoveryPointSelection"
    },
    "RestoreTestingPlanArn" : {
      "type" : "string"
    },
    "RestoreTestingPlanName" : {
      "type" : "string"
    },
    "ScheduleExpressionTimezone" : {
      "type" : "string"
    },
    "Tags" : {
      "uniqueItems" : True,
      "insertionOrder" : False,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  }
}