SCHEMA = {
  "typeName" : "AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource",
  "description" : "Resource Type definition for AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "ApplicationName" : {
      "type" : "string"
    },
    "ReferenceDataSource" : {
      "$ref" : "#/definitions/ReferenceDataSource"
    }
  },
  "definitions" : {
    "ReferenceDataSource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ReferenceSchema" : {
          "$ref" : "#/definitions/ReferenceSchema"
        },
        "TableName" : {
          "type" : "string"
        },
        "S3ReferenceDataSource" : {
          "$ref" : "#/definitions/S3ReferenceDataSource"
        }
      },
      "required" : [ "ReferenceSchema" ]
    },
    "ReferenceSchema" : {
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
    "S3ReferenceDataSource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "BucketARN" : {
          "type" : "string"
        },
        "FileKey" : {
          "type" : "string"
        }
      },
      "required" : [ "BucketARN", "FileKey" ]
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
    "RecordFormat" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MappingParameters" : {
          "$ref" : "#/definitions/MappingParameters"
        },
        "RecordFormatType" : {
          "type" : "string"
        }
      },
      "required" : [ "RecordFormatType" ]
    },
    "MappingParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "JSONMappingParameters" : {
          "$ref" : "#/definitions/JSONMappingParameters"
        },
        "CSVMappingParameters" : {
          "$ref" : "#/definitions/CSVMappingParameters"
        }
      }
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
    "CSVMappingParameters" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RecordRowDelimiter" : {
          "type" : "string"
        },
        "RecordColumnDelimiter" : {
          "type" : "string"
        }
      },
      "required" : [ "RecordColumnDelimiter", "RecordRowDelimiter" ]
    }
  },
  "required" : [ "ReferenceDataSource", "ApplicationName" ],
  "createOnlyProperties" : [ "/properties/ApplicationName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}