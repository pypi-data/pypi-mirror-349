SCHEMA = {
  "typeName" : "AWS::Backup::BackupPlan",
  "description" : "Resource Type definition for AWS::Backup::BackupPlan",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "properties" : {
    "BackupPlan" : {
      "$ref" : "#/definitions/BackupPlanResourceType"
    },
    "BackupPlanTags" : {
      "type" : "object",
      "additionalProperties" : False,
      "patternProperties" : {
        "^.{1,128}$" : {
          "type" : "string"
        }
      }
    },
    "BackupPlanArn" : {
      "type" : "string"
    },
    "BackupPlanId" : {
      "type" : "string"
    },
    "VersionId" : {
      "type" : "string"
    }
  },
  "additionalProperties" : False,
  "required" : [ "BackupPlan" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/BackupPlanTags",
    "permissions" : [ "backup:TagResource", "backup:UntagResource", "backup:ListTags" ]
  },
  "readOnlyProperties" : [ "/properties/BackupPlanId", "/properties/VersionId", "/properties/BackupPlanArn" ],
  "primaryIdentifier" : [ "/properties/BackupPlanId" ],
  "definitions" : {
    "BackupPlanResourceType" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "BackupPlanName" : {
          "type" : "string"
        },
        "AdvancedBackupSettings" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/AdvancedBackupSettingResourceType"
          }
        },
        "BackupPlanRule" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/BackupRuleResourceType"
          }
        }
      },
      "required" : [ "BackupPlanName", "BackupPlanRule" ]
    },
    "BackupRuleResourceType" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RuleName" : {
          "type" : "string"
        },
        "TargetBackupVault" : {
          "type" : "string"
        },
        "StartWindowMinutes" : {
          "type" : "number"
        },
        "CompletionWindowMinutes" : {
          "type" : "number"
        },
        "ScheduleExpression" : {
          "type" : "string"
        },
        "ScheduleExpressionTimezone" : {
          "type" : "string"
        },
        "IndexActions" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/IndexActionsResourceType"
          }
        },
        "RecoveryPointTags" : {
          "type" : "object",
          "additionalProperties" : False,
          "patternProperties" : {
            "^.{1,128}$" : {
              "type" : "string"
            }
          }
        },
        "CopyActions" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/CopyActionResourceType"
          }
        },
        "Lifecycle" : {
          "$ref" : "#/definitions/LifecycleResourceType"
        },
        "EnableContinuousBackup" : {
          "type" : "boolean"
        }
      },
      "required" : [ "TargetBackupVault", "RuleName" ]
    },
    "AdvancedBackupSettingResourceType" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "BackupOptions" : {
          "type" : "object"
        },
        "ResourceType" : {
          "type" : "string"
        }
      },
      "required" : [ "BackupOptions", "ResourceType" ]
    },
    "CopyActionResourceType" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Lifecycle" : {
          "$ref" : "#/definitions/LifecycleResourceType"
        },
        "DestinationBackupVaultArn" : {
          "type" : "string"
        }
      },
      "required" : [ "DestinationBackupVaultArn" ]
    },
    "IndexActionsResourceType" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ResourceTypes" : {
          "$ref" : "#/definitions/ResourceTypes"
        }
      }
    },
    "ResourceTypes" : {
      "type" : "array",
      "insertionOrder" : True,
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/ResourceType"
      }
    },
    "ResourceType" : {
      "type" : "string"
    },
    "LifecycleResourceType" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MoveToColdStorageAfterDays" : {
          "type" : "number"
        },
        "DeleteAfterDays" : {
          "type" : "number"
        },
        "OptInToArchiveForSupportedResources" : {
          "type" : "boolean"
        }
      }
    }
  },
  "handlers" : {
    "read" : {
      "permissions" : [ "backup:GetBackupPlan", "backup:ListTags" ]
    },
    "create" : {
      "permissions" : [ "backup:GetBackupPlan", "backup:TagResource", "backup:CreateBackupPlan" ]
    },
    "delete" : {
      "permissions" : [ "backup:GetBackupPlan", "backup:DeleteBackupPlan" ]
    },
    "update" : {
      "permissions" : [ "backup:UpdateBackupPlan", "backup:ListTags", "backup:TagResource", "backup:UntagResource" ]
    },
    "list" : {
      "permissions" : [ "backup:ListBackupPlans" ]
    }
  }
}