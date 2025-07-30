SCHEMA = {
  "typeName" : "AWS::EC2::SpotFleet",
  "description" : "Resource Type definition for AWS::EC2::SpotFleet",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "SpotFleetRequestConfigData" : {
      "$ref" : "#/definitions/SpotFleetRequestConfigData"
    }
  },
  "definitions" : {
    "SpotFleetRequestConfigData" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AllocationStrategy" : {
          "type" : "string",
          "enum" : [ "capacityOptimized", "capacityOptimizedPrioritized", "diversified", "lowestPrice", "priceCapacityOptimized" ]
        },
        "Context" : {
          "type" : "string"
        },
        "ExcessCapacityTerminationPolicy" : {
          "type" : "string",
          "enum" : [ "Default", "NoTermination", "default", "noTermination" ]
        },
        "IamFleetRole" : {
          "type" : "string"
        },
        "InstanceInterruptionBehavior" : {
          "type" : "string",
          "enum" : [ "hibernate", "stop", "terminate" ]
        },
        "InstancePoolsToUseCount" : {
          "type" : "integer"
        },
        "LaunchSpecifications" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/SpotFleetLaunchSpecification"
          }
        },
        "LaunchTemplateConfigs" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/LaunchTemplateConfig"
          }
        },
        "LoadBalancersConfig" : {
          "$ref" : "#/definitions/LoadBalancersConfig"
        },
        "OnDemandAllocationStrategy" : {
          "type" : "string"
        },
        "OnDemandMaxTotalPrice" : {
          "type" : "string"
        },
        "OnDemandTargetCapacity" : {
          "type" : "integer"
        },
        "ReplaceUnhealthyInstances" : {
          "type" : "boolean"
        },
        "SpotMaintenanceStrategies" : {
          "$ref" : "#/definitions/SpotMaintenanceStrategies"
        },
        "SpotMaxTotalPrice" : {
          "type" : "string"
        },
        "SpotPrice" : {
          "type" : "string"
        },
        "TargetCapacity" : {
          "type" : "integer"
        },
        "TerminateInstancesWithExpiration" : {
          "type" : "boolean"
        },
        "Type" : {
          "type" : "string",
          "enum" : [ "maintain", "request" ]
        },
        "ValidFrom" : {
          "type" : "string"
        },
        "ValidUntil" : {
          "type" : "string"
        },
        "TagSpecifications" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/SpotFleetTagSpecification"
          }
        },
        "TargetCapacityUnitType" : {
          "type" : "string",
          "enum" : [ "vcpu", "memory-mib", "units" ]
        }
      },
      "required" : [ "IamFleetRole", "TargetCapacity" ]
    },
    "SpotFleetLaunchSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "BlockDeviceMappings" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/BlockDeviceMapping"
          }
        },
        "EbsOptimized" : {
          "type" : "boolean",
          "default" : False
        },
        "IamInstanceProfile" : {
          "$ref" : "#/definitions/IamInstanceProfileSpecification"
        },
        "ImageId" : {
          "type" : "string"
        },
        "InstanceType" : {
          "type" : "string"
        },
        "KernelId" : {
          "type" : "string"
        },
        "KeyName" : {
          "type" : "string"
        },
        "Monitoring" : {
          "$ref" : "#/definitions/SpotFleetMonitoring"
        },
        "NetworkInterfaces" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/InstanceNetworkInterfaceSpecification"
          }
        },
        "Placement" : {
          "$ref" : "#/definitions/SpotPlacement"
        },
        "RamdiskId" : {
          "type" : "string"
        },
        "SecurityGroups" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/GroupIdentifier"
          }
        },
        "SpotPrice" : {
          "type" : "string"
        },
        "SubnetId" : {
          "type" : "string"
        },
        "TagSpecifications" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/SpotFleetTagSpecification"
          }
        },
        "UserData" : {
          "type" : "string"
        },
        "WeightedCapacity" : {
          "type" : "number"
        },
        "InstanceRequirements" : {
          "$ref" : "#/definitions/InstanceRequirementsRequest"
        }
      },
      "required" : [ "ImageId" ]
    },
    "LoadBalancersConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ClassicLoadBalancersConfig" : {
          "$ref" : "#/definitions/ClassicLoadBalancersConfig"
        },
        "TargetGroupsConfig" : {
          "$ref" : "#/definitions/TargetGroupsConfig"
        }
      }
    },
    "SpotMaintenanceStrategies" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CapacityRebalance" : {
          "$ref" : "#/definitions/SpotCapacityRebalance"
        }
      }
    },
    "SpotCapacityRebalance" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ReplacementStrategy" : {
          "type" : "string",
          "enum" : [ "launch", "launch-before-terminate" ]
        },
        "TerminationDelay" : {
          "type" : "integer"
        }
      }
    },
    "LaunchTemplateConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "LaunchTemplateSpecification" : {
          "$ref" : "#/definitions/FleetLaunchTemplateSpecification"
        },
        "Overrides" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/LaunchTemplateOverrides"
          }
        }
      }
    },
    "SpotFleetTagSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ResourceType" : {
          "type" : "string",
          "enum" : [ "client-vpn-endpoint", "customer-gateway", "dedicated-host", "dhcp-options", "egress-only-internet-gateway", "elastic-gpu", "elastic-ip", "export-image-task", "export-instance-task", "fleet", "fpga-image", "host-reservation", "image", "import-image-task", "import-snapshot-task", "instance", "internet-gateway", "key-pair", "launch-template", "local-gateway-route-table-vpc-association", "natgateway", "network-acl", "network-insights-analysis", "network-insights-path", "network-interface", "placement-group", "reserved-instances", "route-table", "security-group", "snapshot", "spot-fleet-request", "spot-instances-request", "subnet", "traffic-mirror-filter", "traffic-mirror-session", "traffic-mirror-target", "transit-gateway", "transit-gateway-attachment", "transit-gateway-connect-peer", "transit-gateway-multicast-domain", "transit-gateway-route-table", "volume", "vpc", "vpc-flow-log", "vpc-peering-connection", "vpn-connection", "vpn-gateway" ]
        },
        "Tags" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Tag"
          }
        }
      }
    },
    "FleetLaunchTemplateSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "LaunchTemplateId" : {
          "type" : "string"
        },
        "LaunchTemplateName" : {
          "type" : "string",
          "minLength" : 3,
          "maxLength" : 128,
          "pattern" : "[a-zA-Z0-9\\(\\)\\.\\-/_]+"
        },
        "Version" : {
          "type" : "string"
        }
      },
      "required" : [ "Version" ]
    },
    "GroupIdentifier" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "GroupId" : {
          "type" : "string"
        }
      },
      "required" : [ "GroupId" ]
    },
    "IamInstanceProfileSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Arn" : {
          "type" : "string"
        }
      }
    },
    "ClassicLoadBalancersConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ClassicLoadBalancers" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/ClassicLoadBalancer"
          }
        }
      },
      "required" : [ "ClassicLoadBalancers" ]
    },
    "LaunchTemplateOverrides" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AvailabilityZone" : {
          "type" : "string"
        },
        "InstanceType" : {
          "type" : "string"
        },
        "SpotPrice" : {
          "type" : "string"
        },
        "SubnetId" : {
          "type" : "string"
        },
        "WeightedCapacity" : {
          "type" : "number"
        },
        "InstanceRequirements" : {
          "$ref" : "#/definitions/InstanceRequirementsRequest"
        },
        "Priority" : {
          "type" : "number"
        }
      }
    },
    "SpotFleetMonitoring" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean",
          "default" : False
        }
      }
    },
    "SpotPlacement" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AvailabilityZone" : {
          "type" : "string"
        },
        "GroupName" : {
          "type" : "string"
        },
        "Tenancy" : {
          "type" : "string",
          "enum" : [ "dedicated", "default", "host" ]
        }
      }
    },
    "InstanceNetworkInterfaceSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AssociatePublicIpAddress" : {
          "type" : "boolean"
        },
        "DeleteOnTermination" : {
          "type" : "boolean"
        },
        "Description" : {
          "type" : "string"
        },
        "DeviceIndex" : {
          "type" : "integer"
        },
        "Groups" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "Ipv6AddressCount" : {
          "type" : "integer"
        },
        "Ipv6Addresses" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/InstanceIpv6Address"
          }
        },
        "NetworkInterfaceId" : {
          "type" : "string"
        },
        "PrivateIpAddresses" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/PrivateIpAddressSpecification"
          }
        },
        "SecondaryPrivateIpAddressCount" : {
          "type" : "integer"
        },
        "SubnetId" : {
          "type" : "string"
        }
      }
    },
    "BlockDeviceMapping" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DeviceName" : {
          "type" : "string"
        },
        "Ebs" : {
          "$ref" : "#/definitions/EbsBlockDevice"
        },
        "NoDevice" : {
          "type" : "string"
        },
        "VirtualName" : {
          "type" : "string"
        }
      },
      "required" : [ "DeviceName" ]
    },
    "TargetGroupsConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TargetGroups" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/TargetGroup"
          }
        }
      },
      "required" : [ "TargetGroups" ]
    },
    "EbsBlockDevice" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DeleteOnTermination" : {
          "type" : "boolean"
        },
        "Encrypted" : {
          "type" : "boolean"
        },
        "Iops" : {
          "type" : "integer"
        },
        "SnapshotId" : {
          "type" : "string"
        },
        "VolumeSize" : {
          "type" : "integer"
        },
        "VolumeType" : {
          "type" : "string",
          "enum" : [ "gp2", "gp3", "io1", "io2", "sc1", "st1", "standard" ]
        }
      }
    },
    "TargetGroup" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Arn" : {
          "type" : "string"
        }
      },
      "required" : [ "Arn" ]
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
    "PrivateIpAddressSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Primary" : {
          "type" : "boolean"
        },
        "PrivateIpAddress" : {
          "type" : "string"
        }
      },
      "required" : [ "PrivateIpAddress" ]
    },
    "ClassicLoadBalancer" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "Name" ]
    },
    "InstanceIpv6Address" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Ipv6Address" : {
          "type" : "string"
        }
      },
      "required" : [ "Ipv6Address" ]
    },
    "InstanceRequirementsRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VCpuCount" : {
          "$ref" : "#/definitions/VCpuCountRangeRequest"
        },
        "MemoryMiB" : {
          "$ref" : "#/definitions/MemoryMiBRequest"
        },
        "CpuManufacturers" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string",
            "enum" : [ "intel", "amd", "amazon-web-services", "apple" ]
          }
        },
        "MemoryGiBPerVCpu" : {
          "$ref" : "#/definitions/MemoryGiBPerVCpuRequest"
        },
        "AllowedInstanceTypes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string",
            "minLength" : 1,
            "maxLength" : 30,
            "pattern" : "[a-zA-Z0-9\\.\\*]+"
          }
        },
        "ExcludedInstanceTypes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string",
            "minLength" : 1,
            "maxLength" : 30,
            "pattern" : "[a-zA-Z0-9\\.\\*]+"
          }
        },
        "InstanceGenerations" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string",
            "enum" : [ "current", "previous" ]
          }
        },
        "SpotMaxPricePercentageOverLowestPrice" : {
          "type" : "integer"
        },
        "OnDemandMaxPricePercentageOverLowestPrice" : {
          "type" : "integer"
        },
        "MaxSpotPriceAsPercentageOfOptimalOnDemandPrice" : {
          "type" : "integer"
        },
        "BareMetal" : {
          "type" : "string",
          "enum" : [ "included", "required", "excluded" ]
        },
        "BurstablePerformance" : {
          "type" : "string",
          "enum" : [ "included", "required", "excluded" ]
        },
        "RequireHibernateSupport" : {
          "type" : "boolean"
        },
        "NetworkBandwidthGbps" : {
          "$ref" : "#/definitions/NetworkBandwidthGbpsRequest"
        },
        "NetworkInterfaceCount" : {
          "$ref" : "#/definitions/NetworkInterfaceCountRequest"
        },
        "LocalStorage" : {
          "type" : "string",
          "enum" : [ "included", "required", "excluded" ]
        },
        "LocalStorageTypes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string",
            "enum" : [ "hdd", "ssd" ]
          }
        },
        "TotalLocalStorageGB" : {
          "$ref" : "#/definitions/TotalLocalStorageGBRequest"
        },
        "BaselineEbsBandwidthMbps" : {
          "$ref" : "#/definitions/BaselineEbsBandwidthMbpsRequest"
        },
        "AcceleratorTypes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string",
            "enum" : [ "gpu", "fpga", "inference" ]
          }
        },
        "AcceleratorCount" : {
          "$ref" : "#/definitions/AcceleratorCountRequest"
        },
        "AcceleratorManufacturers" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string",
            "enum" : [ "amazon-web-services", "amd", "habana", "nvidia", "xilinx" ]
          }
        },
        "AcceleratorNames" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string",
            "enum" : [ "a10g", "a100", "h100", "inferentia", "k520", "k80", "m60", "radeon-pro-v520", "t4", "t4g", "vu9p", "v100" ]
          }
        },
        "AcceleratorTotalMemoryMiB" : {
          "$ref" : "#/definitions/AcceleratorTotalMemoryMiBRequest"
        },
        "BaselinePerformanceFactors" : {
          "$ref" : "#/definitions/BaselinePerformanceFactorsRequest"
        }
      }
    },
    "VCpuCountRangeRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Min" : {
          "type" : "integer"
        },
        "Max" : {
          "type" : "integer"
        }
      }
    },
    "MemoryMiBRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Min" : {
          "type" : "integer"
        },
        "Max" : {
          "type" : "integer"
        }
      }
    },
    "MemoryGiBPerVCpuRequest" : {
      "type" : "object",
      "additionalProperties" : False,
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
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Min" : {
          "type" : "number"
        },
        "Max" : {
          "type" : "number"
        }
      }
    },
    "NetworkInterfaceCountRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Min" : {
          "type" : "integer"
        },
        "Max" : {
          "type" : "integer"
        }
      }
    },
    "TotalLocalStorageGBRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Min" : {
          "type" : "number"
        },
        "Max" : {
          "type" : "number"
        }
      }
    },
    "BaselineEbsBandwidthMbpsRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Min" : {
          "type" : "integer"
        },
        "Max" : {
          "type" : "integer"
        }
      }
    },
    "AcceleratorCountRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Min" : {
          "type" : "integer"
        },
        "Max" : {
          "type" : "integer"
        }
      }
    },
    "AcceleratorTotalMemoryMiBRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Min" : {
          "type" : "integer"
        },
        "Max" : {
          "type" : "integer"
        }
      }
    },
    "BaselinePerformanceFactorsRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Cpu" : {
          "$ref" : "#/definitions/CpuPerformanceFactorRequest"
        }
      }
    },
    "CpuPerformanceFactorRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "References" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/PerformanceFactorReferenceRequest"
          }
        }
      }
    },
    "PerformanceFactorReferenceRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "InstanceFamily" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "SpotFleetRequestConfigData" ],
  "createOnlyProperties" : [ "/properties/SpotFleetRequestConfigData/AllocationStrategy", "/properties/SpotFleetRequestConfigData/IamFleetRole", "/properties/SpotFleetRequestConfigData/InstanceInterruptionBehavior", "/properties/SpotFleetRequestConfigData/InstancePoolsToUseCount", "/properties/SpotFleetRequestConfigData/LaunchSpecifications", "/properties/SpotFleetRequestConfigData/LaunchTemplateConfigs", "/properties/SpotFleetRequestConfigData/LoadBalancersConfig", "/properties/SpotFleetRequestConfigData/OnDemandAllocationStrategy", "/properties/SpotFleetRequestConfigData/OnDemandMaxTotalPrice", "/properties/SpotFleetRequestConfigData/OnDemandTargetCapacity", "/properties/SpotFleetRequestConfigData/ReplaceUnhealthyInstances", "/properties/SpotFleetRequestConfigData/SpotMaintenanceStrategies", "/properties/SpotFleetRequestConfigData/SpotMaxTotalPrice", "/properties/SpotFleetRequestConfigData/SpotPrice", "/properties/SpotFleetRequestConfigData/TagSpecifications", "/properties/SpotFleetRequestConfigData/TerminateInstancesWithExpiration", "/properties/SpotFleetRequestConfigData/Type", "/properties/SpotFleetRequestConfigData/ValidFrom", "/properties/SpotFleetRequestConfigData/ValidUntil" ],
  "readOnlyProperties" : [ "/properties/Id" ],
  "writeOnlyProperties" : [ "/properties/SpotFleetRequestConfigData/TagSpecifications", "/properties/SpotFleetRequestConfigData/LaunchSpecifications/*/NetworkInterfaces/*/Groups" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iam:PassRole", "ec2:CreateTags", "ec2:RequestSpotFleet", "ec2:DescribeSpotFleetRequests", "ec2:RunInstances" ]
    },
    "delete" : {
      "permissions" : [ "ec2:DescribeSpotFleetRequests", "ec2:CancelSpotFleetRequests" ]
    },
    "list" : {
      "permissions" : [ "ec2:DescribeSpotFleetRequests" ]
    },
    "read" : {
      "permissions" : [ "ec2:DescribeSpotFleetRequests" ]
    },
    "update" : {
      "permissions" : [ "ec2:ModifySpotFleetRequest", "ec2:DescribeSpotFleetRequests" ]
    }
  }
}