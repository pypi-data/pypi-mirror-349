SCHEMA = {
  "typeName" : "AWS::KinesisAnalytics::ApplicationReferenceDataSource",
  "description" : "Resource Type definition for AWS::KinesisAnalytics::ApplicationReferenceDataSource",
  "additionalProperties" : False,
  "properties" : {
    "ReferenceDataSource" : {
      "$ref" : "#/definitions/ReferenceDataSource"
    },
    "ApplicationName" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    }
  },
  "definitions" : {
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
    "S3ReferenceDataSource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "BucketARN" : {
          "type" : "string"
        },
        "FileKey" : {
          "type" : "string"
        },
        "ReferenceRoleARN" : {
          "type" : "string"
        }
      },
      "required" : [ "BucketARN", "FileKey", "ReferenceRoleARN" ]
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
  "required" : [ "ApplicationName", "ReferenceDataSource" ],
  "createOnlyProperties" : [ "/properties/ApplicationName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}