SCHEMA = {
  "typeName" : "AWS::KinesisAnalytics::Application",
  "description" : "Resource Type definition for AWS::KinesisAnalytics::Application",
  "additionalProperties" : False,
  "properties" : {
    "ApplicationName" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "Inputs" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Input"
      }
    },
    "ApplicationDescription" : {
      "type" : "string"
    },
    "ApplicationCode" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "Input" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "NamePrefix" : {
          "type" : "string"
        },
        "InputSchema" : {
          "$ref" : "#/definitions/InputSchema"
        },
        "KinesisStreamsInput" : {
          "$ref" : "#/definitions/KinesisStreamsInput"
        },
        "KinesisFirehoseInput" : {
          "$ref" : "#/definitions/KinesisFirehoseInput"
        },
        "InputProcessingConfiguration" : {
          "$ref" : "#/definitions/InputProcessingConfiguration"
        },
        "InputParallelism" : {
          "$ref" : "#/definitions/InputParallelism"
        }
      },
      "required" : [ "NamePrefix", "InputSchema" ]
    },
    "InputSchema" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RecordEncoding" : {
          "type" : "string"
        },
        "RecordColumns" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/RecordColumn"
          }
        },
        "RecordFormat" : {
          "$ref" : "#/definitions/RecordFormat"
        }
      },
      "required" : [ "RecordColumns", "RecordFormat" ]
    },
    "KinesisStreamsInput" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ResourceARN" : {
          "type" : "string"
        },
        "RoleARN" : {
          "type" : "string"
        }
      },
      "required" : [ "ResourceARN", "RoleARN" ]
    },
    "KinesisFirehoseInput" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ResourceARN" : {
          "type" : "string"
        },
        "RoleARN" : {
          "type" : "string"
        }
      },
      "required" : [ "ResourceARN", "RoleARN" ]
    },
    "InputProcessingConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "InputLambdaProcessor" : {
          "$ref" : "#/definitions/InputLambdaProcessor"
        }
      }
    },
    "RecordFormat" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RecordFormatType" : {
          "type" : "string"
        },
        "MappingParameters" : {
          "$ref" : "#/definitions/MappingParameters"
        }
      },
      "required" : [ "RecordFormatType" ]
    },
    "RecordColumn" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Mapping" : {
          "type" : "string"
        },
        "SqlType" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "SqlType", "Name" ]
    },
    "JSONMappingParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RecordRowPath" : {
          "type" : "string"
        }
      },
      "required" : [ "RecordRowPath" ]
    },
    "MappingParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CSVMappingParameters" : {
          "$ref" : "#/definitions/CSVMappingParameters"
        },
        "JSONMappingParameters" : {
          "$ref" : "#/definitions/JSONMappingParameters"
        }
      }
    },
    "InputParallelism" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Count" : {
          "type" : "integer"
        }
      }
    },
    "InputLambdaProcessor" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ResourceARN" : {
          "type" : "string"
        },
        "RoleARN" : {
          "type" : "string"
        }
      },
      "required" : [ "ResourceARN", "RoleARN" ]
    },
    "CSVMappingParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RecordColumnDelimiter" : {
          "type" : "string"
        },
        "RecordRowDelimiter" : {
          "type" : "string"
        }
      },
      "required" : [ "RecordRowDelimiter", "RecordColumnDelimiter" ]
    }
  },
  "required" : [ "Inputs" ],
  "createOnlyProperties" : [ "/properties/ApplicationName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}