SCHEMA = {
  "handlers" : {
    "read" : {
      "permissions" : [ "dynamodb:Describe*", "dynamodb:GetResourcePolicy", "application-autoscaling:Describe*", "cloudwatch:PutMetricData", "dynamodb:ListTagsOfResource", "kms:DescribeKey" ]
    },
    "create" : {
      "permissions" : [ "dynamodb:CreateTable", "dynamodb:CreateTableReplica", "dynamodb:Describe*", "dynamodb:UpdateTimeToLive", "dynamodb:UpdateContributorInsights", "dynamodb:UpdateContinuousBackups", "dynamodb:ListTagsOfResource", "dynamodb:Query", "dynamodb:Scan", "dynamodb:UpdateItem", "dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:DeleteItem", "dynamodb:BatchWriteItem", "dynamodb:TagResource", "dynamodb:EnableKinesisStreamingDestination", "dynamodb:DisableKinesisStreamingDestination", "dynamodb:UpdateTableReplicaAutoScaling", "dynamodb:TagResource", "dynamodb:GetResourcePolicy", "dynamodb:PutResourcePolicy", "application-autoscaling:DeleteScalingPolicy", "application-autoscaling:DeleteScheduledAction", "application-autoscaling:DeregisterScalableTarget", "application-autoscaling:Describe*", "application-autoscaling:PutScalingPolicy", "application-autoscaling:PutScheduledAction", "application-autoscaling:RegisterScalableTarget", "kinesis:ListStreams", "kinesis:DescribeStream", "kinesis:PutRecords", "kms:CreateGrant", "kms:DescribeKey", "kms:ListAliases", "kms:Decrypt", "kms:RevokeGrant", "cloudwatch:PutMetricData", "iam:CreateServiceLinkedRole" ]
    },
    "update" : {
      "permissions" : [ "dynamodb:Describe*", "dynamodb:CreateTableReplica", "dynamodb:UpdateTable", "dynamodb:UpdateTimeToLive", "dynamodb:UpdateContinuousBackups", "dynamodb:UpdateContributorInsights", "dynamodb:ListTagsOfResource", "dynamodb:Query", "dynamodb:Scan", "dynamodb:UpdateItem", "dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:DeleteItem", "dynamodb:BatchWriteItem", "dynamodb:DeleteTable", "dynamodb:DeleteTableReplica", "dynamodb:UpdateItem", "dynamodb:TagResource", "dynamodb:UntagResource", "dynamodb:EnableKinesisStreamingDestination", "dynamodb:DisableKinesisStreamingDestination", "dynamodb:UpdateTableReplicaAutoScaling", "dynamodb:UpdateKinesisStreamingDestination", "dynamodb:GetResourcePolicy", "dynamodb:PutResourcePolicy", "dynamodb:DeleteResourcePolicy", "application-autoscaling:DeleteScalingPolicy", "application-autoscaling:DeleteScheduledAction", "application-autoscaling:DeregisterScalableTarget", "application-autoscaling:Describe*", "application-autoscaling:PutScalingPolicy", "application-autoscaling:PutScheduledAction", "application-autoscaling:RegisterScalableTarget", "kinesis:ListStreams", "kinesis:DescribeStream", "kinesis:PutRecords", "kms:CreateGrant", "kms:DescribeKey", "kms:ListAliases", "kms:RevokeGrant", "cloudwatch:PutMetricData" ],
      "timeoutInMinutes" : 1200
    },
    "list" : {
      "permissions" : [ "dynamodb:ListTables", "cloudwatch:PutMetricData" ]
    },
    "delete" : {
      "permissions" : [ "dynamodb:Describe*", "dynamodb:DeleteTable", "application-autoscaling:DeleteScalingPolicy", "application-autoscaling:DeleteScheduledAction", "application-autoscaling:DeregisterScalableTarget", "application-autoscaling:Describe*", "application-autoscaling:PutScalingPolicy", "application-autoscaling:PutScheduledAction", "application-autoscaling:RegisterScalableTarget" ]
    }
  },
  "typeName" : "AWS::DynamoDB::GlobalTable",
  "readOnlyProperties" : [ "/properties/Arn", "/properties/StreamArn", "/properties/TableId" ],
  "description" : "Version: None. Resource Type definition for AWS::DynamoDB::GlobalTable",
  "additionalIdentifiers" : [ [ "/properties/Arn" ], [ "/properties/StreamArn" ] ],
  "writeOnlyProperties" : [ "/properties/Replicas/*/ReadProvisionedThroughputSettings/ReadCapacityAutoScalingSettings/SeedCapacity", "/properties/Replicas/*/GlobalSecondaryIndexes/*/ReadProvisionedThroughputSettings/ReadCapacityAutoScalingSettings/SeedCapacity", "/properties/WriteProvisionedThroughputSettings/WriteCapacityAutoScalingSettings/SeedCapacity", "/properties/GlobalSecondaryIndexes/*/WriteProvisionedThroughputSettings/WriteCapacityAutoScalingSettings/SeedCapacity" ],
  "createOnlyProperties" : [ "/properties/LocalSecondaryIndexes", "/properties/TableName", "/properties/KeySchema" ],
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/TableName" ],
  "definitions" : {
    "LocalSecondaryIndex" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "IndexName" : {
          "minLength" : 3,
          "type" : "string",
          "maxLength" : 255
        },
        "Projection" : {
          "$ref" : "#/definitions/Projection"
        },
        "KeySchema" : {
          "maxItems" : 2,
          "uniqueItems" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/KeySchema"
          }
        }
      },
      "required" : [ "IndexName", "Projection", "KeySchema" ]
    },
    "ReplicaSpecification" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SSESpecification" : {
          "$ref" : "#/definitions/ReplicaSSESpecification"
        },
        "KinesisStreamSpecification" : {
          "$ref" : "#/definitions/KinesisStreamSpecification"
        },
        "ContributorInsightsSpecification" : {
          "$ref" : "#/definitions/ContributorInsightsSpecification"
        },
        "PointInTimeRecoverySpecification" : {
          "$ref" : "#/definitions/PointInTimeRecoverySpecification"
        },
        "ReplicaStreamSpecification" : {
          "$ref" : "#/definitions/ReplicaStreamSpecification"
        },
        "GlobalSecondaryIndexes" : {
          "uniqueItems" : True,
          "insertionOrder" : False,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ReplicaGlobalSecondaryIndexSpecification"
          }
        },
        "Region" : {
          "type" : "string"
        },
        "ResourcePolicy" : {
          "$ref" : "#/definitions/ResourcePolicy"
        },
        "ReadProvisionedThroughputSettings" : {
          "$ref" : "#/definitions/ReadProvisionedThroughputSettings"
        },
        "TableClass" : {
          "type" : "string"
        },
        "DeletionProtectionEnabled" : {
          "type" : "boolean"
        },
        "Tags" : {
          "uniqueItems" : True,
          "insertionOrder" : False,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Tag"
          }
        },
        "ReadOnDemandThroughputSettings" : {
          "$ref" : "#/definitions/ReadOnDemandThroughputSettings"
        }
      },
      "required" : [ "Region" ]
    },
    "AttributeDefinition" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AttributeType" : {
          "type" : "string"
        },
        "AttributeName" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 255
        }
      },
      "required" : [ "AttributeName", "AttributeType" ]
    },
    "Projection" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "NonKeyAttributes" : {
          "maxItems" : 20,
          "uniqueItems" : True,
          "insertionOrder" : False,
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "ProjectionType" : {
          "type" : "string"
        }
      }
    },
    "PointInTimeRecoverySpecification" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PointInTimeRecoveryEnabled" : {
          "type" : "boolean"
        },
        "RecoveryPeriodInDays" : {
          "maximum" : 35,
          "type" : "integer",
          "minimum" : 1
        }
      },
      "dependencies" : {
        "RecoveryPeriodInDays" : [ "PointInTimeRecoveryEnabled" ]
      }
    },
    "ReplicaGlobalSecondaryIndexSpecification" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "IndexName" : {
          "minLength" : 3,
          "type" : "string",
          "maxLength" : 255
        },
        "ContributorInsightsSpecification" : {
          "$ref" : "#/definitions/ContributorInsightsSpecification"
        },
        "ReadProvisionedThroughputSettings" : {
          "$ref" : "#/definitions/ReadProvisionedThroughputSettings"
        },
        "ReadOnDemandThroughputSettings" : {
          "$ref" : "#/definitions/ReadOnDemandThroughputSettings"
        }
      },
      "required" : [ "IndexName" ]
    },
    "GlobalSecondaryIndex" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "IndexName" : {
          "minLength" : 3,
          "type" : "string",
          "maxLength" : 255
        },
        "Projection" : {
          "$ref" : "#/definitions/Projection"
        },
        "KeySchema" : {
          "minItems" : 1,
          "maxItems" : 2,
          "uniqueItems" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/KeySchema"
          }
        },
        "WarmThroughput" : {
          "$ref" : "#/definitions/WarmThroughput"
        },
        "WriteProvisionedThroughputSettings" : {
          "$ref" : "#/definitions/WriteProvisionedThroughputSettings"
        },
        "WriteOnDemandThroughputSettings" : {
          "$ref" : "#/definitions/WriteOnDemandThroughputSettings"
        }
      },
      "required" : [ "IndexName", "Projection", "KeySchema" ]
    },
    "WriteProvisionedThroughputSettings" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "WriteCapacityAutoScalingSettings" : {
          "$ref" : "#/definitions/CapacityAutoScalingSettings"
        }
      }
    },
    "WriteOnDemandThroughputSettings" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MaxWriteRequestUnits" : {
          "type" : "integer",
          "minimum" : 1
        }
      }
    },
    "ReplicaStreamSpecification" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ResourcePolicy" : {
          "$ref" : "#/definitions/ResourcePolicy"
        }
      },
      "required" : [ "ResourcePolicy" ]
    },
    "GlobalTableWitness" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Region" : {
          "type" : "string"
        }
      }
    },
    "ReadOnDemandThroughputSettings" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MaxReadRequestUnits" : {
          "type" : "integer",
          "minimum" : 1
        }
      }
    },
    "SSESpecification" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SSEEnabled" : {
          "type" : "boolean"
        },
        "SSEType" : {
          "type" : "string"
        }
      },
      "required" : [ "SSEEnabled" ]
    },
    "KinesisStreamSpecification" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ApproximateCreationDateTimePrecision" : {
          "type" : "string",
          "enum" : [ "MICROSECOND", "MILLISECOND" ]
        },
        "StreamArn" : {
          "relationshipRef" : {
            "typeName" : "AWS::Kinesis::Stream",
            "propertyPath" : "/properties/Arn"
          },
          "type" : "string"
        }
      },
      "required" : [ "StreamArn" ]
    },
    "StreamSpecification" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "StreamViewType" : {
          "type" : "string"
        }
      },
      "required" : [ "StreamViewType" ]
    },
    "ContributorInsightsSpecification" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ]
    },
    "CapacityAutoScalingSettings" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "MinCapacity" : {
          "type" : "integer",
          "minimum" : 1
        },
        "SeedCapacity" : {
          "type" : "integer",
          "minimum" : 1
        },
        "TargetTrackingScalingPolicyConfiguration" : {
          "$ref" : "#/definitions/TargetTrackingScalingPolicyConfiguration"
        },
        "MaxCapacity" : {
          "type" : "integer",
          "minimum" : 1
        }
      },
      "required" : [ "MinCapacity", "MaxCapacity", "TargetTrackingScalingPolicyConfiguration" ]
    },
    "WarmThroughput" : {
      "anyOf" : [ {
        "required" : [ "ReadUnitsPerSecond" ]
      }, {
        "required" : [ "WriteUnitsPerSecond" ]
      } ],
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ReadUnitsPerSecond" : {
          "type" : "integer",
          "minimum" : 1
        },
        "WriteUnitsPerSecond" : {
          "type" : "integer",
          "minimum" : 1
        }
      }
    },
    "TargetTrackingScalingPolicyConfiguration" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ScaleOutCooldown" : {
          "type" : "integer",
          "minimum" : 0
        },
        "TargetValue" : {
          "format" : "double",
          "type" : "number"
        },
        "DisableScaleIn" : {
          "type" : "boolean"
        },
        "ScaleInCooldown" : {
          "type" : "integer",
          "minimum" : 0
        }
      },
      "required" : [ "TargetValue" ]
    },
    "ReplicaSSESpecification" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "KMSMasterKeyId" : {
          "anyOf" : [ {
            "relationshipRef" : {
              "typeName" : "AWS::KMS::Key",
              "propertyPath" : "/properties/Arn"
            }
          }, {
            "relationshipRef" : {
              "typeName" : "AWS::KMS::Key",
              "propertyPath" : "/properties/KeyId"
            }
          }, {
            "relationshipRef" : {
              "typeName" : "AWS::KMS::Alias",
              "propertyPath" : "/properties/AliasName"
            }
          } ],
          "type" : "string"
        }
      },
      "required" : [ "KMSMasterKeyId" ]
    },
    "ResourcePolicy" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PolicyDocument" : {
          "type" : "object"
        }
      },
      "required" : [ "PolicyDocument" ]
    },
    "KeySchema" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "KeyType" : {
          "type" : "string"
        },
        "AttributeName" : {
          "minLength" : 1,
          "type" : "string",
          "maxLength" : 255
        }
      },
      "required" : [ "KeyType", "AttributeName" ]
    },
    "Tag" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    },
    "ReadProvisionedThroughputSettings" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ReadCapacityUnits" : {
          "type" : "integer",
          "minimum" : 1
        },
        "ReadCapacityAutoScalingSettings" : {
          "$ref" : "#/definitions/CapacityAutoScalingSettings"
        }
      }
    },
    "TimeToLiveSpecification" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "AttributeName" : {
          "type" : "string"
        }
      },
      "required" : [ "Enabled" ]
    }
  },
  "required" : [ "KeySchema", "AttributeDefinitions", "Replicas" ],
  "properties" : {
    "TableId" : {
      "type" : "string"
    },
    "SSESpecification" : {
      "$ref" : "#/definitions/SSESpecification"
    },
    "StreamSpecification" : {
      "$ref" : "#/definitions/StreamSpecification"
    },
    "WarmThroughput" : {
      "$ref" : "#/definitions/WarmThroughput"
    },
    "Replicas" : {
      "minItems" : 1,
      "uniqueItems" : True,
      "insertionOrder" : False,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/ReplicaSpecification"
      }
    },
    "WriteProvisionedThroughputSettings" : {
      "$ref" : "#/definitions/WriteProvisionedThroughputSettings"
    },
    "WriteOnDemandThroughputSettings" : {
      "$ref" : "#/definitions/WriteOnDemandThroughputSettings"
    },
    "TableName" : {
      "type" : "string"
    },
    "AttributeDefinitions" : {
      "minItems" : 1,
      "uniqueItems" : True,
      "insertionOrder" : False,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/AttributeDefinition"
      }
    },
    "BillingMode" : {
      "type" : "string"
    },
    "GlobalSecondaryIndexes" : {
      "uniqueItems" : True,
      "insertionOrder" : False,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/GlobalSecondaryIndex"
      }
    },
    "KeySchema" : {
      "minItems" : 1,
      "maxItems" : 2,
      "uniqueItems" : True,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/KeySchema"
      }
    },
    "LocalSecondaryIndexes" : {
      "uniqueItems" : True,
      "insertionOrder" : False,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/LocalSecondaryIndex"
      }
    },
    "Arn" : {
      "type" : "string"
    },
    "StreamArn" : {
      "type" : "string"
    },
    "TimeToLiveSpecification" : {
      "$ref" : "#/definitions/TimeToLiveSpecification"
    }
  }
}