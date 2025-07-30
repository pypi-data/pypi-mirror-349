SCHEMA = {
  "typeName" : "AWS::Glue::MLTransform",
  "description" : "Resource Type definition for AWS::Glue::MLTransform",
  "additionalProperties" : False,
  "properties" : {
    "MaxRetries" : {
      "type" : "integer"
    },
    "Description" : {
      "type" : "string"
    },
    "TransformEncryption" : {
      "$ref" : "#/definitions/TransformEncryption"
    },
    "Timeout" : {
      "type" : "integer"
    },
    "Name" : {
      "type" : "string"
    },
    "Role" : {
      "type" : "string"
    },
    "WorkerType" : {
      "type" : "string"
    },
    "GlueVersion" : {
      "type" : "string"
    },
    "TransformParameters" : {
      "$ref" : "#/definitions/TransformParameters"
    },
    "Id" : {
      "type" : "string"
    },
    "InputRecordTables" : {
      "$ref" : "#/definitions/InputRecordTables"
    },
    "NumberOfWorkers" : {
      "type" : "integer"
    },
    "Tags" : {
      "type" : "object"
    },
    "MaxCapacity" : {
      "type" : "number"
    }
  },
  "definitions" : {
    "GlueTables" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ConnectionName" : {
          "type" : "string"
        },
        "DatabaseName" : {
          "type" : "string"
        },
        "TableName" : {
          "type" : "string"
        },
        "CatalogId" : {
          "type" : "string"
        }
      },
      "required" : [ "TableName", "DatabaseName" ]
    },
    "TransformEncryption" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TaskRunSecurityConfigurationName" : {
          "type" : "string"
        },
        "MLUserDataEncryption" : {
          "$ref" : "#/definitions/MLUserDataEncryption"
        }
      }
    },
    "MLUserDataEncryption" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "KmsKeyId" : {
          "type" : "string"
        },
        "MLUserDataEncryptionMode" : {
          "type" : "string"
        }
      },
      "required" : [ "MLUserDataEncryptionMode" ]
    },
    "TransformParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TransformType" : {
          "type" : "string"
        },
        "FindMatchesParameters" : {
          "$ref" : "#/definitions/FindMatchesParameters"
        }
      },
      "required" : [ "TransformType" ]
    },
    "InputRecordTables" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "GlueTables" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/GlueTables"
          }
        }
      }
    },
    "FindMatchesParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PrecisionRecallTradeoff" : {
          "type" : "number"
        },
        "EnforceProvidedLabels" : {
          "type" : "boolean"
        },
        "PrimaryKeyColumnName" : {
          "type" : "string"
        },
        "AccuracyCostTradeoff" : {
          "type" : "number"
        }
      },
      "required" : [ "PrimaryKeyColumnName" ]
    }
  },
  "required" : [ "Role", "TransformParameters", "InputRecordTables" ],
  "createOnlyProperties" : [ "/properties/InputRecordTables" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}