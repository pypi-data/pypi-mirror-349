SCHEMA = {
  "typeName" : "AWS::Greengrass::ResourceDefinition",
  "description" : "Resource Type definition for AWS::Greengrass::ResourceDefinition",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "LatestVersionArn" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "object"
    },
    "Name" : {
      "type" : "string"
    },
    "InitialVersion" : {
      "$ref" : "#/definitions/ResourceDefinitionVersion"
    }
  },
  "definitions" : {
    "SecretsManagerSecretResourceData" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ARN" : {
          "type" : "string"
        },
        "AdditionalStagingLabelsToDownload" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "ARN" ]
    },
    "ResourceDataContainer" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "LocalVolumeResourceData" : {
          "$ref" : "#/definitions/LocalVolumeResourceData"
        },
        "LocalDeviceResourceData" : {
          "$ref" : "#/definitions/LocalDeviceResourceData"
        },
        "S3MachineLearningModelResourceData" : {
          "$ref" : "#/definitions/S3MachineLearningModelResourceData"
        },
        "SecretsManagerSecretResourceData" : {
          "$ref" : "#/definitions/SecretsManagerSecretResourceData"
        },
        "SageMakerMachineLearningModelResourceData" : {
          "$ref" : "#/definitions/SageMakerMachineLearningModelResourceData"
        }
      }
    },
    "SageMakerMachineLearningModelResourceData" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OwnerSetting" : {
          "$ref" : "#/definitions/ResourceDownloadOwnerSetting"
        },
        "SageMakerJobArn" : {
          "type" : "string"
        },
        "DestinationPath" : {
          "type" : "string"
        }
      },
      "required" : [ "DestinationPath", "SageMakerJobArn" ]
    },
    "ResourceInstance" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ResourceDataContainer" : {
          "$ref" : "#/definitions/ResourceDataContainer"
        },
        "Id" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "ResourceDataContainer", "Id", "Name" ]
    },
    "LocalVolumeResourceData" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SourcePath" : {
          "type" : "string"
        },
        "DestinationPath" : {
          "type" : "string"
        },
        "GroupOwnerSetting" : {
          "$ref" : "#/definitions/GroupOwnerSetting"
        }
      },
      "required" : [ "SourcePath", "DestinationPath" ]
    },
    "LocalDeviceResourceData" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SourcePath" : {
          "type" : "string"
        },
        "GroupOwnerSetting" : {
          "$ref" : "#/definitions/GroupOwnerSetting"
        }
      },
      "required" : [ "SourcePath" ]
    },
    "S3MachineLearningModelResourceData" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OwnerSetting" : {
          "$ref" : "#/definitions/ResourceDownloadOwnerSetting"
        },
        "DestinationPath" : {
          "type" : "string"
        },
        "S3Uri" : {
          "type" : "string"
        }
      },
      "required" : [ "DestinationPath", "S3Uri" ]
    },
    "ResourceDownloadOwnerSetting" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "GroupPermission" : {
          "type" : "string"
        },
        "GroupOwner" : {
          "type" : "string"
        }
      },
      "required" : [ "GroupOwner", "GroupPermission" ]
    },
    "ResourceDefinitionVersion" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Resources" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/ResourceInstance"
          }
        }
      },
      "required" : [ "Resources" ]
    },
    "GroupOwnerSetting" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AutoAddGroupOwner" : {
          "type" : "boolean"
        },
        "GroupOwner" : {
          "type" : "string"
        }
      },
      "required" : [ "AutoAddGroupOwner" ]
    }
  },
  "required" : [ "Name" ],
  "createOnlyProperties" : [ "/properties/InitialVersion" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/LatestVersionArn", "/properties/Id", "/properties/Arn" ]
}