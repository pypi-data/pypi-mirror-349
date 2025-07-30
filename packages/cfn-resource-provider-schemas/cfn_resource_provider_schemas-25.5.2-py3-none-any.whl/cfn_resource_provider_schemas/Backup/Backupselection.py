SCHEMA = {
  "typeName" : "AWS::Backup::BackupSelection",
  "description" : "Resource Type definition for AWS::Backup::BackupSelection",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "BackupPlanId" : {
      "type" : "string"
    },
    "BackupSelection" : {
      "$ref" : "#/definitions/BackupSelectionResourceType"
    },
    "SelectionId" : {
      "type" : "string"
    }
  },
  "required" : [ "BackupSelection", "BackupPlanId" ],
  "createOnlyProperties" : [ "/properties/BackupSelection", "/properties/BackupPlanId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/SelectionId", "/properties/Id" ],
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "additionalProperties" : False,
  "definitions" : {
    "BackupSelectionResourceType" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IamRoleArn" : {
          "type" : "string"
        },
        "ListOfTags" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/ConditionResourceType"
          }
        },
        "Resources" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        },
        "SelectionName" : {
          "type" : "string"
        },
        "NotResources" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Conditions" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "StringEquals" : {
              "type" : "array",
              "uniqueItems" : False,
              "insertionOrder" : False,
              "items" : {
                "$ref" : "#/definitions/ConditionParameter"
              }
            },
            "StringNotEquals" : {
              "type" : "array",
              "uniqueItems" : False,
              "insertionOrder" : False,
              "items" : {
                "$ref" : "#/definitions/ConditionParameter"
              }
            },
            "StringLike" : {
              "type" : "array",
              "uniqueItems" : False,
              "insertionOrder" : False,
              "items" : {
                "$ref" : "#/definitions/ConditionParameter"
              }
            },
            "StringNotLike" : {
              "type" : "array",
              "uniqueItems" : False,
              "insertionOrder" : False,
              "items" : {
                "$ref" : "#/definitions/ConditionParameter"
              }
            }
          }
        }
      },
      "required" : [ "SelectionName", "IamRoleArn" ]
    },
    "ConditionParameter" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ConditionKey" : {
          "type" : "string"
        },
        "ConditionValue" : {
          "type" : "string"
        }
      }
    },
    "ConditionResourceType" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ConditionKey" : {
          "type" : "string"
        },
        "ConditionValue" : {
          "type" : "string"
        },
        "ConditionType" : {
          "type" : "string"
        }
      },
      "required" : [ "ConditionValue", "ConditionKey", "ConditionType" ]
    }
  },
  "handlers" : {
    "delete" : {
      "permissions" : [ "backup:GetBackupSelection", "backup:DeleteBackupSelection" ]
    },
    "read" : {
      "permissions" : [ "backup:GetBackupSelection" ]
    },
    "create" : {
      "permissions" : [ "backup:CreateBackupSelection", "iam:GetRole", "iam:PassRole", "iam:CreateServiceLinkedRole" ]
    },
    "list" : {
      "permissions" : [ "backup:ListBackupSelections", "backup:ListBackupPlans" ]
    }
  }
}