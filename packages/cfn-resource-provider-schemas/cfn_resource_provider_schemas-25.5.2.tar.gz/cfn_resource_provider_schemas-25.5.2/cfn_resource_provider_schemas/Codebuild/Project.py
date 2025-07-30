SCHEMA = {
  "typeName" : "AWS::CodeBuild::Project",
  "description" : "Resource Type definition for AWS::CodeBuild::Project",
  "additionalProperties" : False,
  "properties" : {
    "Description" : {
      "type" : "string"
    },
    "ResourceAccessRole" : {
      "type" : "string"
    },
    "VpcConfig" : {
      "$ref" : "#/definitions/VpcConfig"
    },
    "SecondarySources" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Source"
      }
    },
    "EncryptionKey" : {
      "type" : "string"
    },
    "SecondaryArtifacts" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Artifacts"
      }
    },
    "Source" : {
      "$ref" : "#/definitions/Source"
    },
    "Name" : {
      "type" : "string"
    },
    "LogsConfig" : {
      "$ref" : "#/definitions/LogsConfig"
    },
    "ServiceRole" : {
      "type" : "string"
    },
    "QueuedTimeoutInMinutes" : {
      "type" : "integer"
    },
    "SecondarySourceVersions" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/ProjectSourceVersion"
      }
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "AutoRetryLimit" : {
      "type" : "integer"
    },
    "SourceVersion" : {
      "type" : "string"
    },
    "Triggers" : {
      "$ref" : "#/definitions/ProjectTriggers"
    },
    "Artifacts" : {
      "$ref" : "#/definitions/Artifacts"
    },
    "BadgeEnabled" : {
      "type" : "boolean"
    },
    "FileSystemLocations" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/ProjectFileSystemLocation"
      }
    },
    "Environment" : {
      "$ref" : "#/definitions/Environment"
    },
    "ConcurrentBuildLimit" : {
      "type" : "integer"
    },
    "Visibility" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "BuildBatchConfig" : {
      "$ref" : "#/definitions/ProjectBuildBatchConfig"
    },
    "TimeoutInMinutes" : {
      "type" : "integer"
    },
    "Cache" : {
      "$ref" : "#/definitions/ProjectCache"
    }
  },
  "definitions" : {
    "ProjectSourceVersion" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SourceIdentifier" : {
          "type" : "string"
        },
        "SourceVersion" : {
          "type" : "string"
        }
      },
      "required" : [ "SourceIdentifier" ]
    },
    "VpcConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Subnets" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "VpcId" : {
          "type" : "string"
        },
        "SecurityGroupIds" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "SourceAuth" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Resource" : {
          "type" : "string"
        },
        "Type" : {
          "type" : "string"
        }
      },
      "required" : [ "Type" ]
    },
    "ScopeConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Scope" : {
          "type" : "string"
        },
        "Domain" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "Name" ]
    },
    "RegistryCredential" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Credential" : {
          "type" : "string"
        },
        "CredentialProvider" : {
          "type" : "string"
        }
      },
      "required" : [ "Credential", "CredentialProvider" ]
    },
    "FilterGroup" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "Source" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "ReportBuildStatus" : {
          "type" : "boolean"
        },
        "Auth" : {
          "$ref" : "#/definitions/SourceAuth"
        },
        "SourceIdentifier" : {
          "type" : "string"
        },
        "BuildSpec" : {
          "type" : "string"
        },
        "GitCloneDepth" : {
          "type" : "integer"
        },
        "BuildStatusConfig" : {
          "$ref" : "#/definitions/BuildStatusConfig"
        },
        "GitSubmodulesConfig" : {
          "$ref" : "#/definitions/GitSubmodulesConfig"
        },
        "InsecureSsl" : {
          "type" : "boolean"
        },
        "Location" : {
          "type" : "string"
        }
      },
      "required" : [ "Type" ]
    },
    "ProjectCache" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Modes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Type" : {
          "type" : "string"
        },
        "CacheNamespace" : {
          "type" : "string"
        },
        "Location" : {
          "type" : "string"
        }
      },
      "required" : [ "Type" ]
    },
    "Artifacts" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Path" : {
          "type" : "string"
        },
        "Type" : {
          "type" : "string"
        },
        "ArtifactIdentifier" : {
          "type" : "string"
        },
        "OverrideArtifactName" : {
          "type" : "boolean"
        },
        "Packaging" : {
          "type" : "string"
        },
        "EncryptionDisabled" : {
          "type" : "boolean"
        },
        "Location" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        },
        "NamespaceType" : {
          "type" : "string"
        }
      },
      "required" : [ "Type" ]
    },
    "LogsConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CloudWatchLogs" : {
          "$ref" : "#/definitions/CloudWatchLogsConfig"
        },
        "S3Logs" : {
          "$ref" : "#/definitions/S3LogsConfig"
        }
      }
    },
    "BatchRestrictions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ComputeTypesAllowed" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "MaximumBuildsAllowed" : {
          "type" : "integer"
        }
      }
    },
    "ProjectBuildBatchConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CombineArtifacts" : {
          "type" : "boolean"
        },
        "ServiceRole" : {
          "type" : "string"
        },
        "BatchReportMode" : {
          "type" : "string"
        },
        "TimeoutInMins" : {
          "type" : "integer"
        },
        "Restrictions" : {
          "$ref" : "#/definitions/BatchRestrictions"
        }
      }
    },
    "CloudWatchLogsConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Status" : {
          "type" : "string"
        },
        "GroupName" : {
          "type" : "string"
        },
        "StreamName" : {
          "type" : "string"
        }
      },
      "required" : [ "Status" ]
    },
    "Environment" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "EnvironmentVariables" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/EnvironmentVariable"
          }
        },
        "Fleet" : {
          "$ref" : "#/definitions/ProjectFleet"
        },
        "PrivilegedMode" : {
          "type" : "boolean"
        },
        "ImagePullCredentialsType" : {
          "type" : "string"
        },
        "Image" : {
          "type" : "string"
        },
        "RegistryCredential" : {
          "$ref" : "#/definitions/RegistryCredential"
        },
        "ComputeType" : {
          "type" : "string"
        },
        "Certificate" : {
          "type" : "string"
        }
      },
      "required" : [ "Type", "Image", "ComputeType" ]
    },
    "EnvironmentVariable" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Type" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Name" ]
    },
    "ProjectFileSystemLocation" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MountPoint" : {
          "type" : "string"
        },
        "Type" : {
          "type" : "string"
        },
        "Identifier" : {
          "type" : "string"
        },
        "MountOptions" : {
          "type" : "string"
        },
        "Location" : {
          "type" : "string"
        }
      },
      "required" : [ "MountPoint", "Type", "Identifier", "Location" ]
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
    "ProjectTriggers" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "BuildType" : {
          "type" : "string"
        },
        "FilterGroups" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/FilterGroup"
          }
        },
        "Webhook" : {
          "type" : "boolean"
        },
        "ScopeConfiguration" : {
          "$ref" : "#/definitions/ScopeConfiguration"
        }
      }
    },
    "BuildStatusConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Context" : {
          "type" : "string"
        },
        "TargetUrl" : {
          "type" : "string"
        }
      }
    },
    "GitSubmodulesConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "FetchSubmodules" : {
          "type" : "boolean"
        }
      },
      "required" : [ "FetchSubmodules" ]
    },
    "S3LogsConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Status" : {
          "type" : "string"
        },
        "EncryptionDisabled" : {
          "type" : "boolean"
        },
        "Location" : {
          "type" : "string"
        }
      },
      "required" : [ "Status" ]
    },
    "ProjectFleet" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "FleetArn" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "Artifacts", "ServiceRole", "Environment", "Source" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Arn" ]
}