SCHEMA = {
  "typeName" : "AWS::IoTAnalytics::Dataset",
  "description" : "Resource Type definition for AWS::IoTAnalytics::Dataset",
  "additionalProperties" : False,
  "taggable" : True,
  "properties" : {
    "Actions" : {
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "minItems" : 1,
      "maxItems" : 1,
      "items" : {
        "$ref" : "#/definitions/Action"
      }
    },
    "LateDataRules" : {
      "type" : "array",
      "minItems" : 1,
      "maxItems" : 1,
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/LateDataRule"
      }
    },
    "DatasetName" : {
      "type" : "string",
      "pattern" : "(^(?!_{2}))(^[a-zA-Z0-9_]+$)",
      "minLength" : 1,
      "maxLength" : 128
    },
    "ContentDeliveryRules" : {
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "minItems" : 0,
      "maxItems" : 20,
      "items" : {
        "$ref" : "#/definitions/DatasetContentDeliveryRule"
      }
    },
    "Triggers" : {
      "type" : "array",
      "minItems" : 0,
      "maxItems" : 5,
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Trigger"
      }
    },
    "VersioningConfiguration" : {
      "$ref" : "#/definitions/VersioningConfiguration"
    },
    "Id" : {
      "type" : "string"
    },
    "RetentionPeriod" : {
      "$ref" : "#/definitions/RetentionPeriod"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "minItems" : 1,
      "maxItems" : 50,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "definitions" : {
    "DatasetContentVersionValue" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DatasetName" : {
          "type" : "string",
          "pattern" : "(^(?!_{2}))(^[a-zA-Z0-9_]+$)",
          "minLength" : 1,
          "maxLength" : 128
        }
      },
      "required" : [ "DatasetName" ]
    },
    "GlueConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DatabaseName" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 150
        },
        "TableName" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 150
        }
      },
      "required" : [ "TableName", "DatabaseName" ]
    },
    "Action" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ActionName" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z0-9_]+$",
          "minLength" : 1,
          "maxLength" : 128
        },
        "ContainerAction" : {
          "$ref" : "#/definitions/ContainerAction"
        },
        "QueryAction" : {
          "$ref" : "#/definitions/QueryAction"
        }
      },
      "required" : [ "ActionName" ]
    },
    "Variable" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VariableName" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 256
        },
        "DatasetContentVersionValue" : {
          "$ref" : "#/definitions/DatasetContentVersionValue"
        },
        "StringValue" : {
          "type" : "string",
          "minLength" : 0,
          "maxLength" : 1024
        },
        "DoubleValue" : {
          "type" : "number"
        },
        "OutputFileUriValue" : {
          "$ref" : "#/definitions/OutputFileUriValue"
        }
      },
      "required" : [ "VariableName" ]
    },
    "IotEventsDestinationConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "InputName" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z][a-zA-Z0-9_]*$",
          "minLength" : 1,
          "maxLength" : 128
        },
        "RoleArn" : {
          "type" : "string",
          "minLength" : 20,
          "maxLength" : 2048
        }
      },
      "required" : [ "InputName", "RoleArn" ]
    },
    "LateDataRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RuleConfiguration" : {
          "$ref" : "#/definitions/LateDataRuleConfiguration"
        },
        "RuleName" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z0-9_]+$",
          "minLength" : 1,
          "maxLength" : 128
        }
      },
      "required" : [ "RuleConfiguration" ]
    },
    "DeltaTimeSessionWindowConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TimeoutInMinutes" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 60
        }
      },
      "required" : [ "TimeoutInMinutes" ]
    },
    "QueryAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Filters" : {
          "type" : "array",
          "minItems" : 0,
          "maxItems" : 1,
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Filter"
          }
        },
        "SqlQuery" : {
          "type" : "string"
        }
      },
      "required" : [ "SqlQuery" ]
    },
    "VersioningConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Unlimited" : {
          "type" : "boolean"
        },
        "MaxVersions" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 1000
        }
      }
    },
    "RetentionPeriod" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "NumberOfDays" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 2147483647
        },
        "Unlimited" : {
          "type" : "boolean"
        }
      }
    },
    "ResourceConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VolumeSizeInGB" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 50
        },
        "ComputeType" : {
          "type" : "string",
          "enum" : [ "ACU_1", "ACU_2" ]
        }
      },
      "required" : [ "VolumeSizeInGB", "ComputeType" ]
    },
    "DatasetContentDeliveryRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Destination" : {
          "$ref" : "#/definitions/DatasetContentDeliveryRuleDestination"
        },
        "EntryName" : {
          "type" : "string"
        }
      },
      "required" : [ "Destination" ]
    },
    "Trigger" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TriggeringDataset" : {
          "$ref" : "#/definitions/TriggeringDataset"
        },
        "Schedule" : {
          "$ref" : "#/definitions/Schedule"
        }
      }
    },
    "DeltaTime" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OffsetSeconds" : {
          "type" : "integer"
        },
        "TimeExpression" : {
          "type" : "string"
        }
      },
      "required" : [ "TimeExpression", "OffsetSeconds" ]
    },
    "ContainerAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Variables" : {
          "type" : "array",
          "minItems" : 0,
          "maxItems" : 50,
          "uniqueItems" : False,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Variable"
          }
        },
        "ExecutionRoleArn" : {
          "type" : "string",
          "minLength" : 20,
          "maxLength" : 2048
        },
        "Image" : {
          "type" : "string",
          "maxLength" : 255
        },
        "ResourceConfiguration" : {
          "$ref" : "#/definitions/ResourceConfiguration"
        }
      },
      "required" : [ "ExecutionRoleArn", "Image", "ResourceConfiguration" ]
    },
    "Filter" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DeltaTime" : {
          "$ref" : "#/definitions/DeltaTime"
        }
      }
    },
    "OutputFileUriValue" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "FileName" : {
          "type" : "string",
          "pattern" : "^[\\w\\.-]{1,255}$"
        }
      },
      "required" : [ "FileName" ]
    },
    "Schedule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ScheduleExpression" : {
          "type" : "string"
        }
      },
      "required" : [ "ScheduleExpression" ]
    },
    "S3DestinationConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "GlueConfiguration" : {
          "$ref" : "#/definitions/GlueConfiguration"
        },
        "Bucket" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z0-9.\\-_]*$",
          "minLength" : 3,
          "maxLength" : 255
        },
        "Key" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z0-9!_.*'()/{}:-]*$",
          "minLength" : 1,
          "maxLength" : 255
        },
        "RoleArn" : {
          "type" : "string",
          "minLength" : 20,
          "maxLength" : 2048
        }
      },
      "required" : [ "Bucket", "Key", "RoleArn" ]
    },
    "LateDataRuleConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DeltaTimeSessionWindowConfiguration" : {
          "$ref" : "#/definitions/DeltaTimeSessionWindowConfiguration"
        }
      }
    },
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 256
        }
      },
      "required" : [ "Value", "Key" ]
    },
    "DatasetContentDeliveryRuleDestination" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IotEventsDestinationConfiguration" : {
          "$ref" : "#/definitions/IotEventsDestinationConfiguration"
        },
        "S3DestinationConfiguration" : {
          "$ref" : "#/definitions/S3DestinationConfiguration"
        }
      }
    },
    "TriggeringDataset" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DatasetName" : {
          "type" : "string",
          "pattern" : "(^(?!_{2}))(^[a-zA-Z0-9_]+$)",
          "minLength" : 1,
          "maxLength" : 128
        }
      },
      "required" : [ "DatasetName" ]
    }
  },
  "required" : [ "Actions" ],
  "primaryIdentifier" : [ "/properties/DatasetName" ],
  "createOnlyProperties" : [ "/properties/DatasetName" ],
  "readOnlyProperties" : [ "/properties/Id" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iotanalytics:CreateDataset" ]
    },
    "read" : {
      "permissions" : [ "iotanalytics:DescribeDataset", "iotanalytics:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "iotanalytics:UpdateDataset", "iotanalytics:TagResource", "iotanalytics:UntagResource" ]
    },
    "delete" : {
      "permissions" : [ "iotanalytics:DeleteDataset" ]
    },
    "list" : {
      "permissions" : [ "iotanalytics:ListDatasets" ]
    }
  }
}