SCHEMA = {
  "typeName" : "AWS::ElastiCache::ReplicationGroup",
  "description" : "Resource Type definition for AWS::ElastiCache::ReplicationGroup",
  "additionalProperties" : False,
  "properties" : {
    "PreferredCacheClusterAZs" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "ReaderEndPointPort" : {
      "type" : "string"
    },
    "NodeGroupConfiguration" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/NodeGroupConfiguration"
      }
    },
    "SnapshotArns" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "ConfigurationEndPointPort" : {
      "type" : "string"
    },
    "Port" : {
      "type" : "integer"
    },
    "NumNodeGroups" : {
      "type" : "integer"
    },
    "NotificationTopicArn" : {
      "type" : "string"
    },
    "AutomaticFailoverEnabled" : {
      "type" : "boolean"
    },
    "ReplicasPerNodeGroup" : {
      "type" : "integer"
    },
    "TransitEncryptionEnabled" : {
      "type" : "boolean"
    },
    "Engine" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "PrimaryEndPointAddress" : {
      "type" : "string"
    },
    "GlobalReplicationGroupId" : {
      "type" : "string"
    },
    "ConfigurationEndPointAddress" : {
      "type" : "string"
    },
    "EngineVersion" : {
      "type" : "string"
    },
    "KmsKeyId" : {
      "type" : "string"
    },
    "PrimaryClusterId" : {
      "type" : "string"
    },
    "ReadEndPointPorts" : {
      "type" : "string"
    },
    "AutoMinorVersionUpgrade" : {
      "type" : "boolean"
    },
    "SecurityGroupIds" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "SnapshotWindow" : {
      "type" : "string"
    },
    "TransitEncryptionMode" : {
      "type" : "string"
    },
    "SnapshotRetentionLimit" : {
      "type" : "integer"
    },
    "ReadEndPointAddressesList" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "SnapshottingClusterId" : {
      "type" : "string"
    },
    "IpDiscovery" : {
      "type" : "string"
    },
    "ReadEndPointAddresses" : {
      "type" : "string"
    },
    "PrimaryEndPointPort" : {
      "type" : "string"
    },
    "CacheSecurityGroupNames" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "ClusterMode" : {
      "type" : "string"
    },
    "ReadEndPointPortsList" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "SnapshotName" : {
      "type" : "string"
    },
    "ReplicationGroupDescription" : {
      "type" : "string"
    },
    "ReaderEndPointAddress" : {
      "type" : "string"
    },
    "MultiAZEnabled" : {
      "type" : "boolean"
    },
    "NetworkType" : {
      "type" : "string"
    },
    "ReplicationGroupId" : {
      "type" : "string"
    },
    "NumCacheClusters" : {
      "type" : "integer"
    },
    "CacheSubnetGroupName" : {
      "type" : "string"
    },
    "CacheParameterGroupName" : {
      "type" : "string"
    },
    "PreferredMaintenanceWindow" : {
      "type" : "string"
    },
    "AtRestEncryptionEnabled" : {
      "type" : "boolean"
    },
    "CacheNodeType" : {
      "type" : "string"
    },
    "UserGroupIds" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "AuthToken" : {
      "type" : "string"
    },
    "DataTieringEnabled" : {
      "type" : "boolean"
    },
    "LogDeliveryConfigurations" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/LogDeliveryConfigurationRequest"
      }
    }
  },
  "definitions" : {
    "LogDeliveryConfigurationRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "LogType" : {
          "type" : "string"
        },
        "LogFormat" : {
          "type" : "string"
        },
        "DestinationType" : {
          "type" : "string"
        },
        "DestinationDetails" : {
          "$ref" : "#/definitions/DestinationDetails"
        }
      },
      "required" : [ "LogFormat", "LogType", "DestinationType", "DestinationDetails" ]
    },
    "KinesisFirehoseDestinationDetails" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DeliveryStream" : {
          "type" : "string"
        }
      },
      "required" : [ "DeliveryStream" ]
    },
    "CloudWatchLogsDestinationDetails" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "LogGroup" : {
          "type" : "string"
        }
      },
      "required" : [ "LogGroup" ]
    },
    "NodeGroupConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Slots" : {
          "type" : "string"
        },
        "PrimaryAvailabilityZone" : {
          "type" : "string"
        },
        "ReplicaAvailabilityZones" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "NodeGroupId" : {
          "type" : "string"
        },
        "ReplicaCount" : {
          "type" : "integer"
        }
      }
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
    },
    "DestinationDetails" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CloudWatchLogsDetails" : {
          "$ref" : "#/definitions/CloudWatchLogsDestinationDetails"
        },
        "KinesisFirehoseDetails" : {
          "$ref" : "#/definitions/KinesisFirehoseDestinationDetails"
        }
      }
    }
  },
  "required" : [ "ReplicationGroupDescription" ],
  "createOnlyProperties" : [ "/properties/KmsKeyId", "/properties/Port", "/properties/SnapshotArns", "/properties/SnapshotName", "/properties/CacheSubnetGroupName", "/properties/NetworkType", "/properties/DataTieringEnabled", "/properties/AtRestEncryptionEnabled", "/properties/ReplicationGroupId", "/properties/GlobalReplicationGroupId", "/properties/ReplicasPerNodeGroup", "/properties/PreferredCacheClusterAZs" ],
  "primaryIdentifier" : [ "/properties/ReplicationGroupId" ],
  "readOnlyProperties" : [ "/properties/ConfigurationEndPoint.Address", "/properties/PrimaryEndPoint.Address", "/properties/PrimaryEndPoint.Port", "/properties/ReaderEndPoint.Address", "/properties/ConfigurationEndPoint.Port", "/properties/ReadEndPoint.Addresses.List", "/properties/ReadEndPoint.Ports.List", "/properties/ReaderEndPoint.Port", "/properties/ReadEndPoint.Addresses", "/properties/ReadEndPoint.Ports", "/properties/ReplicationGroupId" ]
}