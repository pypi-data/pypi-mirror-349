SCHEMA = {
  "typeName" : "AWS::EMR::Cluster",
  "description" : "Resource Type definition for AWS::EMR::Cluster",
  "additionalProperties" : False,
  "properties" : {
    "Steps" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/StepConfig"
      }
    },
    "PlacementGroupConfigs" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/PlacementGroupConfig"
      }
    },
    "StepConcurrencyLevel" : {
      "type" : "integer"
    },
    "EbsRootVolumeSize" : {
      "type" : "integer"
    },
    "OSReleaseLabel" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    },
    "ServiceRole" : {
      "type" : "string"
    },
    "LogUri" : {
      "type" : "string"
    },
    "BootstrapActions" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/BootstrapActionConfig"
      }
    },
    "MasterPublicDNS" : {
      "type" : "string"
    },
    "Configurations" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Configuration"
      }
    },
    "ReleaseLabel" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "ManagedScalingPolicy" : {
      "$ref" : "#/definitions/ManagedScalingPolicy"
    },
    "LogEncryptionKmsKeyId" : {
      "type" : "string"
    },
    "AdditionalInfo" : {
      "type" : "object"
    },
    "AutoTerminationPolicy" : {
      "$ref" : "#/definitions/AutoTerminationPolicy"
    },
    "KerberosAttributes" : {
      "$ref" : "#/definitions/KerberosAttributes"
    },
    "Applications" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Application"
      }
    },
    "AutoScalingRole" : {
      "type" : "string"
    },
    "CustomAmiId" : {
      "type" : "string"
    },
    "EbsRootVolumeIops" : {
      "type" : "integer"
    },
    "Instances" : {
      "$ref" : "#/definitions/JobFlowInstancesConfig"
    },
    "ScaleDownBehavior" : {
      "type" : "string"
    },
    "EbsRootVolumeThroughput" : {
      "type" : "integer"
    },
    "JobFlowRole" : {
      "type" : "string"
    },
    "VisibleToAllUsers" : {
      "type" : "boolean"
    },
    "SecurityConfiguration" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    }
  },
  "definitions" : {
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
    "KeyValue" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
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
    "StepConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "HadoopJarStep" : {
          "$ref" : "#/definitions/HadoopJarStepConfig"
        },
        "ActionOnFailure" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "HadoopJarStep", "Name" ]
    },
    "InstanceFleetConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TargetOnDemandCapacity" : {
          "type" : "integer"
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
      }
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
    },
    "ScriptBootstrapActionConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Path" : {
          "type" : "string"
        },
        "Args" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "Path" ]
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
    "SimpleScalingPolicyConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ScalingAdjustment" : {
          "type" : "integer"
        },
        "CoolDown" : {
          "type" : "integer"
        },
        "AdjustmentType" : {
          "type" : "string"
        }
      },
      "required" : [ "ScalingAdjustment" ]
    },
    "PlacementGroupConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "InstanceRole" : {
          "type" : "string"
        },
        "PlacementStrategy" : {
          "type" : "string"
        }
      },
      "required" : [ "InstanceRole" ]
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
    "ScalingTrigger" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CloudWatchAlarmDefinition" : {
          "$ref" : "#/definitions/CloudWatchAlarmDefinition"
        }
      },
      "required" : [ "CloudWatchAlarmDefinition" ]
    },
    "ManagedScalingPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ComputeLimits" : {
          "$ref" : "#/definitions/ComputeLimits"
        }
      }
    },
    "InstanceGroupConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AutoScalingPolicy" : {
          "$ref" : "#/definitions/AutoScalingPolicy"
        },
        "BidPrice" : {
          "type" : "string"
        },
        "InstanceCount" : {
          "type" : "integer"
        },
        "EbsConfiguration" : {
          "$ref" : "#/definitions/EbsConfiguration"
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
        },
        "Market" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "InstanceCount", "InstanceType" ]
    },
    "HadoopJarStepConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Args" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "MainClass" : {
          "type" : "string"
        },
        "Jar" : {
          "type" : "string"
        },
        "StepProperties" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/KeyValue"
          }
        }
      },
      "required" : [ "Jar" ]
    },
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
    "CloudWatchAlarmDefinition" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MetricName" : {
          "type" : "string"
        },
        "ComparisonOperator" : {
          "type" : "string"
        },
        "Statistic" : {
          "type" : "string"
        },
        "Dimensions" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/MetricDimension"
          }
        },
        "Period" : {
          "type" : "integer"
        },
        "EvaluationPeriods" : {
          "type" : "integer"
        },
        "Unit" : {
          "type" : "string"
        },
        "Namespace" : {
          "type" : "string"
        },
        "Threshold" : {
          "type" : "number"
        }
      },
      "required" : [ "MetricName", "ComparisonOperator", "Period", "Threshold" ]
    },
    "AutoTerminationPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IdleTimeout" : {
          "type" : "integer"
        }
      }
    },
    "KerberosAttributes" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "KdcAdminPassword" : {
          "type" : "string"
        },
        "Realm" : {
          "type" : "string"
        },
        "ADDomainJoinPassword" : {
          "type" : "string"
        },
        "ADDomainJoinUser" : {
          "type" : "string"
        },
        "CrossRealmTrustPrincipalPassword" : {
          "type" : "string"
        }
      },
      "required" : [ "KdcAdminPassword", "Realm" ]
    },
    "JobFlowInstancesConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MasterInstanceFleet" : {
          "$ref" : "#/definitions/InstanceFleetConfig"
        },
        "AdditionalSlaveSecurityGroups" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "CoreInstanceFleet" : {
          "$ref" : "#/definitions/InstanceFleetConfig"
        },
        "CoreInstanceGroup" : {
          "$ref" : "#/definitions/InstanceGroupConfig"
        },
        "Ec2SubnetIds" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "HadoopVersion" : {
          "type" : "string"
        },
        "TerminationProtected" : {
          "type" : "boolean"
        },
        "UnhealthyNodeReplacement" : {
          "type" : "boolean"
        },
        "KeepJobFlowAliveWhenNoSteps" : {
          "type" : "boolean"
        },
        "Ec2KeyName" : {
          "type" : "string"
        },
        "MasterInstanceGroup" : {
          "$ref" : "#/definitions/InstanceGroupConfig"
        },
        "Placement" : {
          "$ref" : "#/definitions/PlacementType"
        },
        "TaskInstanceFleets" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/InstanceFleetConfig"
          }
        },
        "Ec2SubnetId" : {
          "type" : "string"
        },
        "TaskInstanceGroups" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/InstanceGroupConfig"
          }
        },
        "ServiceAccessSecurityGroup" : {
          "type" : "string"
        },
        "EmrManagedSlaveSecurityGroup" : {
          "type" : "string"
        },
        "AdditionalMasterSecurityGroups" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "EmrManagedMasterSecurityGroup" : {
          "type" : "string"
        }
      }
    },
    "ScalingAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Market" : {
          "type" : "string"
        },
        "SimpleScalingPolicyConfiguration" : {
          "$ref" : "#/definitions/SimpleScalingPolicyConfiguration"
        }
      },
      "required" : [ "SimpleScalingPolicyConfiguration" ]
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
    "ScalingRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Action" : {
          "$ref" : "#/definitions/ScalingAction"
        },
        "Description" : {
          "type" : "string"
        },
        "Trigger" : {
          "$ref" : "#/definitions/ScalingTrigger"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "Action", "Trigger", "Name" ]
    },
    "ComputeLimits" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaximumOnDemandCapacityUnits" : {
          "type" : "integer"
        },
        "MaximumCapacityUnits" : {
          "type" : "integer"
        },
        "MaximumCoreCapacityUnits" : {
          "type" : "integer"
        },
        "MinimumCapacityUnits" : {
          "type" : "integer"
        },
        "UnitType" : {
          "type" : "string"
        }
      },
      "required" : [ "UnitType", "MaximumCapacityUnits", "MinimumCapacityUnits" ]
    },
    "MetricDimension" : {
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
    "BootstrapActionConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ScriptBootstrapAction" : {
          "$ref" : "#/definitions/ScriptBootstrapActionConfig"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "ScriptBootstrapAction", "Name" ]
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
    "AutoScalingPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Rules" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/ScalingRule"
          }
        },
        "Constraints" : {
          "$ref" : "#/definitions/ScalingConstraints"
        }
      },
      "required" : [ "Constraints", "Rules" ]
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
    "PlacementType" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AvailabilityZone" : {
          "type" : "string"
        }
      },
      "required" : [ "AvailabilityZone" ]
    },
    "ScalingConstraints" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MinCapacity" : {
          "type" : "integer"
        },
        "MaxCapacity" : {
          "type" : "integer"
        }
      },
      "required" : [ "MinCapacity", "MaxCapacity" ]
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
    "Application" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AdditionalInfo" : {
          "type" : "object",
          "patternProperties" : {
            "[a-zA-Z0-9]+" : {
              "type" : "string"
            }
          }
        },
        "Args" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "Version" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "Instances", "ServiceRole", "JobFlowRole", "Name" ],
  "createOnlyProperties" : [ "/properties/Steps", "/properties/EbsRootVolumeSize", "/properties/SecurityConfiguration", "/properties/ScaleDownBehavior", "/properties/Configurations", "/properties/ReleaseLabel", "/properties/BootstrapActions", "/properties/EbsRootVolumeIops", "/properties/KerberosAttributes", "/properties/ServiceRole", "/properties/LogEncryptionKmsKeyId", "/properties/Name", "/properties/EbsRootVolumeThroughput", "/properties/JobFlowRole", "/properties/AdditionalInfo", "/properties/LogUri", "/properties/CustomAmiId", "/properties/PlacementGroupConfigs", "/properties/OSReleaseLabel", "/properties/AutoScalingRole", "/properties/Applications" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/MasterPublicDNS" ]
}