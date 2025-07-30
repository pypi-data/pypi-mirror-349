SCHEMA = {
  "typeName" : "AWS::Greengrass::ResourceDefinitionVersion",
  "description" : "Resource Type definition for AWS::Greengrass::ResourceDefinitionVersion",
  "additionalProperties" : False,
  "properties" : {
    "ResourceDefinitionId" : {
      "type" : "string"
    },
    "Resources" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/ResourceInstance"
      }
    },
    "Id" : {
      "type" : "string"
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
  "required" : [ "Resources", "ResourceDefinitionId" ],
  "createOnlyProperties" : [ "/properties/Resources", "/properties/ResourceDefinitionId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}