SCHEMA = {
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "tagging" : {
    "permissions" : [ "backup:TagResource", "backup:UntagResource", "backup:ListTags" ],
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "tagProperty" : "/properties/BackupVaultTags",
    "cloudFormationSystemTags" : True
  },
  "handlers" : {
    "read" : {
      "permissions" : [ "backup:DescribeBackupVault", "backup:GetBackupVaultNotifications", "backup:GetBackupVaultAccessPolicy", "backup:ListTags" ]
    },
    "create" : {
      "permissions" : [ "backup:TagResource", "backup:CreateLogicallyAirGappedBackupVault", "backup:PutBackupVaultAccessPolicy", "backup:PutBackupVaultNotifications", "backup-storage:Mount", "backup-storage:MountCapsule", "backup:DescribeBackupVault" ]
    },
    "update" : {
      "permissions" : [ "backup:DescribeBackupVault", "backup:DeleteBackupVaultAccessPolicy", "backup:DeleteBackupVaultNotifications", "backup:DeleteBackupVaultLockConfiguration", "backup:GetBackupVaultAccessPolicy", "backup:ListTags", "backup:TagResource", "backup:UntagResource", "backup:PutBackupVaultAccessPolicy", "backup:PutBackupVaultNotifications", "backup:PutBackupVaultLockConfiguration" ]
    },
    "list" : {
      "permissions" : [ "backup:ListBackupVaults" ]
    },
    "delete" : {
      "permissions" : [ "backup:DeleteBackupVault" ]
    }
  },
  "typeName" : "AWS::Backup::LogicallyAirGappedBackupVault",
  "readOnlyProperties" : [ "/properties/BackupVaultArn", "/properties/EncryptionKeyArn", "/properties/VaultState", "/properties/VaultType" ],
  "description" : "Resource Type definition for AWS::Backup::LogicallyAirGappedBackupVault",
  "createOnlyProperties" : [ "/properties/BackupVaultName", "/properties/MinRetentionDays", "/properties/MaxRetentionDays" ],
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/BackupVaultName" ],
  "definitions" : {
    "NotificationObjectType" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SNSTopicArn" : {
          "type" : "string"
        },
        "BackupVaultEvents" : {
          "uniqueItems" : False,
          "insertionOrder" : False,
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "SNSTopicArn", "BackupVaultEvents" ]
    },
    "BackupVaultNamePattern" : {
      "pattern" : "^[a-zA-Z0-9\\-\\_]{2,50}$",
      "type" : "string"
    }
  },
  "required" : [ "BackupVaultName", "MinRetentionDays", "MaxRetentionDays" ],
  "properties" : {
    "VaultState" : {
      "type" : "string"
    },
    "BackupVaultTags" : {
      "patternProperties" : {
        "^.{1,128}$" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False,
      "type" : "object"
    },
    "VaultType" : {
      "type" : "string"
    },
    "BackupVaultName" : {
      "$ref" : "#/definitions/BackupVaultNamePattern"
    },
    "BackupVaultArn" : {
      "type" : "string"
    },
    "EncryptionKeyArn" : {
      "type" : "string"
    },
    "MaxRetentionDays" : {
      "type" : "integer"
    },
    "MinRetentionDays" : {
      "type" : "integer"
    },
    "Notifications" : {
      "$ref" : "#/definitions/NotificationObjectType"
    },
    "AccessPolicy" : {
      "type" : [ "object", "string" ]
    }
  }
}