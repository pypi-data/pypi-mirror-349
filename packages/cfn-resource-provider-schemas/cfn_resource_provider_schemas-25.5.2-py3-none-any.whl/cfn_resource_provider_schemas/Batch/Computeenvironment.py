SCHEMA = {
  "typeName" : "AWS::Batch::ComputeEnvironment",
  "description" : "Resource Type definition for AWS::Batch::ComputeEnvironment",
  "additionalProperties" : False,
  "properties" : {
    "ComputeEnvironmentArn" : {
      "type" : "string"
    },
    "ComputeEnvironmentName" : {
      "type" : "string"
    },
    "ComputeResources" : {
      "$ref" : "#/definitions/ComputeResources"
    },
    "ReplaceComputeEnvironment" : {
      "type" : "boolean",
      "default" : True
    },
    "ServiceRole" : {
      "type" : "string"
    },
    "State" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "object",
      "description" : "A key-value pair to associate with a resource.",
      "patternProperties" : {
        ".*" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "Type" : {
      "type" : "string"
    },
    "UpdatePolicy" : {
      "$ref" : "#/definitions/UpdatePolicy"
    },
    "UnmanagedvCpus" : {
      "type" : "integer"
    },
    "EksConfiguration" : {
      "$ref" : "#/definitions/EksConfiguration"
    },
    "Context" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "ComputeResources" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AllocationStrategy" : {
          "type" : "string"
        },
        "BidPercentage" : {
          "type" : "integer"
        },
        "DesiredvCpus" : {
          "type" : "integer"
        },
        "Ec2Configuration" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Ec2ConfigurationObject"
          }
        },
        "Ec2KeyPair" : {
          "type" : "string"
        },
        "ImageId" : {
          "type" : "string"
        },
        "InstanceRole" : {
          "type" : "string"
        },
        "InstanceTypes" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        },
        "LaunchTemplate" : {
          "$ref" : "#/definitions/LaunchTemplateSpecification"
        },
        "MaxvCpus" : {
          "type" : "integer"
        },
        "MinvCpus" : {
          "type" : "integer"
        },
        "PlacementGroup" : {
          "type" : "string"
        },
        "SecurityGroupIds" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        },
        "SpotIamFleetRole" : {
          "type" : "string"
        },
        "Subnets" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Tags" : {
          "type" : "object",
          "description" : "A key-value pair to associate with a resource.",
          "patternProperties" : {
            ".*" : {
              "type" : "string"
            }
          },
          "additionalProperties" : False
        },
        "Type" : {
          "type" : "string"
        },
        "UpdateToLatestImageVersion" : {
          "type" : "boolean",
          "default" : False
        }
      },
      "required" : [ "Subnets", "Type", "MaxvCpus" ]
    },
    "Ec2ConfigurationObject" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ImageIdOverride" : {
          "type" : "string"
        },
        "ImageType" : {
          "type" : "string"
        },
        "ImageKubernetesVersion" : {
          "type" : "string"
        }
      },
      "required" : [ "ImageType" ]
    },
    "LaunchTemplateSpecification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "LaunchTemplateId" : {
          "type" : "string"
        },
        "LaunchTemplateName" : {
          "type" : "string"
        },
        "Version" : {
          "type" : "string"
        },
        "Overrides" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/LaunchTemplateSpecificationOverride"
          }
        }
      }
    },
    "LaunchTemplateSpecificationOverride" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "LaunchTemplateId" : {
          "type" : "string"
        },
        "LaunchTemplateName" : {
          "type" : "string"
        },
        "Version" : {
          "type" : "string"
        },
        "TargetInstanceTypes" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "UpdatePolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TerminateJobsOnUpdate" : {
          "type" : "boolean",
          "default" : False
        },
        "JobExecutionTimeoutMinutes" : {
          "type" : "integer",
          "default" : 30
        }
      }
    },
    "EksConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "EksClusterArn" : {
          "type" : "string",
          "default" : False
        },
        "KubernetesNamespace" : {
          "type" : "string",
          "default" : False
        }
      },
      "required" : [ "EksClusterArn", "KubernetesNamespace" ]
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "Batch:TagResource", "Batch:UnTagResource" ]
  },
  "required" : [ "Type" ],
  "createOnlyProperties" : [ "/properties/ComputeResources/SpotIamFleetRole", "/properties/ComputeEnvironmentName", "/properties/Tags", "/properties/Type", "/properties/EksConfiguration" ],
  "conditionalCreateOnlyProperties" : [ "/properties/ComputeResources/AllocationStrategy", "/properties/ComputeResources/BidPercentage", "/properties/ComputeResources/Ec2Configuration", "/properties/ComputeResources/Ec2KeyPair", "/properties/ComputeResources/ImageId", "/properties/ComputeResources/InstanceRole", "/properties/ComputeResources/InstanceTypes", "/properties/ComputeResources/LaunchTemplate", "/properties/ComputeResources/PlacementGroup", "/properties/ComputeResources/SecurityGroupIds", "/properties/ComputeResources/Subnets", "/properties/ComputeResources/Tags", "/properties/ComputeResources/Type" ],
  "writeOnlyProperties" : [ "/properties/ComputeResources/UpdateToLatestImageVersion", "/properties/ReplaceComputeEnvironment", "/properties/UpdatePolicy" ],
  "primaryIdentifier" : [ "/properties/ComputeEnvironmentArn" ],
  "readOnlyProperties" : [ "/properties/ComputeEnvironmentArn" ],
  "additionalIdentifiers" : [ [ "/properties/ComputeEnvironmentName" ] ],
  "handlers" : {
    "create" : {
      "permissions" : [ "Batch:CreateComputeEnvironment", "Batch:TagResource", "Batch:DescribeComputeEnvironments", "iam:CreateServiceLinkedRole", "Iam:PassRole", "Eks:DescribeCluster" ]
    },
    "read" : {
      "permissions" : [ "Batch:DescribeComputeEnvironments" ]
    },
    "update" : {
      "permissions" : [ "Batch:UpdateComputeEnvironment", "Batch:DescribeComputeEnvironments", "Batch:TagResource", "Batch:UnTagResource", "Iam:PassRole", "Eks:DescribeCluster" ]
    },
    "delete" : {
      "permissions" : [ "Batch:DeleteComputeEnvironment", "Batch:DescribeComputeEnvironments", "Batch:UpdateComputeEnvironment", "Iam:PassRole", "Eks:DescribeCluster" ]
    },
    "list" : {
      "permissions" : [ "Batch:DescribeComputeEnvironments" ]
    }
  }
}