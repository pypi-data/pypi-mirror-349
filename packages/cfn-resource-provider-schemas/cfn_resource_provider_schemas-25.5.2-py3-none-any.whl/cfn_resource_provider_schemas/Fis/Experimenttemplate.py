SCHEMA = {
  "typeName" : "AWS::FIS::ExperimentTemplate",
  "description" : "Resource schema for AWS::FIS::ExperimentTemplate",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-fis.git",
  "definitions" : {
    "ExperimentTemplateId" : {
      "type" : "string"
    },
    "ExperimentTemplateDescription" : {
      "type" : "string",
      "description" : "A description for the experiment template.",
      "maxLength" : 512
    },
    "StopConditionSource" : {
      "type" : "string",
      "maxLength" : 64
    },
    "StopConditionValue" : {
      "type" : "string",
      "minLength" : 20,
      "maxLength" : 2048
    },
    "ExperimentTemplateStopCondition" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Source" : {
          "$ref" : "#/definitions/StopConditionSource"
        },
        "Value" : {
          "$ref" : "#/definitions/StopConditionValue"
        }
      },
      "required" : [ "Source" ]
    },
    "CloudWatchDashboard" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DashboardIdentifier" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 512
        }
      },
      "required" : [ "DashboardIdentifier" ]
    },
    "ExperimentTemplateStopConditionList" : {
      "type" : "array",
      "description" : "One or more stop conditions.",
      "items" : {
        "$ref" : "#/definitions/ExperimentTemplateStopCondition"
      }
    },
    "ResourceType" : {
      "type" : "string",
      "description" : "The AWS resource type. The resource type must be supported for the specified action.",
      "maxLength" : 64
    },
    "ResourceArn" : {
      "type" : "string",
      "minLength" : 20,
      "maxLength" : 2048
    },
    "ResourceArnList" : {
      "type" : "array",
      "description" : "The Amazon Resource Names (ARNs) of the target resources.",
      "items" : {
        "$ref" : "#/definitions/ResourceArn"
      }
    },
    "ExperimentTemplateTargetSelectionMode" : {
      "type" : "string",
      "description" : "Scopes the identified resources to a specific number of the resources at random, or a percentage of the resources.",
      "maxLength" : 64
    },
    "ExperimentTemplateTargetFilterPath" : {
      "type" : "string",
      "description" : "The attribute path for the filter.",
      "maxLength" : 256
    },
    "ExperimentTemplateTargetFilterValue" : {
      "type" : "string",
      "maxLength" : 128
    },
    "ExperimentTemplateTargetFilterValues" : {
      "type" : "array",
      "description" : "The attribute values for the filter.",
      "items" : {
        "$ref" : "#/definitions/ExperimentTemplateTargetFilterValue"
      }
    },
    "ExperimentTemplateTargetFilter" : {
      "type" : "object",
      "description" : "Describes a filter used for the target resource input in an experiment template.",
      "additionalProperties" : False,
      "properties" : {
        "Path" : {
          "$ref" : "#/definitions/ExperimentTemplateTargetFilterPath"
        },
        "Values" : {
          "$ref" : "#/definitions/ExperimentTemplateTargetFilterValues"
        }
      },
      "required" : [ "Path", "Values" ]
    },
    "ExperimentTemplateTargetFilterList" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/ExperimentTemplateTargetFilter"
      }
    },
    "ExperimentTemplateTarget" : {
      "type" : "object",
      "description" : "Specifies a target for an experiment.",
      "additionalProperties" : False,
      "properties" : {
        "ResourceType" : {
          "$ref" : "#/definitions/ResourceType"
        },
        "ResourceArns" : {
          "$ref" : "#/definitions/ResourceArnList"
        },
        "ResourceTags" : {
          "type" : "object",
          "patternProperties" : {
            ".{1,128}" : {
              "type" : "string",
              "maxLength" : 256
            }
          },
          "additionalProperties" : False
        },
        "Parameters" : {
          "type" : "object",
          "patternProperties" : {
            ".{1,64}" : {
              "type" : "string",
              "maxLength" : 1024
            }
          },
          "additionalProperties" : False
        },
        "Filters" : {
          "$ref" : "#/definitions/ExperimentTemplateTargetFilterList"
        },
        "SelectionMode" : {
          "$ref" : "#/definitions/ExperimentTemplateTargetSelectionMode"
        }
      },
      "required" : [ "ResourceType", "SelectionMode" ]
    },
    "ExperimentTemplateTargetMap" : {
      "type" : "object",
      "description" : "The targets for the experiment.",
      "patternProperties" : {
        ".{1,64}" : {
          "$ref" : "#/definitions/ExperimentTemplateTarget"
        }
      },
      "additionalProperties" : False
    },
    "ActionId" : {
      "type" : "string",
      "description" : "The ID of the action.",
      "maxLength" : 64
    },
    "ExperimentTemplateActionItemDescription" : {
      "type" : "string",
      "description" : "A description for the action.",
      "maxLength" : 512
    },
    "ExperimentTemplateActionItemParameter" : {
      "type" : "string",
      "maxLength" : 1024
    },
    "ExperimentTemplateActionItemTarget" : {
      "type" : "string",
      "maxLength" : 64
    },
    "ExperimentTemplateActionItemStartAfter" : {
      "type" : "string",
      "maxLength" : 64
    },
    "ExperimentTemplateActionItemStartAfterList" : {
      "type" : "array",
      "description" : "The names of the actions that must be completed before the current action starts.",
      "items" : {
        "$ref" : "#/definitions/ExperimentTemplateActionItemStartAfter"
      }
    },
    "ExperimentTemplateAction" : {
      "type" : "object",
      "description" : "Specifies an action for the experiment template.",
      "additionalProperties" : False,
      "properties" : {
        "ActionId" : {
          "$ref" : "#/definitions/ActionId"
        },
        "Description" : {
          "$ref" : "#/definitions/ExperimentTemplateActionItemDescription"
        },
        "Parameters" : {
          "type" : "object",
          "description" : "The parameters for the action, if applicable.",
          "patternProperties" : {
            ".{1,64}" : {
              "$ref" : "#/definitions/ExperimentTemplateActionItemParameter"
            }
          },
          "additionalProperties" : False
        },
        "Targets" : {
          "type" : "object",
          "description" : "One or more targets for the action.",
          "patternProperties" : {
            ".{1,64}" : {
              "$ref" : "#/definitions/ExperimentTemplateActionItemTarget"
            }
          },
          "additionalProperties" : False
        },
        "StartAfter" : {
          "$ref" : "#/definitions/ExperimentTemplateActionItemStartAfterList"
        }
      },
      "required" : [ "ActionId" ]
    },
    "ExperimentTemplateActionMap" : {
      "type" : "object",
      "description" : "The actions for the experiment.",
      "patternProperties" : {
        "[\\S]{1,64}" : {
          "$ref" : "#/definitions/ExperimentTemplateAction"
        }
      },
      "additionalProperties" : False
    },
    "ExperimentTemplateLogConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CloudWatchLogsConfiguration" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "LogGroupArn" : {
              "type" : "string",
              "minLength" : 20,
              "maxLength" : 2048
            }
          },
          "required" : [ "LogGroupArn" ]
        },
        "S3Configuration" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "BucketName" : {
              "type" : "string",
              "minLength" : 3,
              "maxLength" : 63
            },
            "Prefix" : {
              "type" : "string",
              "minLength" : 1,
              "maxLength" : 700
            }
          },
          "required" : [ "BucketName" ]
        },
        "LogSchemaVersion" : {
          "type" : "integer",
          "minimum" : 1
        }
      },
      "required" : [ "LogSchemaVersion" ]
    },
    "ExperimentTemplateExperimentOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AccountTargeting" : {
          "type" : "string",
          "description" : "The account targeting setting for the experiment template.",
          "enum" : [ "multi-account", "single-account" ]
        },
        "EmptyTargetResolutionMode" : {
          "type" : "string",
          "description" : "The target resolution failure mode for the experiment template.",
          "enum" : [ "fail", "skip" ]
        }
      }
    },
    "ExperimentTemplateExperimentReportConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "required" : [ "Outputs" ],
      "properties" : {
        "Outputs" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "ExperimentReportS3Configuration" : {
              "type" : "object",
              "additionalProperties" : False,
              "properties" : {
                "BucketName" : {
                  "type" : "string",
                  "minLength" : 3,
                  "maxLength" : 63
                },
                "Prefix" : {
                  "type" : "string",
                  "minLength" : 1,
                  "maxLength" : 256
                }
              },
              "required" : [ "BucketName" ]
            }
          },
          "required" : [ "ExperimentReportS3Configuration" ]
        },
        "DataSources" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "CloudWatchDashboards" : {
              "type" : "array",
              "items" : {
                "$ref" : "#/definitions/CloudWatchDashboard"
              }
            }
          }
        },
        "PreExperimentDuration" : {
          "type" : "string"
        },
        "PostExperimentDuration" : {
          "type" : "string"
        }
      }
    },
    "RoleArn" : {
      "type" : "string",
      "description" : "The Amazon Resource Name (ARN) of an IAM role that grants the AWS FIS service permission to perform service actions on your behalf.",
      "maxLength" : 1224
    }
  },
  "properties" : {
    "Id" : {
      "$ref" : "#/definitions/ExperimentTemplateId"
    },
    "Description" : {
      "$ref" : "#/definitions/ExperimentTemplateDescription"
    },
    "Targets" : {
      "$ref" : "#/definitions/ExperimentTemplateTargetMap"
    },
    "Actions" : {
      "$ref" : "#/definitions/ExperimentTemplateActionMap"
    },
    "StopConditions" : {
      "$ref" : "#/definitions/ExperimentTemplateStopConditionList"
    },
    "LogConfiguration" : {
      "$ref" : "#/definitions/ExperimentTemplateLogConfiguration"
    },
    "RoleArn" : {
      "$ref" : "#/definitions/RoleArn"
    },
    "Tags" : {
      "type" : "object",
      "patternProperties" : {
        ".{1,128}" : {
          "type" : "string",
          "maxLength" : 256
        }
      },
      "additionalProperties" : False
    },
    "ExperimentOptions" : {
      "$ref" : "#/definitions/ExperimentTemplateExperimentOptions"
    },
    "ExperimentReportConfiguration" : {
      "$ref" : "#/definitions/ExperimentTemplateExperimentReportConfiguration"
    }
  },
  "additionalProperties" : False,
  "required" : [ "Description", "StopConditions", "Targets", "RoleArn", "Tags" ],
  "readOnlyProperties" : [ "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/Tags", "/properties/ExperimentOptions/AccountTargeting" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "fis:TagResource", "fis:UntagResource", "fis:ListTagsForResource" ]
  },
  "primaryIdentifier" : [ "/properties/Id" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "fis:CreateExperimentTemplate", "fis:TagResource", "iam:PassRole" ]
    },
    "read" : {
      "permissions" : [ "fis:GetExperimentTemplate", "fis:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "fis:UpdateExperimentTemplate", "fis:TagResource", "fis:UntagResource", "iam:PassRole" ]
    },
    "delete" : {
      "permissions" : [ "fis:DeleteExperimentTemplate" ]
    },
    "list" : {
      "permissions" : [ "fis:ListExperimentTemplates", "fis:ListTagsForResource" ]
    }
  }
}