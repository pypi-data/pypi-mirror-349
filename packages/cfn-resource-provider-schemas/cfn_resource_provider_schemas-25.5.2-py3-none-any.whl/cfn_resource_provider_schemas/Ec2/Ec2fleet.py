SCHEMA = {
  "handlers" : {
    "read" : {
      "permissions" : [ "ec2:DescribeFleets" ]
    },
    "create" : {
      "permissions" : [ "ec2:CreateFleet", "ec2:DescribeFleets" ]
    },
    "update" : {
      "permissions" : [ "ec2:ModifyFleet", "ec2:DescribeFleets" ]
    },
    "list" : {
      "permissions" : [ "ec2:DescribeFleets" ]
    },
    "delete" : {
      "permissions" : [ "ec2:DescribeFleets", "ec2:DeleteFleets" ]
    }
  },
  "typeName" : "AWS::EC2::EC2Fleet",
  "readOnlyProperties" : [ "/properties/FleetId" ],
  "description" : "Resource Type definition for AWS::EC2::EC2Fleet",
  "createOnlyProperties" : [ "/properties/LaunchTemplateConfigs", "/properties/OnDemandOptions", "/properties/ReplaceUnhealthyInstances", "/properties/SpotOptions", "/properties/TagSpecifications", "/properties/TerminateInstancesWithExpiration", "/properties/Type", "/properties/ValidFrom", "/properties/ValidUntil" ],
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/FleetId" ],
  "definitions" : {
    "TargetCapacitySpecificationRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DefaultTargetCapacityType" : {
          "type" : "string",
          "enum" : [ "on-demand", "spot" ]
        },
        "TotalTargetCapacity" : {
          "type" : "integer"
        },
        "OnDemandTargetCapacity" : {
          "type" : "integer"
        },
        "SpotTargetCapacity" : {
          "type" : "integer"
        },
        "TargetCapacityUnitType" : {
          "type" : "string",
          "enum" : [ "vcpu", "memory-mib", "units" ]
        }
      },
      "required" : [ "TotalTargetCapacity" ]
    },
    "FleetLaunchTemplateSpecificationRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "LaunchTemplateName" : {
          "minLength" : 3,
          "pattern" : "[a-zA-Z0-9\\(\\)\\.\\-/_]+",
          "type" : "string",
          "maxLength" : 128
        },
        "Version" : {
          "type" : "string"
        },
        "LaunchTemplateId" : {
          "type" : "string"
        }
      },
      "required" : [ "Version" ]
    },
    "MemoryGiBPerVCpuRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Min" : {
          "type" : "number"
        },
        "Max" : {
          "type" : "number"
        }
      }
    },
    "CapacityReservationOptionsRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "UsageStrategy" : {
          "type" : "string",
          "enum" : [ "use-capacity-reservations-first" ]
        }
      }
    },
    "TotalLocalStorageGBRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Min" : {
          "type" : "number"
        },
        "Max" : {
          "type" : "number"
        }
      }
    },
    "NetworkBandwidthGbpsRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Min" : {
          "type" : "number"
        },
        "Max" : {
          "type" : "number"
        }
      }
    },
    "VCpuCountRangeRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Min" : {
          "type" : "integer"
        },
        "Max" : {
          "type" : "integer"
        }
      }
    },
    "BaselineEbsBandwidthMbpsRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Min" : {
          "type" : "integer"
        },
        "Max" : {
          "type" : "integer"
        }
      }
    },
    "NetworkInterfaceCountRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Min" : {
          "type" : "integer"
        },
        "Max" : {
          "type" : "integer"
        }
      }
    },
    "OnDemandOptionsRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SingleAvailabilityZone" : {
          "type" : "boolean"
        },
        "AllocationStrategy" : {
          "type" : "string"
        },
        "SingleInstanceType" : {
          "type" : "boolean"
        },
        "MinTargetCapacity" : {
          "type" : "integer"
        },
        "MaxTotalPrice" : {
          "type" : "string"
        },
        "CapacityReservationOptions" : {
          "$ref" : "#/definitions/CapacityReservationOptionsRequest"
        }
      }
    },
    "SpotOptionsRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SingleAvailabilityZone" : {
          "type" : "boolean"
        },
        "AllocationStrategy" : {
          "type" : "string",
          "enum" : [ "lowest-price", "lowestPrice", "diversified", "capacityOptimized", "capacity-optimized", "capacityOptimizedPrioritized", "capacity-optimized-prioritized", "priceCapacityOptimized", "price-capacity-optimized" ]
        },
        "SingleInstanceType" : {
          "type" : "boolean"
        },
        "MinTargetCapacity" : {
          "type" : "integer"
        },
        "MaxTotalPrice" : {
          "type" : "string"
        },
        "MaintenanceStrategies" : {
          "$ref" : "#/definitions/MaintenanceStrategies"
        },
        "InstanceInterruptionBehavior" : {
          "type" : "string",
          "enum" : [ "hibernate", "stop", "terminate" ]
        },
        "InstancePoolsToUseCount" : {
          "type" : "integer"
        }
      }
    },
    "Placement" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "GroupName" : {
          "type" : "string"
        },
        "Tenancy" : {
          "type" : "string"
        },
        "SpreadDomain" : {
          "type" : "string"
        },
        "PartitionNumber" : {
          "type" : "integer"
        },
        "AvailabilityZone" : {
          "type" : "string"
        },
        "Affinity" : {
          "type" : "string"
        },
        "HostId" : {
          "type" : "string"
        },
        "HostResourceGroupArn" : {
          "type" : "string"
        }
      }
    },
    "PerformanceFactorReferenceRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "InstanceFamily" : {
          "type" : "string"
        }
      }
    },
    "CpuPerformanceFactorRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "References" : {
          "uniqueItems" : False,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PerformanceFactorReferenceRequest"
          }
        }
      }
    },
    "MaintenanceStrategies" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "CapacityRebalance" : {
          "$ref" : "#/definitions/CapacityRebalance"
        }
      }
    },
    "BlockDeviceMapping" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Ebs" : {
          "$ref" : "#/definitions/EbsBlockDevice"
        },
        "NoDevice" : {
          "type" : "string"
        },
        "VirtualName" : {
          "type" : "string"
        },
        "DeviceName" : {
          "type" : "string"
        }
      }
    },
    "AcceleratorCountRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Min" : {
          "type" : "integer"
        },
        "Max" : {
          "type" : "integer"
        }
      }
    },
    "CapacityRebalance" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "TerminationDelay" : {
          "type" : "integer"
        },
        "ReplacementStrategy" : {
          "type" : "string",
          "enum" : [ "launch", "launch-before-terminate" ]
        }
      }
    },
    "FleetLaunchTemplateConfigRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "LaunchTemplateSpecification" : {
          "$ref" : "#/definitions/FleetLaunchTemplateSpecificationRequest"
        },
        "Overrides" : {
          "uniqueItems" : False,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FleetLaunchTemplateOverridesRequest"
          }
        }
      }
    },
    "FleetLaunchTemplateOverridesRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "WeightedCapacity" : {
          "type" : "number"
        },
        "Placement" : {
          "$ref" : "#/definitions/Placement"
        },
        "Priority" : {
          "type" : "number"
        },
        "AvailabilityZone" : {
          "type" : "string"
        },
        "SubnetId" : {
          "type" : "string"
        },
        "InstanceRequirements" : {
          "$ref" : "#/definitions/InstanceRequirementsRequest"
        },
        "InstanceType" : {
          "type" : "string"
        },
        "MaxPrice" : {
          "type" : "string"
        }
      }
    },
    "InstanceRequirementsRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "InstanceGenerations" : {
          "uniqueItems" : False,
          "type" : "array",
          "items" : {
            "type" : "string",
            "enum" : [ "current", "previous" ]
          }
        },
        "MemoryGiBPerVCpu" : {
          "$ref" : "#/definitions/MemoryGiBPerVCpuRequest"
        },
        "AcceleratorTypes" : {
          "uniqueItems" : False,
          "type" : "array",
          "items" : {
            "type" : "string",
            "enum" : [ "gpu", "fpga", "inference" ]
          }
        },
        "VCpuCount" : {
          "$ref" : "#/definitions/VCpuCountRangeRequest"
        },
        "AcceleratorManufacturers" : {
          "uniqueItems" : False,
          "type" : "array",
          "items" : {
            "type" : "string",
            "enum" : [ "amazon-web-services", "amd", "habana", "nvidia", "xilinx" ]
          }
        },
        "LocalStorage" : {
          "type" : "string",
          "enum" : [ "included", "required", "excluded" ]
        },
        "CpuManufacturers" : {
          "uniqueItems" : False,
          "type" : "array",
          "items" : {
            "type" : "string",
            "enum" : [ "intel", "amd", "amazon-web-services", "apple" ]
          }
        },
        "BareMetal" : {
          "type" : "string",
          "enum" : [ "included", "required", "excluded" ]
        },
        "RequireHibernateSupport" : {
          "type" : "boolean"
        },
        "MaxSpotPriceAsPercentageOfOptimalOnDemandPrice" : {
          "type" : "integer"
        },
        "OnDemandMaxPricePercentageOverLowestPrice" : {
          "type" : "integer"
        },
        "MemoryMiB" : {
          "$ref" : "#/definitions/MemoryMiBRequest"
        },
        "LocalStorageTypes" : {
          "uniqueItems" : False,
          "type" : "array",
          "items" : {
            "type" : "string",
            "enum" : [ "hdd", "ssd" ]
          }
        },
        "NetworkInterfaceCount" : {
          "$ref" : "#/definitions/NetworkInterfaceCountRequest"
        },
        "ExcludedInstanceTypes" : {
          "uniqueItems" : False,
          "type" : "array",
          "items" : {
            "minLength" : 1,
            "pattern" : "[a-zA-Z0-9\\.\\*]+",
            "type" : "string",
            "maxLength" : 30
          }
        },
        "AllowedInstanceTypes" : {
          "uniqueItems" : False,
          "type" : "array",
          "items" : {
            "minLength" : 1,
            "pattern" : "[a-zA-Z0-9\\.\\*]+",
            "type" : "string",
            "maxLength" : 30
          }
        },
        "NetworkBandwidthGbps" : {
          "$ref" : "#/definitions/NetworkBandwidthGbpsRequest"
        },
        "AcceleratorCount" : {
          "$ref" : "#/definitions/AcceleratorCountRequest"
        },
        "BaselinePerformanceFactors" : {
          "$ref" : "#/definitions/BaselinePerformanceFactorsRequest"
        },
        "SpotMaxPricePercentageOverLowestPrice" : {
          "type" : "integer"
        },
        "BaselineEbsBandwidthMbps" : {
          "$ref" : "#/definitions/BaselineEbsBandwidthMbpsRequest"
        },
        "AcceleratorNames" : {
          "uniqueItems" : False,
          "type" : "array",
          "items" : {
            "type" : "string",
            "enum" : [ "a10g", "a100", "h100", "inferentia", "k520", "k80", "m60", "radeon-pro-v520", "t4", "t4g", "vu9p", "v100" ]
          }
        },
        "AcceleratorTotalMemoryMiB" : {
          "$ref" : "#/definitions/AcceleratorTotalMemoryMiBRequest"
        },
        "BurstablePerformance" : {
          "type" : "string",
          "enum" : [ "included", "required", "excluded" ]
        },
        "TotalLocalStorageGB" : {
          "$ref" : "#/definitions/TotalLocalStorageGBRequest"
        }
      }
    },
    "MemoryMiBRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Min" : {
          "type" : "integer"
        },
        "Max" : {
          "type" : "integer"
        }
      }
    },
    "TagSpecification" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ResourceType" : {
          "type" : "string",
          "enum" : [ "client-vpn-endpoint", "customer-gateway", "dedicated-host", "dhcp-options", "egress-only-internet-gateway", "elastic-gpu", "elastic-ip", "export-image-task", "export-instance-task", "fleet", "fpga-image", "host-reservation", "image", "import-image-task", "import-snapshot-task", "instance", "internet-gateway", "key-pair", "launch-template", "local-gateway-route-table-vpc-association", "natgateway", "network-acl", "network-insights-analysis", "network-insights-path", "network-interface", "placement-group", "reserved-instances", "route-table", "security-group", "snapshot", "spot-fleet-request", "spot-instances-request", "subnet", "traffic-mirror-filter", "traffic-mirror-session", "traffic-mirror-target", "transit-gateway", "transit-gateway-attachment", "transit-gateway-connect-peer", "transit-gateway-multicast-domain", "transit-gateway-route-table", "volume", "vpc", "vpc-flow-log", "vpc-peering-connection", "vpn-connection", "vpn-gateway" ]
        },
        "Tags" : {
          "uniqueItems" : False,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Tag"
          }
        }
      }
    },
    "BaselinePerformanceFactorsRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Cpu" : {
          "$ref" : "#/definitions/CpuPerformanceFactorRequest"
        }
      }
    },
    "AcceleratorTotalMemoryMiBRequest" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Min" : {
          "type" : "integer"
        },
        "Max" : {
          "type" : "integer"
        }
      }
    },
    "EbsBlockDevice" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "SnapshotId" : {
          "type" : "string"
        },
        "VolumeType" : {
          "type" : "string",
          "enum" : [ "gp2", "gp3", "io1", "io2", "sc1", "st1", "standard" ]
        },
        "KmsKeyId" : {
          "type" : "string"
        },
        "Encrypted" : {
          "type" : "boolean"
        },
        "Iops" : {
          "type" : "integer"
        },
        "VolumeSize" : {
          "type" : "integer"
        },
        "DeleteOnTermination" : {
          "type" : "boolean"
        }
      }
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
    }
  },
  "properties" : {
    "Context" : {
      "type" : "string"
    },
    "TargetCapacitySpecification" : {
      "$ref" : "#/definitions/TargetCapacitySpecificationRequest"
    },
    "OnDemandOptions" : {
      "$ref" : "#/definitions/OnDemandOptionsRequest"
    },
    "ExcessCapacityTerminationPolicy" : {
      "type" : "string",
      "enum" : [ "termination", "no-termination" ]
    },
    "TagSpecifications" : {
      "uniqueItems" : False,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/TagSpecification"
      }
    },
    "SpotOptions" : {
      "$ref" : "#/definitions/SpotOptionsRequest"
    },
    "LaunchTemplateConfigs" : {
      "maxItems" : 50,
      "uniqueItems" : False,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/FleetLaunchTemplateConfigRequest"
      }
    },
    "TerminateInstancesWithExpiration" : {
      "type" : "boolean"
    },
    "ValidUntil" : {
      "type" : "string"
    },
    "Type" : {
      "type" : "string",
      "enum" : [ "maintain", "request", "instant" ]
    },
    "FleetId" : {
      "type" : "string"
    },
    "ValidFrom" : {
      "type" : "string"
    },
    "ReplaceUnhealthyInstances" : {
      "type" : "boolean"
    }
  },
  "required" : [ "TargetCapacitySpecification", "LaunchTemplateConfigs" ]
}