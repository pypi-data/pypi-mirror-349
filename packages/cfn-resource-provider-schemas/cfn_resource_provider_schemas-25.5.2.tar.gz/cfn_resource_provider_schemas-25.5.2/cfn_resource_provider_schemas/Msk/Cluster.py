SCHEMA = {
  "typeName" : "AWS::MSK::Cluster",
  "description" : "Resource Type definition for AWS::MSK::Cluster",
  "additionalProperties" : False,
  "properties" : {
    "BrokerNodeGroupInfo" : {
      "$ref" : "#/definitions/BrokerNodeGroupInfo"
    },
    "EnhancedMonitoring" : {
      "type" : "string",
      "minLength" : 7,
      "maxLength" : 23,
      "enum" : [ "DEFAULT", "PER_BROKER", "PER_TOPIC_PER_BROKER", "PER_TOPIC_PER_PARTITION" ]
    },
    "KafkaVersion" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 128
    },
    "NumberOfBrokerNodes" : {
      "type" : "integer"
    },
    "EncryptionInfo" : {
      "$ref" : "#/definitions/EncryptionInfo"
    },
    "OpenMonitoring" : {
      "$ref" : "#/definitions/OpenMonitoring"
    },
    "ClusterName" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 64
    },
    "Arn" : {
      "type" : "string"
    },
    "CurrentVersion" : {
      "description" : "The current version of the MSK cluster",
      "type" : "string"
    },
    "ClientAuthentication" : {
      "$ref" : "#/definitions/ClientAuthentication"
    },
    "LoggingInfo" : {
      "$ref" : "#/definitions/LoggingInfo"
    },
    "Tags" : {
      "type" : "object",
      "description" : "A key-value pair to associate with a resource.",
      "patternProperties" : {
        "^([\\p{L}\\p{Z}\\p{N}_.:/=+\\-@]*)$" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "ConfigurationInfo" : {
      "$ref" : "#/definitions/ConfigurationInfo"
    },
    "StorageMode" : {
      "type" : "string",
      "minLength" : 5,
      "maxLength" : 6,
      "enum" : [ "LOCAL", "TIERED" ]
    }
  },
  "definitions" : {
    "S3" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "Prefix" : {
          "type" : "string"
        },
        "Bucket" : {
          "type" : "string"
        }
      },
      "required" : [ "Enabled" ]
    },
    "BrokerLogs" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "S3" : {
          "$ref" : "#/definitions/S3"
        },
        "CloudWatchLogs" : {
          "$ref" : "#/definitions/CloudWatchLogs"
        },
        "Firehose" : {
          "$ref" : "#/definitions/Firehose"
        }
      }
    },
    "NodeExporter" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "EnabledInBroker" : {
          "type" : "boolean"
        }
      },
      "required" : [ "EnabledInBroker" ]
    },
    "EncryptionInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "EncryptionAtRest" : {
          "$ref" : "#/definitions/EncryptionAtRest"
        },
        "EncryptionInTransit" : {
          "$ref" : "#/definitions/EncryptionInTransit"
        }
      }
    },
    "Firehose" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "DeliveryStream" : {
          "type" : "string"
        }
      },
      "required" : [ "Enabled" ]
    },
    "OpenMonitoring" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Prometheus" : {
          "$ref" : "#/definitions/Prometheus"
        }
      },
      "required" : [ "Prometheus" ]
    },
    "Prometheus" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "JmxExporter" : {
          "$ref" : "#/definitions/JmxExporter"
        },
        "NodeExporter" : {
          "$ref" : "#/definitions/NodeExporter"
        }
      }
    },
    "CloudWatchLogs" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "LogGroup" : {
          "type" : "string"
        },
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ]
    },
    "EBSStorageInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VolumeSize" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 16384
        },
        "ProvisionedThroughput" : {
          "$ref" : "#/definitions/ProvisionedThroughput"
        }
      }
    },
    "ProvisionedThroughput" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "VolumeThroughput" : {
          "type" : "integer"
        }
      }
    },
    "PublicAccess" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string",
          "minLength" : 7,
          "maxLength" : 23
        }
      }
    },
    "VpcConnectivity" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ClientAuthentication" : {
          "$ref" : "#/definitions/VpcConnectivityClientAuthentication"
        }
      }
    },
    "ConfigurationInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Revision" : {
          "type" : "integer"
        },
        "Arn" : {
          "type" : "string"
        }
      },
      "required" : [ "Revision", "Arn" ]
    },
    "BrokerNodeGroupInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "StorageInfo" : {
          "$ref" : "#/definitions/StorageInfo"
        },
        "ConnectivityInfo" : {
          "$ref" : "#/definitions/ConnectivityInfo"
        },
        "SecurityGroups" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        },
        "BrokerAZDistribution" : {
          "type" : "string",
          "minLength" : 6,
          "maxLength" : 9
        },
        "ClientSubnets" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        },
        "InstanceType" : {
          "type" : "string",
          "minLength" : 5,
          "maxLength" : 32
        }
      },
      "required" : [ "ClientSubnets", "InstanceType" ]
    },
    "EncryptionAtRest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DataVolumeKMSKeyId" : {
          "type" : "string"
        }
      },
      "required" : [ "DataVolumeKMSKeyId" ]
    },
    "JmxExporter" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "EnabledInBroker" : {
          "type" : "boolean"
        }
      },
      "required" : [ "EnabledInBroker" ]
    },
    "StorageInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "EBSStorageInfo" : {
          "$ref" : "#/definitions/EBSStorageInfo"
        }
      }
    },
    "ConnectivityInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PublicAccess" : {
          "$ref" : "#/definitions/PublicAccess"
        },
        "VpcConnectivity" : {
          "$ref" : "#/definitions/VpcConnectivity"
        }
      }
    },
    "VpcConnectivityTls" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ]
    },
    "VpcConnectivitySasl" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Scram" : {
          "$ref" : "#/definitions/VpcConnectivityScram"
        },
        "Iam" : {
          "$ref" : "#/definitions/VpcConnectivityIam"
        }
      }
    },
    "VpcConnectivityScram" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ]
    },
    "VpcConnectivityIam" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ]
    },
    "Tls" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CertificateAuthorityArnList" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Enabled" : {
          "type" : "boolean"
        }
      }
    },
    "Sasl" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Scram" : {
          "$ref" : "#/definitions/Scram"
        },
        "Iam" : {
          "$ref" : "#/definitions/Iam"
        }
      }
    },
    "Scram" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ]
    },
    "Iam" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ]
    },
    "Unauthenticated" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ]
    },
    "ClientAuthentication" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Tls" : {
          "$ref" : "#/definitions/Tls"
        },
        "Sasl" : {
          "$ref" : "#/definitions/Sasl"
        },
        "Unauthenticated" : {
          "$ref" : "#/definitions/Unauthenticated"
        }
      }
    },
    "VpcConnectivityClientAuthentication" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Tls" : {
          "$ref" : "#/definitions/VpcConnectivityTls"
        },
        "Sasl" : {
          "$ref" : "#/definitions/VpcConnectivitySasl"
        }
      }
    },
    "LoggingInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "BrokerLogs" : {
          "$ref" : "#/definitions/BrokerLogs"
        }
      },
      "required" : [ "BrokerLogs" ]
    },
    "EncryptionInTransit" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "InCluster" : {
          "type" : "boolean"
        },
        "ClientBroker" : {
          "type" : "string",
          "enum" : [ "TLS", "TLS_PLAINTEXT", "PLAINTEXT" ]
        }
      }
    }
  },
  "required" : [ "BrokerNodeGroupInfo", "KafkaVersion", "NumberOfBrokerNodes", "ClusterName" ],
  "createOnlyProperties" : [ "/properties/BrokerNodeGroupInfo/BrokerAZDistribution", "/properties/BrokerNodeGroupInfo/ClientSubnets", "/properties/BrokerNodeGroupInfo/SecurityGroups", "/properties/EncryptionInfo/EncryptionAtRest", "/properties/EncryptionInfo/EncryptionInTransit/InCluster", "/properties/ClusterName" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "readOnlyProperties" : [ "/properties/Arn" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "kafka:TagResource", "kafka:UntagResource", "kafka:ListTagsForResource" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "ec2:DescribeSecurityGroups", "ec2:DescribeSubnets", "ec2:DescribeVpcs", "iam:AttachRolePolicy", "iam:CreateServiceLinkedRole", "iam:PutRolePolicy", "kms:CreateGrant", "kms:DescribeKey", "kafka:CreateCluster", "kafka:DescribeCluster", "kafka:TagResource", "logs:CreateLogDelivery", "logs:GetLogDelivery", "logs:UpdateLogDelivery", "logs:DeleteLogDelivery", "logs:ListLogDeliveries", "s3:GetBucketPolicy", "s3:PutBucketPolicy", "logs:PutResourcePolicy", "logs:DescribeResourcePolicies", "logs:DescribeLogGroups", "firehose:TagDeliveryStream", "acm-pca:GetCertificateAuthorityCertificate" ],
      "timeoutInMinutes" : 120
    },
    "update" : {
      "permissions" : [ "kafka:UpdateMonitoring", "kafka:UpdateClusterKafkaVersion", "kafka:UpdateClusterConfiguration", "kafka:UpdateBrokerType", "kafka:UpdateBrokerCount", "kafka:UpdateBrokerStorage", "kafka:UpdateStorage", "kafka:UpdateSecurity", "kafka:UpdateConnectivity", "kafka:DescribeCluster", "kafka:DescribeClusterOperation", "kafka:TagResource", "kafka:UntagResource", "ec2:DescribeSubnets", "ec2:DescribeVpcs", "ec2:DescribeSecurityGroups", "iam:AttachRolePolicy", "iam:CreateServiceLinkedRole", "iam:PutRolePolicy", "kms:DescribeKey", "kms:CreateGrant", "logs:CreateLogDelivery", "logs:GetLogDelivery", "logs:UpdateLogDelivery", "logs:DeleteLogDelivery", "logs:ListLogDeliveries", "s3:GetBucketPolicy", "logs:PutResourcePolicy", "logs:DescribeResourcePolicies", "logs:DescribeLogGroups", "firehose:TagDeliveryStream", "acm-pca:GetCertificateAuthorityCertificate" ],
      "timeoutInMinutes" : 720
    },
    "delete" : {
      "permissions" : [ "kafka:DeleteCluster", "kafka:DescribeCluster" ],
      "timeoutInMinutes" : 30
    },
    "list" : {
      "permissions" : [ "kafka:ListClusters" ]
    },
    "read" : {
      "permissions" : [ "kafka:DescribeCluster" ]
    }
  }
}