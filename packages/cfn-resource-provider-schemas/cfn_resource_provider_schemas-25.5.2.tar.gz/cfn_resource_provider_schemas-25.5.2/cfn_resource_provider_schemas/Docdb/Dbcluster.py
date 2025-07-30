SCHEMA = {
  "typeName" : "AWS::DocDB::DBCluster",
  "description" : "Resource Type definition for AWS::DocDB::DBCluster",
  "additionalProperties" : False,
  "properties" : {
    "StorageEncrypted" : {
      "type" : "boolean"
    },
    "RestoreToTime" : {
      "type" : "string"
    },
    "SnapshotIdentifier" : {
      "type" : "string"
    },
    "Port" : {
      "type" : "integer"
    },
    "DBClusterIdentifier" : {
      "type" : "string"
    },
    "PreferredBackupWindow" : {
      "type" : "string"
    },
    "ClusterResourceId" : {
      "type" : "string"
    },
    "Endpoint" : {
      "type" : "string"
    },
    "RotateMasterUserPassword" : {
      "type" : "boolean"
    },
    "VpcSecurityGroupIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "CopyTagsToSnapshot" : {
      "type" : "boolean"
    },
    "RestoreType" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "EngineVersion" : {
      "type" : "string"
    },
    "StorageType" : {
      "type" : "string"
    },
    "KmsKeyId" : {
      "type" : "string"
    },
    "AvailabilityZones" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "ServerlessV2ScalingConfiguration" : {
      "$ref" : "#/definitions/ServerlessV2ScalingConfiguration"
    },
    "PreferredMaintenanceWindow" : {
      "type" : "string"
    },
    "MasterUserSecretKmsKeyId" : {
      "type" : "string"
    },
    "DBSubnetGroupName" : {
      "type" : "string"
    },
    "DeletionProtection" : {
      "type" : "boolean"
    },
    "UseLatestRestorableTime" : {
      "type" : "boolean"
    },
    "ManageMasterUserPassword" : {
      "type" : "boolean"
    },
    "MasterUserPassword" : {
      "type" : "string"
    },
    "SourceDBClusterIdentifier" : {
      "type" : "string"
    },
    "MasterUsername" : {
      "type" : "string"
    },
    "ReadEndpoint" : {
      "type" : "string"
    },
    "DBClusterParameterGroupName" : {
      "type" : "string"
    },
    "BackupRetentionPeriod" : {
      "type" : "integer"
    },
    "Id" : {
      "type" : "string"
    },
    "EnableCloudwatchLogsExports" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    }
  },
  "definitions" : {
    "ServerlessV2ScalingConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MinCapacity" : {
          "type" : "number"
        },
        "MaxCapacity" : {
          "type" : "number"
        }
      },
      "required" : [ "MinCapacity", "MaxCapacity" ]
    },
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    }
  },
  "createOnlyProperties" : [ "/properties/SnapshotIdentifier", "/properties/KmsKeyId", "/properties/MasterUsername", "/properties/SourceDBClusterIdentifier", "/properties/DBClusterIdentifier", "/properties/AvailabilityZones", "/properties/DBSubnetGroupName", "/properties/StorageEncrypted" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/ReadEndpoint", "/properties/Id", "/properties/Endpoint", "/properties/ClusterResourceId" ]
}