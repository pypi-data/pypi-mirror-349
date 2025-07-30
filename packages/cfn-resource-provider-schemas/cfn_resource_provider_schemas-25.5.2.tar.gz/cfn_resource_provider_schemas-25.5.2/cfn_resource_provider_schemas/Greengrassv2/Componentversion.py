SCHEMA = {
  "typeName" : "AWS::GreengrassV2::ComponentVersion",
  "description" : "Resource for Greengrass component version.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-greengrassv2",
  "definitions" : {
    "LambdaFunctionRecipeSource" : {
      "type" : "object",
      "properties" : {
        "LambdaArn" : {
          "type" : "string",
          "pattern" : "^arn:[^:]*:lambda:(([a-z]+-)+[0-9])?:([0-9]{12})?:[^.]+$"
        },
        "ComponentName" : {
          "type" : "string"
        },
        "ComponentVersion" : {
          "type" : "string"
        },
        "ComponentPlatforms" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ComponentPlatform"
          },
          "insertionOrder" : False
        },
        "ComponentDependencies" : {
          "type" : "object",
          "patternProperties" : {
            ".*" : {
              "$ref" : "#/definitions/ComponentDependencyRequirement"
            }
          },
          "additionalProperties" : False
        },
        "ComponentLambdaParameters" : {
          "$ref" : "#/definitions/LambdaExecutionParameters"
        }
      },
      "additionalProperties" : False
    },
    "ComponentPlatform" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "Attributes" : {
          "type" : "object",
          "patternProperties" : {
            ".+" : {
              "type" : "string"
            }
          },
          "additionalProperties" : False
        }
      },
      "additionalProperties" : False
    },
    "ComponentDependencyRequirement" : {
      "type" : "object",
      "properties" : {
        "VersionRequirement" : {
          "type" : "string"
        },
        "DependencyType" : {
          "type" : "string",
          "enum" : [ "SOFT", "HARD" ]
        }
      },
      "additionalProperties" : False
    },
    "LambdaExecutionParameters" : {
      "type" : "object",
      "properties" : {
        "EventSources" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/LambdaEventSource"
          },
          "insertionOrder" : False
        },
        "MaxQueueSize" : {
          "type" : "integer"
        },
        "MaxInstancesCount" : {
          "type" : "integer"
        },
        "MaxIdleTimeInSeconds" : {
          "type" : "integer"
        },
        "TimeoutInSeconds" : {
          "type" : "integer"
        },
        "StatusTimeoutInSeconds" : {
          "type" : "integer"
        },
        "Pinned" : {
          "type" : "boolean"
        },
        "InputPayloadEncodingType" : {
          "type" : "string",
          "enum" : [ "json", "binary" ]
        },
        "ExecArgs" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          },
          "insertionOrder" : True
        },
        "EnvironmentVariables" : {
          "type" : "object",
          "patternProperties" : {
            ".+" : {
              "type" : "string"
            }
          },
          "additionalProperties" : False
        },
        "LinuxProcessParams" : {
          "$ref" : "#/definitions/LambdaLinuxProcessParams"
        }
      },
      "additionalProperties" : False
    },
    "LambdaEventSource" : {
      "type" : "object",
      "properties" : {
        "Topic" : {
          "type" : "string"
        },
        "Type" : {
          "type" : "string",
          "enum" : [ "PUB_SUB", "IOT_CORE" ]
        }
      },
      "additionalProperties" : False
    },
    "LambdaLinuxProcessParams" : {
      "type" : "object",
      "properties" : {
        "IsolationMode" : {
          "type" : "string",
          "enum" : [ "GreengrassContainer", "NoContainer" ]
        },
        "ContainerParams" : {
          "$ref" : "#/definitions/LambdaContainerParams"
        }
      },
      "additionalProperties" : False
    },
    "LambdaContainerParams" : {
      "type" : "object",
      "properties" : {
        "MemorySizeInKB" : {
          "type" : "integer"
        },
        "MountROSysfs" : {
          "type" : "boolean"
        },
        "Volumes" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/LambdaVolumeMount"
          },
          "insertionOrder" : False
        },
        "Devices" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/LambdaDeviceMount"
          },
          "insertionOrder" : False
        }
      },
      "additionalProperties" : False
    },
    "LambdaVolumeMount" : {
      "type" : "object",
      "properties" : {
        "SourcePath" : {
          "$ref" : "#/definitions/FilesystemPath"
        },
        "DestinationPath" : {
          "$ref" : "#/definitions/FilesystemPath"
        },
        "Permission" : {
          "$ref" : "#/definitions/LambdaFilesystemPermission"
        },
        "AddGroupOwner" : {
          "$ref" : "#/definitions/LambdaAddGroupOwnerBoolean"
        }
      },
      "additionalProperties" : False
    },
    "LambdaDeviceMount" : {
      "type" : "object",
      "properties" : {
        "Path" : {
          "$ref" : "#/definitions/FilesystemPath"
        },
        "Permission" : {
          "$ref" : "#/definitions/LambdaFilesystemPermission"
        },
        "AddGroupOwner" : {
          "$ref" : "#/definitions/LambdaAddGroupOwnerBoolean"
        }
      },
      "additionalProperties" : False
    },
    "FilesystemPath" : {
      "type" : "string"
    },
    "LambdaFilesystemPermission" : {
      "type" : "string",
      "enum" : [ "ro", "rw" ]
    },
    "LambdaAddGroupOwnerBoolean" : {
      "type" : "boolean"
    }
  },
  "properties" : {
    "Arn" : {
      "type" : "string"
    },
    "ComponentName" : {
      "type" : "string"
    },
    "ComponentVersion" : {
      "type" : "string"
    },
    "InlineRecipe" : {
      "type" : "string"
    },
    "LambdaFunction" : {
      "$ref" : "#/definitions/LambdaFunctionRecipeSource"
    },
    "Tags" : {
      "type" : "object",
      "patternProperties" : {
        "^(?!aws:)[a-zA-Z+-=._:/]{1,128}$" : {
          "type" : "string",
          "maxLength" : 256
        }
      },
      "maxProperties" : 50,
      "additionalProperties" : False
    }
  },
  "additionalProperties" : False,
  "createOnlyProperties" : [ "/properties/LambdaFunction", "/properties/InlineRecipe" ],
  "readOnlyProperties" : [ "/properties/Arn", "/properties/ComponentName", "/properties/ComponentVersion" ],
  "writeOnlyProperties" : [ "/properties/LambdaFunction", "/properties/InlineRecipe" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "additionalIdentifiers" : [ [ "/properties/ComponentName", "/properties/ComponentVersion" ] ],
  "handlers" : {
    "create" : {
      "permissions" : [ "greengrass:CreateComponentVersion", "greengrass:DescribeComponent", "greengrass:ListTagsForResource", "greengrass:TagResource", "lambda:GetFunction", "s3:GetObject" ]
    },
    "read" : {
      "permissions" : [ "greengrass:DescribeComponent", "greengrass:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "greengrass:DescribeComponent", "greengrass:ListTagsForResource", "greengrass:TagResource", "greengrass:UntagResource" ]
    },
    "delete" : {
      "permissions" : [ "greengrass:DeleteComponent" ]
    },
    "list" : {
      "handlerSchema" : {
        "properties" : {
          "Arn" : {
            "type" : "string"
          }
        },
        "required" : [ "Arn" ]
      },
      "permissions" : [ "greengrass:ListComponentVersions" ]
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags"
  }
}