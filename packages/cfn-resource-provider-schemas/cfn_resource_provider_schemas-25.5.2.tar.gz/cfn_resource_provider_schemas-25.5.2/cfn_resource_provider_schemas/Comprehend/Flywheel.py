SCHEMA = {
  "typeName" : "AWS::Comprehend::Flywheel",
  "description" : "The AWS::Comprehend::Flywheel resource creates an Amazon Comprehend Flywheel that enables customer to train their model.",
  "additionalProperties" : False,
  "properties" : {
    "ActiveModelArn" : {
      "type" : "string",
      "pattern" : "arn:aws(-[^:]+)?:comprehend:[a-zA-Z0-9-]*:[0-9]{12}:(document-classifier|entity-recognizer)/[a-zA-Z0-9](-*[a-zA-Z0-9])*(/version/[a-zA-Z0-9](-*[a-zA-Z0-9])*)?",
      "maxLength" : 256
    },
    "DataAccessRoleArn" : {
      "type" : "string",
      "pattern" : "arn:aws(-[^:]+)?:iam::[0-9]{12}:role/.+",
      "minLength" : 20,
      "maxLength" : 2048
    },
    "DataLakeS3Uri" : {
      "type" : "string",
      "pattern" : "s3://[a-z0-9][\\.\\-a-z0-9]{1,61}[a-z0-9](/.*)?",
      "maxLength" : 512
    },
    "DataSecurityConfig" : {
      "$ref" : "#/definitions/DataSecurityConfig"
    },
    "FlywheelName" : {
      "type" : "string",
      "pattern" : "^[a-zA-Z0-9](-*[a-zA-Z0-9])*$",
      "minLength" : 1,
      "maxLength" : 63
    },
    "ModelType" : {
      "type" : "string",
      "enum" : [ "DOCUMENT_CLASSIFIER", "ENTITY_RECOGNIZER" ]
    },
    "Tags" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "insertionOrder" : False,
      "uniqueItems" : True
    },
    "TaskConfig" : {
      "$ref" : "#/definitions/TaskConfig"
    },
    "Arn" : {
      "type" : "string",
      "pattern" : "arn:aws(-[^:]+)?:comprehend:[a-zA-Z0-9-]*:[0-9]{12}:flywheel/[a-zA-Z0-9](-*[a-zA-Z0-9])*",
      "minLength" : 1,
      "maxLength" : 256
    }
  },
  "required" : [ "FlywheelName", "DataAccessRoleArn", "DataLakeS3Uri" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "createOnlyProperties" : [ "/properties/FlywheelName", "/properties/ModelType", "/properties/DataLakeS3Uri", "/properties/TaskConfig" ],
  "readOnlyProperties" : [ "/properties/Arn" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "comprehend:TagResource", "comprehend:UntagResource" ]
  },
  "definitions" : {
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "type" : "string",
          "minLength" : 0,
          "maxLength" : 256
        }
      },
      "additionalProperties" : False,
      "required" : [ "Key", "Value" ]
    },
    "TaskConfig" : {
      "type" : "object",
      "properties" : {
        "LanguageCode" : {
          "type" : "string",
          "enum" : [ "en", "es", "fr", "it", "de", "pt" ]
        },
        "DocumentClassificationConfig" : {
          "$ref" : "#/definitions/DocumentClassificationConfig"
        },
        "EntityRecognitionConfig" : {
          "$ref" : "#/definitions/EntityRecognitionConfig"
        }
      },
      "required" : [ "LanguageCode" ],
      "additionalProperties" : False
    },
    "DataSecurityConfig" : {
      "type" : "object",
      "properties" : {
        "ModelKmsKeyId" : {
          "$ref" : "#/definitions/KmsKeyId"
        },
        "VolumeKmsKeyId" : {
          "$ref" : "#/definitions/KmsKeyId"
        },
        "DataLakeKmsKeyId" : {
          "$ref" : "#/definitions/KmsKeyId"
        },
        "VpcConfig" : {
          "$ref" : "#/definitions/VpcConfig"
        }
      },
      "required" : [ ],
      "additionalProperties" : False
    },
    "VpcConfig" : {
      "type" : "object",
      "properties" : {
        "SecurityGroupIds" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "pattern" : "[-0-9a-zA-Z]+",
            "minLength" : 1,
            "maxLength" : 32
          },
          "insertionOrder" : False,
          "uniqueItems" : True,
          "minItems" : 1,
          "maxItems" : 5
        },
        "Subnets" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "pattern" : "[-0-9a-zA-Z]+",
            "minLength" : 1,
            "maxLength" : 32
          },
          "insertionOrder" : False,
          "uniqueItems" : True,
          "minItems" : 1,
          "maxItems" : 16
        }
      },
      "required" : [ "SecurityGroupIds", "Subnets" ],
      "additionalProperties" : False
    },
    "KmsKeyId" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 2048
    },
    "EntityTypesListItem" : {
      "type" : "object",
      "properties" : {
        "Type" : {
          "type" : "string",
          "pattern" : "^(?![^\\n\\r\\t,]*\\\\n|\\\\r|\\\\t)[^\\n\\r\\t,]+$",
          "minLength" : 1,
          "maxLength" : 64
        }
      },
      "additionalProperties" : False,
      "required" : [ "Type" ]
    },
    "EntityRecognitionConfig" : {
      "type" : "object",
      "properties" : {
        "EntityTypes" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/EntityTypesListItem"
          },
          "insertionOrder" : False,
          "uniqueItems" : True,
          "minItems" : 1,
          "maxItems" : 25
        }
      },
      "additionalProperties" : False
    },
    "DocumentClassificationConfig" : {
      "type" : "object",
      "properties" : {
        "Mode" : {
          "type" : "string",
          "enum" : [ "MULTI_CLASS", "MULTI_LABEL" ]
        },
        "Labels" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "maxLength" : 5000
          },
          "insertionOrder" : False,
          "uniqueItems" : True,
          "maxItems" : 1000
        }
      },
      "additionalProperties" : False,
      "required" : [ "Mode" ]
    }
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "iam:PassRole", "comprehend:CreateFlywheel", "comprehend:DescribeFlywheel", "comprehend:ListTagsForResource" ],
      "timeoutInMinutes" : 240
    },
    "read" : {
      "permissions" : [ "comprehend:DescribeFlywheel", "comprehend:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "iam:PassRole", "comprehend:DescribeFlywheel", "comprehend:UpdateFlywheel", "comprehend:ListTagsForResource", "comprehend:TagResource", "comprehend:UntagResource" ],
      "timeoutInMinutes" : 10
    },
    "delete" : {
      "permissions" : [ "comprehend:DeleteFlywheel", "comprehend:DescribeFlywheel" ],
      "timeoutInMinutes" : 120
    },
    "list" : {
      "permissions" : [ "comprehend:ListFlywheels" ]
    }
  }
}