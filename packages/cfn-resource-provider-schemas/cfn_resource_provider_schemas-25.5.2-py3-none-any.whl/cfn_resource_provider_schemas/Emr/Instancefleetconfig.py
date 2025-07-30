SCHEMA = {
  "typeName" : "AWS::EMR::InstanceFleetConfig",
  "description" : "Resource Type definition for AWS::EMR::InstanceFleetConfig",
  "additionalProperties" : False,
  "properties" : {
    "InstanceFleetType" : {
      "type" : "string"
    },
    "TargetOnDemandCapacity" : {
      "type" : "integer"
    },
    "ClusterId" : {
      "type" : "string"
    },
    "TargetSpotCapacity" : {
      "type" : "integer"
    },
    "LaunchSpecifications" : {
      "$ref" : "#/definitions/InstanceFleetProvisioningSpecifications"
    },
    "ResizeSpecifications" : {
      "$ref" : "#/definitions/InstanceFleetResizingSpecifications"
    },
    "Id" : {
      "type" : "string"
    },
    "InstanceTypeConfigs" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/InstanceTypeConfig"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "VolumeSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SizeInGB" : {
          "type" : "integer"
        },
        "Throughput" : {
          "type" : "integer"
        },
        "VolumeType" : {
          "type" : "string"
        },
        "Iops" : {
          "type" : "integer"
        }
      },
      "required" : [ "SizeInGB", "VolumeType" ]
    },
    "EbsConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "EbsBlockDeviceConfigs" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/EbsBlockDeviceConfig"
          }
        },
        "EbsOptimized" : {
          "type" : "boolean"
        }
      }
    },
    "Configuration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ConfigurationProperties" : {
          "type" : "object",
          "patternProperties" : {
            "[a-zA-Z0-9]+" : {
              "type" : "string"
            }
          }
        },
        "Configurations" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/Configuration"
          }
        },
        "Classification" : {
          "type" : "string"
        }
      }
    },
    "OnDemandCapacityReservationOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "UsageStrategy" : {
          "type" : "string"
        },
        "CapacityReservationResourceGroupArn" : {
          "type" : "string"
        },
        "CapacityReservationPreference" : {
          "type" : "string"
        }
      }
    },
    "InstanceFleetResizingSpecifications" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OnDemandResizeSpecification" : {
          "$ref" : "#/definitions/OnDemandResizingSpecification"
        },
        "SpotResizeSpecification" : {
          "$ref" : "#/definitions/SpotResizingSpecification"
        }
      }
    },
    "InstanceFleetProvisioningSpecifications" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SpotSpecification" : {
          "$ref" : "#/definitions/SpotProvisioningSpecification"
        },
        "OnDemandSpecification" : {
          "$ref" : "#/definitions/OnDemandProvisioningSpecification"
        }
      }
    },
    "OnDemandResizingSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CapacityReservationOptions" : {
          "$ref" : "#/definitions/OnDemandCapacityReservationOptions"
        },
        "AllocationStrategy" : {
          "type" : "string"
        },
        "TimeoutDurationMinutes" : {
          "type" : "integer"
        }
      }
    },
    "OnDemandProvisioningSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CapacityReservationOptions" : {
          "$ref" : "#/definitions/OnDemandCapacityReservationOptions"
        },
        "AllocationStrategy" : {
          "type" : "string"
        }
      },
      "required" : [ "AllocationStrategy" ]
    },
    "EbsBlockDeviceConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VolumeSpecification" : {
          "$ref" : "#/definitions/VolumeSpecification"
        },
        "VolumesPerInstance" : {
          "type" : "integer"
        }
      },
      "required" : [ "VolumeSpecification" ]
    },
    "InstanceTypeConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "BidPrice" : {
          "type" : "string"
        },
        "WeightedCapacity" : {
          "type" : "integer"
        },
        "EbsConfiguration" : {
          "$ref" : "#/definitions/EbsConfiguration"
        },
        "Priority" : {
          "type" : "number"
        },
        "BidPriceAsPercentageOfOnDemandPrice" : {
          "type" : "number"
        },
        "CustomAmiId" : {
          "type" : "string"
        },
        "Configurations" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/Configuration"
          }
        },
        "InstanceType" : {
          "type" : "string"
        }
      },
      "required" : [ "InstanceType" ]
    },
    "SpotResizingSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AllocationStrategy" : {
          "type" : "string"
        },
        "TimeoutDurationMinutes" : {
          "type" : "integer"
        }
      }
    },
    "SpotProvisioningSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AllocationStrategy" : {
          "type" : "string"
        },
        "TimeoutDurationMinutes" : {
          "type" : "integer"
        },
        "TimeoutAction" : {
          "type" : "string"
        },
        "BlockDurationMinutes" : {
          "type" : "integer"
        }
      },
      "required" : [ "TimeoutDurationMinutes", "TimeoutAction" ]
    }
  },
  "required" : [ "InstanceFleetType", "ClusterId" ],
  "createOnlyProperties" : [ "/properties/Name", "/properties/LaunchSpecifications", "/properties/ClusterId", "/properties/InstanceFleetType" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}