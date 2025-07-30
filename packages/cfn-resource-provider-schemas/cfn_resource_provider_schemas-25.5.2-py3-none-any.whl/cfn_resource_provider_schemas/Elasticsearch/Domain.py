SCHEMA = {
  "typeName" : "AWS::Elasticsearch::Domain",
  "description" : "Resource Type definition for AWS::Elasticsearch::Domain",
  "additionalProperties" : False,
  "properties" : {
    "ElasticsearchClusterConfig" : {
      "$ref" : "#/definitions/ElasticsearchClusterConfig"
    },
    "DomainName" : {
      "type" : "string"
    },
    "ElasticsearchVersion" : {
      "type" : "string"
    },
    "LogPublishingOptions" : {
      "type" : "object",
      "patternProperties" : {
        "[a-zA-Z0-9]+" : {
          "$ref" : "#/definitions/LogPublishingOption"
        }
      }
    },
    "SnapshotOptions" : {
      "$ref" : "#/definitions/SnapshotOptions"
    },
    "VPCOptions" : {
      "$ref" : "#/definitions/VPCOptions"
    },
    "NodeToNodeEncryptionOptions" : {
      "$ref" : "#/definitions/NodeToNodeEncryptionOptions"
    },
    "AccessPolicies" : {
      "type" : "object"
    },
    "DomainEndpointOptions" : {
      "$ref" : "#/definitions/DomainEndpointOptions"
    },
    "DomainArn" : {
      "type" : "string"
    },
    "CognitoOptions" : {
      "$ref" : "#/definitions/CognitoOptions"
    },
    "AdvancedOptions" : {
      "type" : "object",
      "patternProperties" : {
        "[a-zA-Z0-9]+" : {
          "type" : "string"
        }
      }
    },
    "AdvancedSecurityOptions" : {
      "$ref" : "#/definitions/AdvancedSecurityOptionsInput"
    },
    "DomainEndpoint" : {
      "type" : "string"
    },
    "EBSOptions" : {
      "$ref" : "#/definitions/EBSOptions"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "EncryptionAtRestOptions" : {
      "$ref" : "#/definitions/EncryptionAtRestOptions"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "definitions" : {
    "LogPublishingOption" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CloudWatchLogsLogGroupArn" : {
          "type" : "string"
        },
        "Enabled" : {
          "type" : "boolean"
        }
      }
    },
    "ElasticsearchClusterConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "InstanceCount" : {
          "type" : "integer"
        },
        "WarmEnabled" : {
          "type" : "boolean"
        },
        "WarmCount" : {
          "type" : "integer"
        },
        "DedicatedMasterEnabled" : {
          "type" : "boolean"
        },
        "ZoneAwarenessConfig" : {
          "$ref" : "#/definitions/ZoneAwarenessConfig"
        },
        "ColdStorageOptions" : {
          "$ref" : "#/definitions/ColdStorageOptions"
        },
        "DedicatedMasterCount" : {
          "type" : "integer"
        },
        "InstanceType" : {
          "type" : "string"
        },
        "WarmType" : {
          "type" : "string"
        },
        "ZoneAwarenessEnabled" : {
          "type" : "boolean"
        },
        "DedicatedMasterType" : {
          "type" : "string"
        }
      }
    },
    "VPCOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecurityGroupIds" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "SubnetIds" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "SnapshotOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AutomatedSnapshotStartHour" : {
          "type" : "integer"
        }
      }
    },
    "ZoneAwarenessConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AvailabilityZoneCount" : {
          "type" : "integer"
        }
      }
    },
    "NodeToNodeEncryptionOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        }
      }
    },
    "ColdStorageOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        }
      }
    },
    "DomainEndpointOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CustomEndpointCertificateArn" : {
          "type" : "string"
        },
        "CustomEndpointEnabled" : {
          "type" : "boolean"
        },
        "EnforceHTTPS" : {
          "type" : "boolean"
        },
        "CustomEndpoint" : {
          "type" : "string"
        },
        "TLSSecurityPolicy" : {
          "type" : "string"
        }
      }
    },
    "CognitoOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "IdentityPoolId" : {
          "type" : "string"
        },
        "UserPoolId" : {
          "type" : "string"
        },
        "RoleArn" : {
          "type" : "string"
        }
      }
    },
    "EBSOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "EBSEnabled" : {
          "type" : "boolean"
        },
        "VolumeType" : {
          "type" : "string"
        },
        "Iops" : {
          "type" : "integer"
        },
        "VolumeSize" : {
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
    "EncryptionAtRestOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "KmsKeyId" : {
          "type" : "string"
        },
        "Enabled" : {
          "type" : "boolean"
        }
      }
    },
    "MasterUserOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MasterUserPassword" : {
          "type" : "string"
        },
        "MasterUserName" : {
          "type" : "string"
        },
        "MasterUserARN" : {
          "type" : "string"
        }
      }
    },
    "AdvancedSecurityOptionsInput" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "MasterUserOptions" : {
          "$ref" : "#/definitions/MasterUserOptions"
        },
        "AnonymousAuthEnabled" : {
          "type" : "boolean"
        },
        "InternalUserDatabaseEnabled" : {
          "type" : "boolean"
        }
      }
    }
  },
  "createOnlyProperties" : [ "/properties/DomainName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/DomainArn", "/properties/DomainEndpoint", "/properties/Arn" ]
}