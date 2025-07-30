SCHEMA = {
  "typeName" : "AWS::DLM::LifecyclePolicy",
  "description" : "Resource Type definition for AWS::DLM::LifecyclePolicy",
  "additionalProperties" : False,
  "properties" : {
    "CreateInterval" : {
      "type" : "integer"
    },
    "Description" : {
      "type" : "string"
    },
    "ExtendDeletion" : {
      "type" : "boolean"
    },
    "Exclusions" : {
      "$ref" : "#/definitions/Exclusions"
    },
    "RetainInterval" : {
      "type" : "integer"
    },
    "ExecutionRoleArn" : {
      "type" : "string"
    },
    "DefaultPolicy" : {
      "type" : "string"
    },
    "State" : {
      "type" : "string"
    },
    "CrossRegionCopyTargets" : {
      "$ref" : "#/definitions/CrossRegionCopyTargets"
    },
    "PolicyDetails" : {
      "$ref" : "#/definitions/PolicyDetails"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "CopyTags" : {
      "type" : "boolean"
    }
  },
  "definitions" : {
    "Action" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CrossRegionCopy" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/CrossRegionCopyAction"
          }
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "CrossRegionCopy", "Name" ]
    },
    "Exclusions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ExcludeTags" : {
          "$ref" : "#/definitions/ExcludeTags"
        },
        "ExcludeVolumeTypes" : {
          "$ref" : "#/definitions/ExcludeVolumeTypesList"
        },
        "ExcludeBootVolumes" : {
          "type" : "boolean"
        }
      }
    },
    "ArchiveRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RetainRule" : {
          "$ref" : "#/definitions/ArchiveRetainRule"
        }
      },
      "required" : [ "RetainRule" ]
    },
    "ExcludeVolumeTypesList" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "DeprecateRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IntervalUnit" : {
          "type" : "string"
        },
        "Count" : {
          "type" : "integer"
        },
        "Interval" : {
          "type" : "integer"
        }
      }
    },
    "CrossRegionCopyDeprecateRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IntervalUnit" : {
          "type" : "string"
        },
        "Interval" : {
          "type" : "integer"
        }
      },
      "required" : [ "IntervalUnit", "Interval" ]
    },
    "CreateRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IntervalUnit" : {
          "type" : "string"
        },
        "Scripts" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Script"
          }
        },
        "Times" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "CronExpression" : {
          "type" : "string"
        },
        "Interval" : {
          "type" : "integer"
        },
        "Location" : {
          "type" : "string"
        }
      }
    },
    "PolicyDetails" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PolicyLanguage" : {
          "type" : "string"
        },
        "ResourceTypes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Schedules" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Schedule"
          }
        },
        "PolicyType" : {
          "type" : "string"
        },
        "CreateInterval" : {
          "type" : "integer"
        },
        "Parameters" : {
          "$ref" : "#/definitions/Parameters"
        },
        "ExtendDeletion" : {
          "type" : "boolean"
        },
        "Exclusions" : {
          "$ref" : "#/definitions/Exclusions"
        },
        "Actions" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Action"
          }
        },
        "ResourceType" : {
          "type" : "string"
        },
        "RetainInterval" : {
          "type" : "integer"
        },
        "EventSource" : {
          "$ref" : "#/definitions/EventSource"
        },
        "CrossRegionCopyTargets" : {
          "$ref" : "#/definitions/CrossRegionCopyTargets"
        },
        "TargetTags" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Tag"
          }
        },
        "ResourceLocations" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "CopyTags" : {
          "type" : "boolean"
        }
      }
    },
    "Script" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ExecutionHandlerService" : {
          "type" : "string"
        },
        "ExecutionTimeout" : {
          "type" : "integer"
        },
        "Stages" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "ExecutionHandler" : {
          "type" : "string"
        },
        "MaximumRetryCount" : {
          "type" : "integer"
        },
        "ExecuteOperationOnScriptFailure" : {
          "type" : "boolean"
        }
      }
    },
    "Parameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ExcludeBootVolume" : {
          "type" : "boolean"
        },
        "NoReboot" : {
          "type" : "boolean"
        },
        "ExcludeDataVolumeTags" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Tag"
          }
        }
      }
    },
    "CrossRegionCopyRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TargetRegion" : {
          "type" : "string"
        },
        "Target" : {
          "type" : "string"
        },
        "DeprecateRule" : {
          "$ref" : "#/definitions/CrossRegionCopyDeprecateRule"
        },
        "Encrypted" : {
          "type" : "boolean"
        },
        "CmkArn" : {
          "type" : "string"
        },
        "RetainRule" : {
          "$ref" : "#/definitions/CrossRegionCopyRetainRule"
        },
        "CopyTags" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Encrypted" ]
    },
    "EncryptionConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Encrypted" : {
          "type" : "boolean"
        },
        "CmkArn" : {
          "type" : "string"
        }
      },
      "required" : [ "Encrypted" ]
    },
    "CrossRegionCopyRetainRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IntervalUnit" : {
          "type" : "string"
        },
        "Interval" : {
          "type" : "integer"
        }
      },
      "required" : [ "IntervalUnit", "Interval" ]
    },
    "ExcludeTags" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "EventParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DescriptionRegex" : {
          "type" : "string"
        },
        "EventType" : {
          "type" : "string"
        },
        "SnapshotOwner" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "EventType", "SnapshotOwner" ]
    },
    "RetainRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IntervalUnit" : {
          "type" : "string"
        },
        "Count" : {
          "type" : "integer"
        },
        "Interval" : {
          "type" : "integer"
        }
      }
    },
    "CrossRegionCopyAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Target" : {
          "type" : "string"
        },
        "EncryptionConfiguration" : {
          "$ref" : "#/definitions/EncryptionConfiguration"
        },
        "RetainRule" : {
          "$ref" : "#/definitions/CrossRegionCopyRetainRule"
        }
      },
      "required" : [ "Target", "EncryptionConfiguration" ]
    },
    "EventSource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "Parameters" : {
          "$ref" : "#/definitions/EventParameters"
        }
      },
      "required" : [ "Type" ]
    },
    "ArchiveRetainRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RetentionArchiveTier" : {
          "$ref" : "#/definitions/RetentionArchiveTier"
        }
      },
      "required" : [ "RetentionArchiveTier" ]
    },
    "CrossRegionCopyTargets" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "Schedule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ShareRules" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/ShareRule"
          }
        },
        "DeprecateRule" : {
          "$ref" : "#/definitions/DeprecateRule"
        },
        "TagsToAdd" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Tag"
          }
        },
        "CreateRule" : {
          "$ref" : "#/definitions/CreateRule"
        },
        "VariableTags" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Tag"
          }
        },
        "FastRestoreRule" : {
          "$ref" : "#/definitions/FastRestoreRule"
        },
        "ArchiveRule" : {
          "$ref" : "#/definitions/ArchiveRule"
        },
        "RetainRule" : {
          "$ref" : "#/definitions/RetainRule"
        },
        "CrossRegionCopyRules" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/CrossRegionCopyRule"
          }
        },
        "Name" : {
          "type" : "string"
        },
        "CopyTags" : {
          "type" : "boolean"
        }
      }
    },
    "FastRestoreRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IntervalUnit" : {
          "type" : "string"
        },
        "Count" : {
          "type" : "integer"
        },
        "AvailabilityZones" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Interval" : {
          "type" : "integer"
        }
      }
    },
    "RetentionArchiveTier" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IntervalUnit" : {
          "type" : "string"
        },
        "Count" : {
          "type" : "integer"
        },
        "Interval" : {
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
    "ShareRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TargetAccounts" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "UnshareIntervalUnit" : {
          "type" : "string"
        },
        "UnshareInterval" : {
          "type" : "integer"
        }
      }
    }
  },
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Arn" ]
}