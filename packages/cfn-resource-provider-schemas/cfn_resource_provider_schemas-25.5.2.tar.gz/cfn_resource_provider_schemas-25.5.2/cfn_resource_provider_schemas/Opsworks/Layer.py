SCHEMA = {
  "typeName" : "AWS::OpsWorks::Layer",
  "description" : "Resource Type definition for AWS::OpsWorks::Layer",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Attributes" : {
      "type" : "object",
      "patternProperties" : {
        "[a-zA-Z0-9]+" : {
          "type" : "string"
        }
      }
    },
    "AutoAssignElasticIps" : {
      "type" : "boolean"
    },
    "AutoAssignPublicIps" : {
      "type" : "boolean"
    },
    "CustomInstanceProfileArn" : {
      "type" : "string"
    },
    "CustomJson" : {
      "type" : "object"
    },
    "CustomRecipes" : {
      "$ref" : "#/definitions/Recipes"
    },
    "CustomSecurityGroupIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "EnableAutoHealing" : {
      "type" : "boolean"
    },
    "InstallUpdatesOnBoot" : {
      "type" : "boolean"
    },
    "LifecycleEventConfiguration" : {
      "$ref" : "#/definitions/LifecycleEventConfiguration"
    },
    "LoadBasedAutoScaling" : {
      "$ref" : "#/definitions/LoadBasedAutoScaling"
    },
    "Name" : {
      "type" : "string"
    },
    "Packages" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Shortname" : {
      "type" : "string"
    },
    "StackId" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "Type" : {
      "type" : "string"
    },
    "UseEbsOptimizedInstances" : {
      "type" : "boolean"
    },
    "VolumeConfigurations" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/VolumeConfiguration"
      }
    }
  },
  "definitions" : {
    "LifecycleEventConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ShutdownEventConfiguration" : {
          "$ref" : "#/definitions/ShutdownEventConfiguration"
        }
      }
    },
    "LoadBasedAutoScaling" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DownScaling" : {
          "$ref" : "#/definitions/AutoScalingThresholds"
        },
        "Enable" : {
          "type" : "boolean"
        },
        "UpScaling" : {
          "$ref" : "#/definitions/AutoScalingThresholds"
        }
      }
    },
    "Recipes" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Configure" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "Deploy" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "Setup" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "Shutdown" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "Undeploy" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "VolumeConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Encrypted" : {
          "type" : "boolean"
        },
        "Iops" : {
          "type" : "integer"
        },
        "MountPoint" : {
          "type" : "string"
        },
        "NumberOfDisks" : {
          "type" : "integer"
        },
        "RaidLevel" : {
          "type" : "integer"
        },
        "Size" : {
          "type" : "integer"
        },
        "VolumeType" : {
          "type" : "string"
        }
      }
    },
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    },
    "ShutdownEventConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DelayUntilElbConnectionsDrained" : {
          "type" : "boolean"
        },
        "ExecutionTimeout" : {
          "type" : "integer"
        }
      }
    },
    "AutoScalingThresholds" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CpuThreshold" : {
          "type" : "number"
        },
        "IgnoreMetricsTime" : {
          "type" : "integer"
        },
        "InstanceCount" : {
          "type" : "integer"
        },
        "LoadThreshold" : {
          "type" : "number"
        },
        "MemoryThreshold" : {
          "type" : "number"
        },
        "ThresholdsWaitTime" : {
          "type" : "integer"
        }
      }
    }
  },
  "required" : [ "EnableAutoHealing", "Name", "Type", "AutoAssignElasticIps", "Shortname", "AutoAssignPublicIps", "StackId" ],
  "createOnlyProperties" : [ "/properties/Type", "/properties/StackId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}