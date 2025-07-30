SCHEMA = {
  "typeName" : "AWS::Batch::JobDefinition",
  "description" : "Resource Type definition for AWS::Batch::JobDefinition",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : {
    "ContainerProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Command" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : True,
          "items" : {
            "type" : "string"
          }
        },
        "Environment" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : True,
          "items" : {
            "$ref" : "#/definitions/Environment"
          }
        },
        "Image" : {
          "type" : "string"
        },
        "JobRoleArn" : {
          "type" : "string"
        },
        "Memory" : {
          "type" : "integer"
        },
        "MountPoints" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/MountPoint"
          }
        },
        "Privileged" : {
          "type" : "boolean"
        },
        "ReadonlyRootFilesystem" : {
          "type" : "boolean"
        },
        "Ulimits" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Ulimit"
          }
        },
        "User" : {
          "type" : "string"
        },
        "Vcpus" : {
          "type" : "integer"
        },
        "Volumes" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Volume"
          }
        },
        "ResourceRequirements" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/ResourceRequirement"
          }
        },
        "LinuxParameters" : {
          "$ref" : "#/definitions/LinuxParameters"
        },
        "LogConfiguration" : {
          "$ref" : "#/definitions/LogConfiguration"
        },
        "ExecutionRoleArn" : {
          "type" : "string"
        },
        "Secrets" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Secret"
          }
        },
        "NetworkConfiguration" : {
          "$ref" : "#/definitions/NetworkConfiguration"
        },
        "FargatePlatformConfiguration" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "PlatformVersion" : {
              "type" : "string"
            }
          }
        },
        "EphemeralStorage" : {
          "$ref" : "#/definitions/EphemeralStorage"
        },
        "RuntimePlatform" : {
          "$ref" : "#/definitions/RuntimePlatform"
        },
        "RepositoryCredentials" : {
          "$ref" : "#/definitions/RepositoryCredentials"
        },
        "EnableExecuteCommand" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Image" ]
    },
    "MultiNodeContainerProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Command" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : True,
          "items" : {
            "type" : "string"
          }
        },
        "Environment" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : True,
          "items" : {
            "$ref" : "#/definitions/Environment"
          }
        },
        "Image" : {
          "type" : "string"
        },
        "JobRoleArn" : {
          "type" : "string"
        },
        "Memory" : {
          "type" : "integer"
        },
        "MountPoints" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/MountPoint"
          }
        },
        "Privileged" : {
          "type" : "boolean"
        },
        "ReadonlyRootFilesystem" : {
          "type" : "boolean"
        },
        "Ulimits" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Ulimit"
          }
        },
        "User" : {
          "type" : "string"
        },
        "Vcpus" : {
          "type" : "integer"
        },
        "Volumes" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Volume"
          }
        },
        "InstanceType" : {
          "type" : "string"
        },
        "ResourceRequirements" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/ResourceRequirement"
          }
        },
        "LinuxParameters" : {
          "$ref" : "#/definitions/LinuxParameters"
        },
        "LogConfiguration" : {
          "$ref" : "#/definitions/LogConfiguration"
        },
        "ExecutionRoleArn" : {
          "type" : "string"
        },
        "Secrets" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Secret"
          }
        },
        "EphemeralStorage" : {
          "$ref" : "#/definitions/EphemeralStorage"
        },
        "RuntimePlatform" : {
          "$ref" : "#/definitions/RuntimePlatform"
        },
        "RepositoryCredentials" : {
          "$ref" : "#/definitions/RepositoryCredentials"
        },
        "EnableExecuteCommand" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Image" ]
    },
    "EphemeralStorage" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SizeInGiB" : {
          "type" : "integer"
        }
      },
      "required" : [ "SizeInGiB" ]
    },
    "LinuxParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Devices" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Device"
          }
        },
        "InitProcessEnabled" : {
          "type" : "boolean"
        },
        "MaxSwap" : {
          "type" : "integer"
        },
        "Swappiness" : {
          "type" : "integer"
        },
        "SharedMemorySize" : {
          "type" : "integer"
        },
        "Tmpfs" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Tmpfs"
          }
        }
      }
    },
    "LogConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "LogDriver" : {
          "type" : "string"
        },
        "Options" : {
          "type" : "object",
          "additionalProperties" : False,
          "patternProperties" : {
            ".*" : {
              "type" : "string"
            }
          }
        },
        "SecretOptions" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Secret"
          }
        }
      },
      "required" : [ "LogDriver" ]
    },
    "RuntimePlatform" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OperatingSystemFamily" : {
          "type" : "string"
        },
        "CpuArchitecture" : {
          "type" : "string"
        }
      }
    },
    "NetworkConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AssignPublicIp" : {
          "type" : "string"
        }
      }
    },
    "RepositoryCredentials" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CredentialsParameter" : {
          "type" : "string"
        }
      },
      "required" : [ "CredentialsParameter" ]
    },
    "Environment" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      }
    },
    "MountPoint" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ContainerPath" : {
          "type" : "string"
        },
        "ReadOnly" : {
          "type" : "boolean"
        },
        "SourceVolume" : {
          "type" : "string"
        }
      }
    },
    "Ulimit" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "HardLimit" : {
          "type" : "integer"
        },
        "Name" : {
          "type" : "string"
        },
        "SoftLimit" : {
          "type" : "integer"
        }
      },
      "required" : [ "HardLimit", "Name", "SoftLimit" ]
    },
    "Volume" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Host" : {
          "$ref" : "#/definitions/Host"
        },
        "EfsVolumeConfiguration" : {
          "$ref" : "#/definitions/EFSVolumeConfiguration"
        },
        "Name" : {
          "type" : "string"
        }
      }
    },
    "Host" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SourcePath" : {
          "type" : "string"
        }
      }
    },
    "EFSVolumeConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "FileSystemId" : {
          "type" : "string"
        },
        "RootDirectory" : {
          "type" : "string"
        },
        "TransitEncryption" : {
          "type" : "string"
        },
        "TransitEncryptionPort" : {
          "type" : "integer"
        },
        "AuthorizationConfig" : {
          "$ref" : "#/definitions/EFSAuthorizationConfig"
        }
      },
      "required" : [ "FileSystemId" ]
    },
    "EFSAuthorizationConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AccessPointId" : {
          "type" : "string"
        },
        "Iam" : {
          "type" : "string"
        }
      }
    },
    "ResourceRequirement" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      }
    },
    "Device" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "HostPath" : {
          "type" : "string"
        },
        "ContainerPath" : {
          "type" : "string"
        },
        "Permissions" : {
          "type" : "array",
          "insertionOrder" : False,
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "Tmpfs" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ContainerPath" : {
          "type" : "string"
        },
        "Size" : {
          "type" : "integer"
        },
        "MountOptions" : {
          "type" : "array",
          "insertionOrder" : False,
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "ContainerPath", "Size" ]
    },
    "Secret" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "ValueFrom" : {
          "type" : "string"
        }
      },
      "required" : [ "Name", "ValueFrom" ]
    },
    "EksProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PodProperties" : {
          "$ref" : "#/definitions/EksPodProperties"
        }
      }
    },
    "EksPodProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ServiceAccountName" : {
          "type" : "string"
        },
        "HostNetwork" : {
          "type" : "boolean"
        },
        "DnsPolicy" : {
          "type" : "string"
        },
        "InitContainers" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/EksContainer"
          }
        },
        "Containers" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/EksContainer"
          }
        },
        "Volumes" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/EksVolume"
          }
        },
        "ImagePullSecrets" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/ImagePullSecret"
          }
        },
        "Metadata" : {
          "$ref" : "#/definitions/EksMetadata"
        },
        "ShareProcessNamespace" : {
          "type" : "boolean"
        }
      }
    },
    "EksContainer" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "Image" : {
          "type" : "string"
        },
        "ImagePullPolicy" : {
          "type" : "string"
        },
        "Command" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Args" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Env" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/EksContainerEnvironmentVariable"
          }
        },
        "Resources" : {
          "$ref" : "#/definitions/EksContainerResourceRequirements"
        },
        "VolumeMounts" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/EksContainerVolumeMount"
          }
        },
        "SecurityContext" : {
          "$ref" : "#/definitions/EksContainerSecurityContext"
        }
      },
      "required" : [ "Image" ]
    },
    "EksContainerEnvironmentVariable" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "required" : [ "Name" ]
    },
    "EksContainerResourceRequirements" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Limits" : {
          "type" : "object",
          "additionalProperties" : False,
          "patternProperties" : {
            ".*" : {
              "type" : "string"
            }
          }
        },
        "Requests" : {
          "type" : "object",
          "additionalProperties" : False,
          "patternProperties" : {
            ".*" : {
              "type" : "string"
            }
          }
        }
      }
    },
    "EksContainerSecurityContext" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RunAsUser" : {
          "type" : "integer"
        },
        "RunAsGroup" : {
          "type" : "integer"
        },
        "Privileged" : {
          "type" : "boolean"
        },
        "AllowPrivilegeEscalation" : {
          "type" : "boolean"
        },
        "ReadOnlyRootFilesystem" : {
          "type" : "boolean"
        },
        "RunAsNonRoot" : {
          "type" : "boolean"
        }
      }
    },
    "EksVolume" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "HostPath" : {
          "$ref" : "#/definitions/EksHostPath"
        },
        "EmptyDir" : {
          "$ref" : "#/definitions/EksEmptyDir"
        },
        "Secret" : {
          "$ref" : "#/definitions/EksSecret"
        },
        "PersistentVolumeClaim" : {
          "$ref" : "#/definitions/EksPersistentVolumeClaim"
        }
      },
      "required" : [ "Name" ]
    },
    "EksHostPath" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Path" : {
          "type" : "string"
        }
      }
    },
    "EksEmptyDir" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Medium" : {
          "type" : "string"
        },
        "SizeLimit" : {
          "type" : "string"
        }
      }
    },
    "EksSecret" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecretName" : {
          "type" : "string"
        },
        "Optional" : {
          "type" : "boolean"
        }
      },
      "required" : [ "SecretName" ]
    },
    "EksPersistentVolumeClaim" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ClaimName" : {
          "type" : "string"
        },
        "ReadOnly" : {
          "type" : "boolean"
        }
      },
      "required" : [ "ClaimName" ]
    },
    "EksContainerVolumeMount" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "MountPath" : {
          "type" : "string"
        },
        "SubPath" : {
          "type" : "string"
        },
        "ReadOnly" : {
          "type" : "boolean"
        }
      }
    },
    "EksMetadata" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Labels" : {
          "type" : "object",
          "additionalProperties" : False,
          "patternProperties" : {
            ".*" : {
              "type" : "string"
            }
          }
        },
        "Annotations" : {
          "type" : "object",
          "additionalProperties" : False,
          "patternProperties" : {
            ".*" : {
              "type" : "string"
            }
          }
        },
        "Namespace" : {
          "type" : "string"
        }
      }
    },
    "ImagePullSecret" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        }
      }
    },
    "RetryStrategy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Attempts" : {
          "type" : "integer"
        },
        "EvaluateOnExit" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/EvaluateOnExit"
          }
        }
      }
    },
    "EvaluateOnExit" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OnExitCode" : {
          "type" : "string"
        },
        "OnStatusReason" : {
          "type" : "string"
        },
        "OnReason" : {
          "type" : "string"
        },
        "Action" : {
          "type" : "string"
        }
      },
      "required" : [ "Action" ]
    },
    "NodeProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "NumNodes" : {
          "type" : "integer"
        },
        "MainNode" : {
          "type" : "integer"
        },
        "NodeRangeProperties" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/NodeRangeProperty"
          }
        }
      },
      "required" : [ "NumNodes", "MainNode", "NodeRangeProperties" ]
    },
    "NodeRangeProperty" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TargetNodes" : {
          "type" : "string"
        },
        "Container" : {
          "$ref" : "#/definitions/MultiNodeContainerProperties"
        },
        "EcsProperties" : {
          "$ref" : "#/definitions/MultiNodeEcsProperties"
        },
        "EksProperties" : {
          "$ref" : "#/definitions/EksProperties"
        },
        "ConsumableResourceProperties" : {
          "$ref" : "#/definitions/ConsumableResourceProperties"
        },
        "InstanceTypes" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "TargetNodes" ]
    },
    "JobTimeout" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AttemptDurationSeconds" : {
          "type" : "integer"
        }
      }
    },
    "EcsProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TaskProperties" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/EcsTaskProperties"
          }
        }
      },
      "required" : [ "TaskProperties" ]
    },
    "EcsTaskProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Containers" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/TaskContainerProperties"
          }
        },
        "EphemeralStorage" : {
          "$ref" : "#/definitions/EphemeralStorage"
        },
        "ExecutionRoleArn" : {
          "type" : "string"
        },
        "RuntimePlatform" : {
          "$ref" : "#/definitions/RuntimePlatform"
        },
        "NetworkConfiguration" : {
          "$ref" : "#/definitions/NetworkConfiguration"
        },
        "Volumes" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Volume"
          }
        },
        "PidMode" : {
          "type" : "string"
        },
        "IpcMode" : {
          "type" : "string"
        },
        "PlatformVersion" : {
          "type" : "string"
        },
        "TaskRoleArn" : {
          "type" : "string"
        },
        "EnableExecuteCommand" : {
          "type" : "boolean"
        }
      }
    },
    "MultiNodeEcsProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TaskProperties" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/MultiNodeEcsTaskProperties"
          }
        }
      },
      "required" : [ "TaskProperties" ]
    },
    "MultiNodeEcsTaskProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Containers" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/TaskContainerProperties"
          }
        },
        "ExecutionRoleArn" : {
          "type" : "string"
        },
        "Volumes" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Volume"
          }
        },
        "PidMode" : {
          "type" : "string"
        },
        "IpcMode" : {
          "type" : "string"
        },
        "TaskRoleArn" : {
          "type" : "string"
        },
        "EnableExecuteCommand" : {
          "type" : "boolean"
        }
      }
    },
    "TaskContainerProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Command" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : True,
          "items" : {
            "type" : "string"
          }
        },
        "Environment" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : True,
          "items" : {
            "$ref" : "#/definitions/Environment"
          }
        },
        "DependsOn" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/TaskContainerDependency"
          }
        },
        "Name" : {
          "type" : "string"
        },
        "Image" : {
          "type" : "string"
        },
        "LinuxParameters" : {
          "$ref" : "#/definitions/LinuxParameters"
        },
        "LogConfiguration" : {
          "$ref" : "#/definitions/LogConfiguration"
        },
        "MountPoints" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/MountPoint"
          }
        },
        "Essential" : {
          "type" : "boolean"
        },
        "Privileged" : {
          "type" : "boolean"
        },
        "ReadonlyRootFilesystem" : {
          "type" : "boolean"
        },
        "Ulimits" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Ulimit"
          }
        },
        "User" : {
          "type" : "string"
        },
        "Secrets" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Secret"
          }
        },
        "RepositoryCredentials" : {
          "$ref" : "#/definitions/RepositoryCredentials"
        },
        "ResourceRequirements" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/ResourceRequirement"
          }
        },
        "FirelensConfiguration" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "Type" : {
              "type" : "string"
            },
            "Options" : {
              "type" : "object",
              "additionalProperties" : False,
              "patternProperties" : {
                ".*" : {
                  "type" : "string"
                }
              }
            }
          },
          "required" : [ "Type" ]
        }
      },
      "required" : [ "Image" ]
    },
    "TaskContainerDependency" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ContainerName" : {
          "type" : "string"
        },
        "Condition" : {
          "type" : "string"
        }
      },
      "required" : [ "ContainerName", "Condition" ]
    },
    "ConsumableResourceRequirement" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ConsumableResource" : {
          "type" : "string",
          "description" : "The ARN of the consumable resource the job definition should consume.",
          "pattern" : "arn:[a-z0-9-\\.]{1,63}:[a-z0-9-\\.]{0,63}:[a-z0-9-\\.]{0,63}:[a-z0-9-\\.]{0,63}:[^/].{0,1023}"
        },
        "Quantity" : {
          "type" : "integer",
          "format" : "int64"
        }
      },
      "required" : [ "ConsumableResource", "Quantity" ]
    },
    "ConsumableResourceProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ConsumableResourceList" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/ConsumableResourceRequirement"
          }
        }
      },
      "required" : [ "ConsumableResourceList" ]
    }
  },
  "properties" : {
    "ContainerProperties" : {
      "$ref" : "#/definitions/ContainerProperties"
    },
    "EcsProperties" : {
      "$ref" : "#/definitions/EcsProperties"
    },
    "NodeProperties" : {
      "$ref" : "#/definitions/NodeProperties"
    },
    "JobDefinitionName" : {
      "type" : "string",
      "maxLength" : 128
    },
    "JobDefinitionArn" : {
      "type" : "string"
    },
    "SchedulingPriority" : {
      "type" : "integer"
    },
    "Parameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "patternProperties" : {
        ".*" : {
          "type" : "string"
        }
      }
    },
    "PlatformCapabilities" : {
      "type" : "array",
      "insertionOrder" : True,
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "PropagateTags" : {
      "type" : "boolean"
    },
    "RetryStrategy" : {
      "$ref" : "#/definitions/RetryStrategy"
    },
    "Timeout" : {
      "$ref" : "#/definitions/JobTimeout"
    },
    "Type" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "object",
      "additionalProperties" : False,
      "description" : "A key-value pair to associate with a resource.",
      "patternProperties" : {
        ".*" : {
          "type" : "string"
        }
      }
    },
    "EksProperties" : {
      "$ref" : "#/definitions/EksProperties"
    },
    "ConsumableResourceProperties" : {
      "$ref" : "#/definitions/ConsumableResourceProperties"
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "Batch:TagResource", "Batch:UnTagResource" ]
  },
  "additionalProperties" : False,
  "required" : [ "Type" ],
  "createOnlyProperties" : [ "/properties/JobDefinitionName" ],
  "readOnlyProperties" : [ "/properties/JobDefinitionArn" ],
  "primaryIdentifier" : [ "/properties/JobDefinitionName" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "Batch:RegisterJobDefinition", "Batch:TagResource", "Batch:DescribeJobDefinitions", "Iam:PassRole" ]
    },
    "read" : {
      "permissions" : [ "Batch:DescribeJobDefinitions" ]
    },
    "update" : {
      "permissions" : [ "Batch:DescribeJobDefinitions", "Batch:RegisterJobDefinition", "Batch:DeregisterJobDefinition", "Batch:TagResource", "Batch:UntagResource", "Iam:PassRole" ]
    },
    "delete" : {
      "permissions" : [ "Batch:DescribeJobDefinitions", "Batch:DeregisterJobDefinition", "Iam:PassRole" ]
    },
    "list" : {
      "permissions" : [ "Batch:DescribeJobDefinitions" ]
    }
  }
}