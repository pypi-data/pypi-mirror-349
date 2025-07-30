SCHEMA = {
  "typeName" : "AWS::SageMaker::Model",
  "description" : "Resource Type definition for AWS::SageMaker::Model",
  "additionalProperties" : False,
  "properties" : {
    "ExecutionRoleArn" : {
      "type" : "string"
    },
    "EnableNetworkIsolation" : {
      "type" : "boolean"
    },
    "PrimaryContainer" : {
      "$ref" : "#/definitions/ContainerDefinition"
    },
    "ModelName" : {
      "type" : "string"
    },
    "VpcConfig" : {
      "$ref" : "#/definitions/VpcConfig"
    },
    "Containers" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/ContainerDefinition"
      }
    },
    "InferenceExecutionConfig" : {
      "$ref" : "#/definitions/InferenceExecutionConfig"
    },
    "Id" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "definitions" : {
    "ImageConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RepositoryAuthConfig" : {
          "$ref" : "#/definitions/RepositoryAuthConfig"
        },
        "RepositoryAccessMode" : {
          "type" : "string"
        }
      },
      "required" : [ "RepositoryAccessMode" ]
    },
    "ModelAccessConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AcceptEula" : {
          "type" : "boolean"
        }
      },
      "required" : [ "AcceptEula" ]
    },
    "VpcConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecurityGroupIds" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Subnets" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "Subnets", "SecurityGroupIds" ]
    },
    "RepositoryAuthConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RepositoryCredentialsProviderArn" : {
          "type" : "string"
        }
      },
      "required" : [ "RepositoryCredentialsProviderArn" ]
    },
    "S3DataSource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ModelAccessConfig" : {
          "$ref" : "#/definitions/ModelAccessConfig"
        },
        "S3DataType" : {
          "type" : "string"
        },
        "CompressionType" : {
          "type" : "string"
        },
        "HubAccessConfig" : {
          "$ref" : "#/definitions/HubAccessConfig"
        },
        "S3Uri" : {
          "type" : "string"
        }
      },
      "required" : [ "S3Uri", "S3DataType", "CompressionType" ]
    },
    "ContainerDefinition" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ImageConfig" : {
          "$ref" : "#/definitions/ImageConfig"
        },
        "InferenceSpecificationName" : {
          "type" : "string"
        },
        "ContainerHostname" : {
          "type" : "string"
        },
        "ModelPackageName" : {
          "type" : "string"
        },
        "Mode" : {
          "type" : "string"
        },
        "Environment" : {
          "type" : "object"
        },
        "ModelDataUrl" : {
          "type" : "string"
        },
        "Image" : {
          "type" : "string"
        },
        "ModelDataSource" : {
          "$ref" : "#/definitions/ModelDataSource"
        },
        "MultiModelConfig" : {
          "$ref" : "#/definitions/MultiModelConfig"
        }
      }
    },
    "InferenceExecutionConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Mode" : {
          "type" : "string"
        }
      },
      "required" : [ "Mode" ]
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
    "ModelDataSource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "S3DataSource" : {
          "$ref" : "#/definitions/S3DataSource"
        }
      },
      "required" : [ "S3DataSource" ]
    },
    "HubAccessConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "HubContentArn" : {
          "type" : "string"
        }
      },
      "required" : [ "HubContentArn" ]
    },
    "MultiModelConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ModelCacheSetting" : {
          "type" : "string"
        }
      }
    }
  },
  "createOnlyProperties" : [ "/properties/ExecutionRoleArn", "/properties/EnableNetworkIsolation", "/properties/InferenceExecutionConfig", "/properties/PrimaryContainer", "/properties/ModelName", "/properties/VpcConfig", "/properties/Containers" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}