SCHEMA = {
  "typeName" : "AWS::CleanRoomsML::TrainingDataset",
  "description" : "Definition of AWS::CleanRoomsML::TrainingDataset Resource Type",
  "definitions" : {
    "ColumnSchema" : {
      "type" : "object",
      "properties" : {
        "ColumnName" : {
          "type" : "string",
          "maxLength" : 128,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9_](([a-zA-Z0-9_ ]+-)*([a-zA-Z0-9_ ]+))?$"
        },
        "ColumnTypes" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnType"
          },
          "maxItems" : 1,
          "minItems" : 1
        }
      },
      "required" : [ "ColumnName", "ColumnTypes" ],
      "additionalProperties" : False
    },
    "ColumnType" : {
      "type" : "string",
      "enum" : [ "USER_ID", "ITEM_ID", "TIMESTAMP", "CATEGORICAL_FEATURE", "NUMERICAL_FEATURE" ]
    },
    "DataSource" : {
      "type" : "object",
      "properties" : {
        "GlueDataSource" : {
          "$ref" : "#/definitions/GlueDataSource"
        }
      },
      "required" : [ "GlueDataSource" ],
      "additionalProperties" : False
    },
    "Dataset" : {
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/DatasetType"
        },
        "InputConfig" : {
          "$ref" : "#/definitions/DatasetInputConfig"
        }
      },
      "required" : [ "InputConfig", "Type" ],
      "additionalProperties" : False
    },
    "DatasetInputConfig" : {
      "type" : "object",
      "properties" : {
        "Schema" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ColumnSchema"
          },
          "maxItems" : 100,
          "minItems" : 1
        },
        "DataSource" : {
          "$ref" : "#/definitions/DataSource"
        }
      },
      "required" : [ "DataSource", "Schema" ],
      "additionalProperties" : False
    },
    "DatasetType" : {
      "type" : "string",
      "enum" : [ "INTERACTIONS" ]
    },
    "GlueDataSource" : {
      "type" : "object",
      "properties" : {
        "TableName" : {
          "type" : "string",
          "maxLength" : 128,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9_](([a-zA-Z0-9_ ]+-)*([a-zA-Z0-9_ ]+))?$"
        },
        "DatabaseName" : {
          "type" : "string",
          "maxLength" : 128,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9_](([a-zA-Z0-9_]+-)*([a-zA-Z0-9_]+))?$"
        },
        "CatalogId" : {
          "type" : "string",
          "maxLength" : 12,
          "minLength" : 12,
          "pattern" : "^[0-9]{12}$"
        }
      },
      "required" : [ "DatabaseName", "TableName" ],
      "additionalProperties" : False
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
    "TrainingDatasetStatus" : {
      "type" : "string",
      "enum" : [ "ACTIVE" ]
    },
    "Unit" : {
      "type" : "object",
      "additionalProperties" : False
    }
  },
  "properties" : {
    "Description" : {
      "type" : "string",
      "maxLength" : 255,
      "pattern" : "^[\\u0020-\\uD7FF\\uE000-\\uFFFD\\uD800\\uDBFF-\\uDC00\\uDFFF\\t\\r\\n]*$"
    },
    "Name" : {
      "type" : "string",
      "maxLength" : 63,
      "minLength" : 1,
      "pattern" : "^(?!\\s*$)[\\u0020-\\uD7FF\\uE000-\\uFFFD\\uD800\\uDBFF-\\uDC00\\uDFFF\\t]*$"
    },
    "RoleArn" : {
      "type" : "string",
      "maxLength" : 2048,
      "minLength" : 20,
      "pattern" : "^arn:aws[-a-z]*:iam::[0-9]{12}:role/.+$"
    },
    "Tags" : {
      "description" : "An arbitrary set of tags (key-value pairs) for this cleanrooms-ml training dataset.",
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "uniqueItems" : True,
      "type" : "array"
    },
    "TrainingData" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Dataset"
      },
      "maxItems" : 1,
      "minItems" : 1
    },
    "TrainingDatasetArn" : {
      "type" : "string",
      "maxLength" : 2048,
      "minLength" : 20,
      "pattern" : "^arn:aws[-a-z]*:cleanrooms-ml:[-a-z0-9]+:[0-9]{12}:training-dataset/[-a-zA-Z0-9_/.]+$"
    },
    "Status" : {
      "$ref" : "#/definitions/TrainingDatasetStatus"
    }
  },
  "required" : [ "Name", "RoleArn", "TrainingData" ],
  "readOnlyProperties" : [ "/properties/Status", "/properties/TrainingDatasetArn" ],
  "createOnlyProperties" : [ "/properties/Description", "/properties/Name", "/properties/RoleArn", "/properties/TrainingData" ],
  "primaryIdentifier" : [ "/properties/TrainingDatasetArn" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "cleanrooms-ml:TagResource", "cleanrooms-ml:UntagResource" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "cleanrooms-ml:CreateTrainingDataset", "cleanrooms-ml:GetTrainingDataset", "cleanrooms-ml:TagResource", "iam:PassRole" ]
    },
    "read" : {
      "permissions" : [ "cleanrooms-ml:GetTrainingDataset" ]
    },
    "delete" : {
      "permissions" : [ "cleanrooms-ml:DeleteTrainingDataset" ]
    },
    "list" : {
      "permissions" : [ "cleanrooms-ml:ListTrainingDatasets" ]
    },
    "update" : {
      "permissions" : [ "cleanrooms-ml:TagResource", "cleanrooms-ml:UntagResource" ]
    }
  },
  "additionalProperties" : False
}