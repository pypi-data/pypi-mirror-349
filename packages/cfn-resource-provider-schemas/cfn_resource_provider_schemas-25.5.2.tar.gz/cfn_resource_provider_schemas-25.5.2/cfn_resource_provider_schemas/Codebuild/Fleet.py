SCHEMA = {
  "typeName" : "AWS::CodeBuild::Fleet",
  "description" : "Resource Type definition for AWS::CodeBuild::Fleet",
  "additionalProperties" : False,
  "properties" : {
    "Name" : {
      "type" : "string",
      "minLength" : 2,
      "maxLength" : 128
    },
    "BaseCapacity" : {
      "type" : "integer",
      "minimum" : 1
    },
    "EnvironmentType" : {
      "type" : "string",
      "enum" : [ "WINDOWS_SERVER_2019_CONTAINER", "WINDOWS_SERVER_2022_CONTAINER", "LINUX_CONTAINER", "LINUX_GPU_CONTAINER", "ARM_CONTAINER", "MAC_ARM", "LINUX_EC2", "ARM_EC2", "WINDOWS_EC2" ]
    },
    "ComputeType" : {
      "type" : "string",
      "enum" : [ "BUILD_GENERAL1_SMALL", "BUILD_GENERAL1_MEDIUM", "BUILD_GENERAL1_LARGE", "BUILD_GENERAL1_XLARGE", "BUILD_GENERAL1_2XLARGE", "ATTRIBUTE_BASED_COMPUTE", "CUSTOM_INSTANCE_TYPE" ]
    },
    "OverflowBehavior" : {
      "type" : "string",
      "enum" : [ "QUEUE", "ON_DEMAND" ]
    },
    "FleetServiceRole" : {
      "type" : "string",
      "pattern" : "^(?:arn:)[a-zA-Z+-=,._:/@]+$"
    },
    "FleetVpcConfig" : {
      "$ref" : "#/definitions/VpcConfig"
    },
    "FleetProxyConfiguration" : {
      "$ref" : "#/definitions/ProxyConfiguration"
    },
    "Tags" : {
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "Arn" : {
      "type" : "string",
      "minLength" : 1
    },
    "ImageId" : {
      "type" : "string",
      "pattern" : "^((aws/codebuild/[A-Za-z-]+:[0-9]+(-[0-9._]+)?)|ami-[a-z0-9]{1,1020})$"
    },
    "ScalingConfiguration" : {
      "$ref" : "#/definitions/ScalingConfigurationInput"
    },
    "ComputeConfiguration" : {
      "$ref" : "#/definitions/ComputeConfiguration"
    }
  },
  "definitions" : {
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "type" : "string",
          "description" : "The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. ",
          "minLength" : 1,
          "maxLength" : 128,
          "pattern" : "^(?!aws:)[a-zA-Z+-=._:/]+$"
        },
        "Value" : {
          "type" : "string",
          "description" : "The value for the tag. You can specify a value that is 0 to 255 Unicode characters in length. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. ",
          "minLength" : 0,
          "maxLength" : 256,
          "pattern" : "[a-zA-Z+-=._:/]+$"
        }
      },
      "required" : [ "Value", "Key" ]
    },
    "VpcConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VpcId" : {
          "type" : "string"
        },
        "Subnets" : {
          "type" : "array",
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        },
        "SecurityGroupIds" : {
          "type" : "array",
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "ProxyConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DefaultBehavior" : {
          "type" : "string",
          "enum" : [ "ALLOW_ALL", "DENY_ALL" ]
        },
        "OrderedProxyRules" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "$ref" : "#/definitions/FleetProxyRule"
          }
        }
      }
    },
    "FleetProxyRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string",
          "enum" : [ "DOMAIN", "IP" ]
        },
        "Effect" : {
          "type" : "string",
          "enum" : [ "ALLOW", "DENY" ]
        },
        "Entities" : {
          "type" : "array",
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "ScalingConfigurationInput" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxCapacity" : {
          "type" : "integer",
          "minimum" : 1
        },
        "ScalingType" : {
          "type" : "string",
          "enum" : [ "TARGET_TRACKING_SCALING" ]
        },
        "TargetTrackingScalingConfigs" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/TargetTrackingScalingConfiguration"
          }
        }
      }
    },
    "TargetTrackingScalingConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MetricType" : {
          "type" : "string",
          "enum" : [ "FLEET_UTILIZATION_RATE" ]
        },
        "TargetValue" : {
          "type" : "number"
        }
      }
    },
    "ComputeConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "vCpu" : {
          "type" : "integer"
        },
        "memory" : {
          "type" : "integer"
        },
        "disk" : {
          "type" : "integer"
        },
        "machineType" : {
          "type" : "string",
          "enum" : [ "GENERAL", "NVME" ]
        },
        "instanceType" : {
          "type" : "string"
        }
      }
    }
  },
  "primaryIdentifier" : [ "/properties/Arn" ],
  "readOnlyProperties" : [ "/properties/Arn" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "codebuild:CreateFleet", "codebuild:UpdateFleet" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "codebuild:BatchGetFleets", "codebuild:CreateFleet", "iam:PassRole" ]
    },
    "delete" : {
      "permissions" : [ "codebuild:BatchGetFleets", "codebuild:DeleteFleet" ]
    },
    "read" : {
      "permissions" : [ "codebuild:BatchGetFleets" ]
    },
    "list" : {
      "permissions" : [ "codebuild:ListFleets" ]
    },
    "update" : {
      "permissions" : [ "codebuild:BatchGetFleets", "codebuild:UpdateFleet", "iam:PassRole" ]
    }
  }
}