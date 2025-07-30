SCHEMA = {
  "typeName" : "AWS::Cassandra::Table",
  "description" : "Resource schema for AWS::Cassandra::Table",
  "definitions" : {
    "Column" : {
      "type" : "object",
      "properties" : {
        "ColumnName" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$"
        },
        "ColumnType" : {
          "type" : "string"
        }
      },
      "required" : [ "ColumnName", "ColumnType" ],
      "additionalProperties" : False
    },
    "ClusteringKeyColumn" : {
      "type" : "object",
      "properties" : {
        "Column" : {
          "$ref" : "#/definitions/Column"
        },
        "OrderBy" : {
          "type" : "string",
          "enum" : [ "ASC", "DESC" ],
          "default" : "ASC"
        }
      },
      "additionalProperties" : False,
      "required" : [ "Column" ]
    },
    "ProvisionedThroughput" : {
      "description" : "Throughput for the specified table, which consists of values for ReadCapacityUnits and WriteCapacityUnits",
      "type" : "object",
      "properties" : {
        "ReadCapacityUnits" : {
          "type" : "integer",
          "minimum" : 1
        },
        "WriteCapacityUnits" : {
          "type" : "integer",
          "minimum" : 1
        }
      },
      "additionalProperties" : False,
      "required" : [ "ReadCapacityUnits", "WriteCapacityUnits" ]
    },
    "Mode" : {
      "description" : "Capacity mode for the specified table",
      "type" : "string",
      "enum" : [ "PROVISIONED", "ON_DEMAND" ],
      "default" : "ON_DEMAND"
    },
    "BillingMode" : {
      "type" : "object",
      "properties" : {
        "Mode" : {
          "$ref" : "#/definitions/Mode"
        },
        "ProvisionedThroughput" : {
          "$ref" : "#/definitions/ProvisionedThroughput"
        }
      },
      "required" : [ "Mode" ],
      "additionalProperties" : False
    },
    "Tag" : {
      "description" : "A key-value pair to apply to the resource",
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 256
        }
      },
      "required" : [ "Value", "Key" ]
    },
    "EncryptionSpecification" : {
      "description" : "Represents the settings used to enable server-side encryption",
      "type" : "object",
      "properties" : {
        "EncryptionType" : {
          "$ref" : "#/definitions/EncryptionType"
        },
        "KmsKeyIdentifier" : {
          "$ref" : "#/definitions/KmsKeyIdentifier"
        }
      },
      "required" : [ "EncryptionType" ],
      "additionalProperties" : False
    },
    "EncryptionType" : {
      "description" : "Server-side encryption type",
      "type" : "string",
      "enum" : [ "AWS_OWNED_KMS_KEY", "CUSTOMER_MANAGED_KMS_KEY" ],
      "default" : "AWS_OWNED_KMS_KEY"
    },
    "KmsKeyIdentifier" : {
      "description" : "The AWS KMS customer master key (CMK) that should be used for the AWS KMS encryption. To specify a CMK, use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. ",
      "type" : "string"
    },
    "AutoScalingSpecification" : {
      "description" : "Represents the read and write settings used for AutoScaling.",
      "type" : "object",
      "properties" : {
        "WriteCapacityAutoScaling" : {
          "$ref" : "#/definitions/AutoScalingSetting"
        },
        "ReadCapacityAutoScaling" : {
          "$ref" : "#/definitions/AutoScalingSetting"
        }
      },
      "additionalProperties" : False
    },
    "AutoScalingSetting" : {
      "description" : "Represents configuration for auto scaling.",
      "type" : "object",
      "properties" : {
        "AutoScalingDisabled" : {
          "type" : "boolean",
          "default" : False
        },
        "MinimumUnits" : {
          "type" : "integer",
          "minimum" : 1
        },
        "MaximumUnits" : {
          "type" : "integer",
          "minimum" : 1
        },
        "ScalingPolicy" : {
          "$ref" : "#/definitions/ScalingPolicy"
        }
      },
      "additionalProperties" : False
    },
    "ScalingPolicy" : {
      "description" : "Represents scaling policy.",
      "type" : "object",
      "properties" : {
        "TargetTrackingScalingPolicyConfiguration" : {
          "$ref" : "#/definitions/TargetTrackingScalingPolicyConfiguration"
        }
      },
      "additionalProperties" : False
    },
    "TargetTrackingScalingPolicyConfiguration" : {
      "description" : "Represents configuration for target tracking scaling policy.",
      "type" : "object",
      "properties" : {
        "DisableScaleIn" : {
          "type" : "boolean",
          "default" : "False"
        },
        "ScaleInCooldown" : {
          "type" : "integer",
          "default" : 0
        },
        "ScaleOutCooldown" : {
          "type" : "integer",
          "default" : 0
        },
        "TargetValue" : {
          "type" : "integer"
        }
      },
      "required" : [ "TargetValue" ],
      "additionalProperties" : False
    },
    "ReplicaSpecification" : {
      "description" : "Represents replica specifications.",
      "type" : "object",
      "properties" : {
        "Region" : {
          "type" : "string",
          "minLength" : 2,
          "maxLength" : 25
        },
        "ReadCapacityUnits" : {
          "type" : "integer"
        },
        "ReadCapacityAutoScaling" : {
          "$ref" : "#/definitions/AutoScalingSetting"
        }
      },
      "required" : [ "Region" ],
      "additionalProperties" : False
    }
  },
  "properties" : {
    "KeyspaceName" : {
      "description" : "Name for Cassandra keyspace",
      "type" : "string",
      "pattern" : "^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$"
    },
    "TableName" : {
      "description" : "Name for Cassandra table",
      "type" : "string",
      "pattern" : "^[a-zA-Z0-9][a-zA-Z0-9_]{1,47}$"
    },
    "RegularColumns" : {
      "description" : "Non-key columns of the table",
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Column"
      }
    },
    "PartitionKeyColumns" : {
      "description" : "Partition key columns of the table",
      "type" : "array",
      "minItems" : 1,
      "uniqueItems" : True,
      "insertionOrder" : True,
      "items" : {
        "$ref" : "#/definitions/Column"
      }
    },
    "ClusteringKeyColumns" : {
      "description" : "Clustering key columns of the table",
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : True,
      "items" : {
        "$ref" : "#/definitions/ClusteringKeyColumn"
      }
    },
    "BillingMode" : {
      "$ref" : "#/definitions/BillingMode"
    },
    "PointInTimeRecoveryEnabled" : {
      "description" : "Indicates whether point in time recovery is enabled (True) or disabled (False) on the table",
      "type" : "boolean"
    },
    "ClientSideTimestampsEnabled" : {
      "description" : "Indicates whether client side timestamps are enabled (True) or disabled (False) on the table. False by default, once it is enabled it cannot be disabled again.",
      "type" : "boolean"
    },
    "Tags" : {
      "description" : "An array of key-value pairs to apply to this resource",
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "minItems" : 0,
      "maxItems" : 50
    },
    "DefaultTimeToLive" : {
      "description" : "Default TTL (Time To Live) in seconds, where zero is disabled. If the value is greater than zero, TTL is enabled for the entire table and an expiration timestamp is added to each column.",
      "type" : "integer",
      "minimum" : 0
    },
    "EncryptionSpecification" : {
      "$ref" : "#/definitions/EncryptionSpecification"
    },
    "AutoScalingSpecifications" : {
      "$ref" : "#/definitions/AutoScalingSpecification"
    },
    "ReplicaSpecifications" : {
      "type" : "array",
      "minItems" : 1,
      "uniqueItems" : True,
      "insertionOrder" : True,
      "items" : {
        "$ref" : "#/definitions/ReplicaSpecification"
      }
    }
  },
  "additionalProperties" : False,
  "required" : [ "KeyspaceName", "PartitionKeyColumns" ],
  "createOnlyProperties" : [ "/properties/KeyspaceName", "/properties/TableName", "/properties/PartitionKeyColumns", "/properties/ClusteringKeyColumns", "/properties/ClientSideTimestampsEnabled" ],
  "writeOnlyProperties" : [ "/properties/AutoScalingSpecifications", "/properties/ReplicaSpecifications" ],
  "primaryIdentifier" : [ "/properties/KeyspaceName", "/properties/TableName" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "cassandra:TagResource", "cassandra:TagMultiRegionResource", "cassandra:UntagResource", "cassandra:UntagMultiRegionResource" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "cassandra:Create", "cassandra:CreateMultiRegionResource", "cassandra:Select", "cassandra:SelectMultiRegionResource", "cassandra:TagResource", "cassandra:TagMultiRegionResource", "kms:CreateGrant", "kms:DescribeKey", "kms:Encrypt", "kms:Decrypt", "application-autoscaling:DescribeScalableTargets", "application-autoscaling:DescribeScalingPolicies", "application-autoscaling:DeregisterScalableTarget", "application-autoscaling:RegisterScalableTarget", "application-autoscaling:PutScalingPolicy", "cloudwatch:DeleteAlarms", "cloudwatch:DescribeAlarms", "cloudwatch:GetMetricData", "cloudwatch:PutMetricAlarm" ]
    },
    "read" : {
      "permissions" : [ "cassandra:Select", "cassandra:SelectMultiRegionResource", "application-autoscaling:DescribeScalableTargets", "application-autoscaling:DescribeScalingPolicies", "application-autoscaling:DeregisterScalableTarget", "application-autoscaling:RegisterScalableTarget", "application-autoscaling:PutScalingPolicy", "cloudwatch:DeleteAlarms", "cloudwatch:DescribeAlarms", "cloudwatch:GetMetricData", "cloudwatch:PutMetricAlarm" ]
    },
    "update" : {
      "permissions" : [ "cassandra:Alter", "cassandra:AlterMultiRegionResource", "cassandra:Select", "cassandra:SelectMultiRegionResource", "cassandra:TagResource", "cassandra:TagMultiRegionResource", "cassandra:UntagResource", "cassandra:UntagMultiRegionResource", "kms:CreateGrant", "kms:DescribeKey", "kms:Encrypt", "kms:Decrypt", "application-autoscaling:DescribeScalableTargets", "application-autoscaling:DescribeScalingPolicies", "application-autoscaling:DeregisterScalableTarget", "application-autoscaling:RegisterScalableTarget", "application-autoscaling:PutScalingPolicy", "cloudwatch:DeleteAlarms", "cloudwatch:DescribeAlarms", "cloudwatch:GetMetricData", "cloudwatch:PutMetricAlarm" ]
    },
    "delete" : {
      "permissions" : [ "cassandra:Drop", "cassandra:DropMultiRegionResource", "cassandra:Select", "cassandra:SelectMultiRegionResource", "application-autoscaling:DescribeScalableTargets", "application-autoscaling:DescribeScalingPolicies", "application-autoscaling:DeregisterScalableTarget", "application-autoscaling:RegisterScalableTarget", "application-autoscaling:PutScalingPolicy", "cloudwatch:DeleteAlarms", "cloudwatch:DescribeAlarms", "cloudwatch:GetMetricData", "cloudwatch:PutMetricAlarm" ]
    },
    "list" : {
      "permissions" : [ "cassandra:Select", "cassandra:SelectMultiRegionResource", "application-autoscaling:DescribeScalableTargets", "application-autoscaling:DescribeScalingPolicies", "application-autoscaling:DeregisterScalableTarget", "application-autoscaling:RegisterScalableTarget", "application-autoscaling:PutScalingPolicy", "cloudwatch:DeleteAlarms", "cloudwatch:DescribeAlarms", "cloudwatch:GetMetricData", "cloudwatch:PutMetricAlarm" ]
    }
  },
  "propertyTransform" : {
    "/properties/ClusteringKeyColumns/*/Column/ColumnType" : "$lowercase(ColumnType)",
    "/properties/PartitionKeyColumns/*/ColumnType" : "$lowercase(ColumnType)",
    "/properties/RegularColumns/*/ColumnType" : "$lowercase(ColumnType)"
  }
}