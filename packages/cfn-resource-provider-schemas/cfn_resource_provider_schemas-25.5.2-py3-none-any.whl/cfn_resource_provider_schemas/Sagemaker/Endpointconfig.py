SCHEMA = {
  "typeName" : "AWS::SageMaker::EndpointConfig",
  "description" : "Resource Type definition for AWS::SageMaker::EndpointConfig",
  "additionalProperties" : False,
  "properties" : {
    "ShadowProductionVariants" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/ProductionVariant"
      }
    },
    "DataCaptureConfig" : {
      "$ref" : "#/definitions/DataCaptureConfig"
    },
    "ExecutionRoleArn" : {
      "type" : "string"
    },
    "EnableNetworkIsolation" : {
      "type" : "boolean"
    },
    "ProductionVariants" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/ProductionVariant"
      }
    },
    "KmsKeyId" : {
      "type" : "string"
    },
    "AsyncInferenceConfig" : {
      "$ref" : "#/definitions/AsyncInferenceConfig"
    },
    "VpcConfig" : {
      "$ref" : "#/definitions/VpcConfig"
    },
    "EndpointConfigName" : {
      "type" : "string"
    },
    "ExplainerConfig" : {
      "$ref" : "#/definitions/ExplainerConfig"
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
    "ManagedInstanceScaling" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Status" : {
          "type" : "string"
        },
        "MaxInstanceCount" : {
          "type" : "integer"
        },
        "MinInstanceCount" : {
          "type" : "integer"
        }
      }
    },
    "AsyncInferenceNotificationConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IncludeInferenceResponseIn" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "SuccessTopic" : {
          "type" : "string"
        },
        "ErrorTopic" : {
          "type" : "string"
        }
      }
    },
    "ClarifyHeader" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "ProductionVariant" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ManagedInstanceScaling" : {
          "$ref" : "#/definitions/ManagedInstanceScaling"
        },
        "ModelName" : {
          "type" : "string"
        },
        "VolumeSizeInGB" : {
          "type" : "integer"
        },
        "EnableSSMAccess" : {
          "type" : "boolean"
        },
        "VariantName" : {
          "type" : "string"
        },
        "InitialInstanceCount" : {
          "type" : "integer"
        },
        "RoutingConfig" : {
          "$ref" : "#/definitions/RoutingConfig"
        },
        "InitialVariantWeight" : {
          "type" : "number"
        },
        "ModelDataDownloadTimeoutInSeconds" : {
          "type" : "integer"
        },
        "InferenceAmiVersion" : {
          "type" : "string"
        },
        "ContainerStartupHealthCheckTimeoutInSeconds" : {
          "type" : "integer"
        },
        "ServerlessConfig" : {
          "$ref" : "#/definitions/ServerlessConfig"
        },
        "InstanceType" : {
          "type" : "string"
        }
      },
      "required" : [ "VariantName" ]
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
    "ClarifyInferenceConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ContentTemplate" : {
          "type" : "string"
        },
        "LabelHeaders" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/ClarifyHeader"
          }
        },
        "MaxPayloadInMB" : {
          "type" : "integer"
        },
        "ProbabilityIndex" : {
          "type" : "integer"
        },
        "LabelAttribute" : {
          "type" : "string"
        },
        "FeatureTypes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/ClarifyFeatureType"
          }
        },
        "FeatureHeaders" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/ClarifyHeader"
          }
        },
        "LabelIndex" : {
          "type" : "integer"
        },
        "ProbabilityAttribute" : {
          "type" : "string"
        },
        "FeaturesAttribute" : {
          "type" : "string"
        },
        "MaxRecordCount" : {
          "type" : "integer"
        }
      }
    },
    "ExplainerConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ClarifyExplainerConfig" : {
          "$ref" : "#/definitions/ClarifyExplainerConfig"
        }
      }
    },
    "ClarifyFeatureType" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "CaptureContentTypeHeader" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CsvContentTypes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "JsonContentTypes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "RoutingConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RoutingStrategy" : {
          "type" : "string"
        }
      }
    },
    "ClarifyTextConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Language" : {
          "type" : "string"
        },
        "Granularity" : {
          "type" : "string"
        }
      },
      "required" : [ "Language", "Granularity" ]
    },
    "DataCaptureConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CaptureOptions" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/CaptureOption"
          }
        },
        "KmsKeyId" : {
          "type" : "string"
        },
        "DestinationS3Uri" : {
          "type" : "string"
        },
        "InitialSamplingPercentage" : {
          "type" : "integer"
        },
        "CaptureContentTypeHeader" : {
          "$ref" : "#/definitions/CaptureContentTypeHeader"
        },
        "EnableCapture" : {
          "type" : "boolean"
        }
      },
      "required" : [ "CaptureOptions", "DestinationS3Uri", "InitialSamplingPercentage" ]
    },
    "AsyncInferenceConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ClientConfig" : {
          "$ref" : "#/definitions/AsyncInferenceClientConfig"
        },
        "OutputConfig" : {
          "$ref" : "#/definitions/AsyncInferenceOutputConfig"
        }
      },
      "required" : [ "OutputConfig" ]
    },
    "AsyncInferenceClientConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxConcurrentInvocationsPerInstance" : {
          "type" : "integer"
        }
      }
    },
    "ClarifyShapBaselineConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MimeType" : {
          "type" : "string"
        },
        "ShapBaseline" : {
          "type" : "string"
        },
        "ShapBaselineUri" : {
          "type" : "string"
        }
      }
    },
    "ServerlessConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxConcurrency" : {
          "type" : "integer"
        },
        "MemorySizeInMB" : {
          "type" : "integer"
        },
        "ProvisionedConcurrency" : {
          "type" : "integer"
        }
      },
      "required" : [ "MaxConcurrency", "MemorySizeInMB" ]
    },
    "ClarifyShapConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TextConfig" : {
          "$ref" : "#/definitions/ClarifyTextConfig"
        },
        "UseLogit" : {
          "type" : "boolean"
        },
        "Seed" : {
          "type" : "integer"
        },
        "ShapBaselineConfig" : {
          "$ref" : "#/definitions/ClarifyShapBaselineConfig"
        },
        "NumberOfSamples" : {
          "type" : "integer"
        }
      },
      "required" : [ "ShapBaselineConfig" ]
    },
    "ClarifyExplainerConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "EnableExplanations" : {
          "type" : "string"
        },
        "ShapConfig" : {
          "$ref" : "#/definitions/ClarifyShapConfig"
        },
        "InferenceConfig" : {
          "$ref" : "#/definitions/ClarifyInferenceConfig"
        }
      },
      "required" : [ "ShapConfig" ]
    },
    "CaptureOption" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CaptureMode" : {
          "type" : "string"
        }
      },
      "required" : [ "CaptureMode" ]
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
    "AsyncInferenceOutputConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "NotificationConfig" : {
          "$ref" : "#/definitions/AsyncInferenceNotificationConfig"
        },
        "KmsKeyId" : {
          "type" : "string"
        },
        "S3OutputPath" : {
          "type" : "string"
        },
        "S3FailurePath" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "ProductionVariants" ],
  "createOnlyProperties" : [ "/properties/KmsKeyId", "/properties/AsyncInferenceConfig", "/properties/ExecutionRoleArn", "/properties/ShadowProductionVariants", "/properties/EnableNetworkIsolation", "/properties/ProductionVariants", "/properties/DataCaptureConfig", "/properties/ExplainerConfig", "/properties/EndpointConfigName", "/properties/VpcConfig" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}