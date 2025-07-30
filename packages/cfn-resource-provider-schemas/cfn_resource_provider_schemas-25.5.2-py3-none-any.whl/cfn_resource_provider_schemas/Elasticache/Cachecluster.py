SCHEMA = {
  "typeName" : "AWS::ElastiCache::CacheCluster",
  "description" : "Resource Type definition for AWS::ElastiCache::CacheCluster",
  "additionalProperties" : False,
  "properties" : {
    "CacheSecurityGroupNames" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "SnapshotArns" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "Port" : {
      "type" : "integer"
    },
    "ConfigurationEndpointAddress" : {
      "type" : "string"
    },
    "NotificationTopicArn" : {
      "type" : "string"
    },
    "NumCacheNodes" : {
      "type" : "integer"
    },
    "SnapshotName" : {
      "type" : "string"
    },
    "TransitEncryptionEnabled" : {
      "type" : "boolean"
    },
    "NetworkType" : {
      "type" : "string"
    },
    "PreferredAvailabilityZones" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "VpcSecurityGroupIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "ClusterName" : {
      "type" : "string"
    },
    "RedisEndpointAddress" : {
      "type" : "string"
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
    "EngineVersion" : {
      "type" : "string"
    },
    "RedisEndpointPort" : {
      "type" : "string"
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
    "AutoMinorVersionUpgrade" : {
      "type" : "boolean"
    },
    "PreferredAvailabilityZone" : {
      "type" : "string"
    },
    "SnapshotWindow" : {
      "type" : "string"
    },
    "CacheNodeType" : {
      "type" : "string"
    },
    "SnapshotRetentionLimit" : {
      "type" : "integer"
    },
    "ConfigurationEndpointPort" : {
      "type" : "string"
    },
    "IpDiscovery" : {
      "type" : "string"
    },
    "LogDeliveryConfigurations" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/LogDeliveryConfigurationRequest"
      }
    },
    "Id" : {
      "type" : "string"
    },
    "AZMode" : {
      "type" : "string"
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
  "required" : [ "CacheNodeType", "NumCacheNodes", "Engine" ],
  "createOnlyProperties" : [ "/properties/Port", "/properties/SnapshotArns", "/properties/SnapshotName", "/properties/CacheSubnetGroupName", "/properties/ClusterName", "/properties/NetworkType", "/properties/Engine" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/ConfigurationEndpoint.Address", "/properties/Id", "/properties/ConfigurationEndpoint.Port", "/properties/RedisEndpoint.Port", "/properties/RedisEndpoint.Address" ]
}