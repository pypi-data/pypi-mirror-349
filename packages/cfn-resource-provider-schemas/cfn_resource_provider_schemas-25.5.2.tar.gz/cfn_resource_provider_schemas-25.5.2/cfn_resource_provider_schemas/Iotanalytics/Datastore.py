SCHEMA = {
  "typeName" : "AWS::IoTAnalytics::Datastore",
  "description" : "Resource Type definition for AWS::IoTAnalytics::Datastore",
  "additionalProperties" : False,
  "taggable" : True,
  "properties" : {
    "DatastoreStorage" : {
      "$ref" : "#/definitions/DatastoreStorage"
    },
    "DatastoreName" : {
      "type" : "string",
      "pattern" : "[a-zA-Z0-9_]+",
      "minLength" : 1,
      "maxLength" : 128
    },
    "DatastorePartitions" : {
      "$ref" : "#/definitions/DatastorePartitions"
    },
    "Id" : {
      "type" : "string"
    },
    "FileFormatConfiguration" : {
      "$ref" : "#/definitions/FileFormatConfiguration"
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
    "DatastoreStorage" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ServiceManagedS3" : {
          "$ref" : "#/definitions/ServiceManagedS3"
        },
        "CustomerManagedS3" : {
          "$ref" : "#/definitions/CustomerManagedS3"
        },
        "IotSiteWiseMultiLayerStorage" : {
          "$ref" : "#/definitions/IotSiteWiseMultiLayerStorage"
        }
      }
    },
    "SchemaDefinition" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Columns" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "minItems" : 1,
          "maxItems" : 100,
          "items" : {
            "$ref" : "#/definitions/Column"
          }
        }
      }
    },
    "JsonConfiguration" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "ParquetConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SchemaDefinition" : {
          "$ref" : "#/definitions/SchemaDefinition"
        }
      }
    },
    "FileFormatConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "JsonConfiguration" : {
          "$ref" : "#/definitions/JsonConfiguration"
        },
        "ParquetConfiguration" : {
          "$ref" : "#/definitions/ParquetConfiguration"
        }
      }
    },
    "Column" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "Type", "Name" ]
    },
    "CustomerManagedS3" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Bucket" : {
          "type" : "string",
          "pattern" : "[a-zA-Z0-9.\\-_]*",
          "minLength" : 3,
          "maxLength" : 255
        },
        "RoleArn" : {
          "type" : "string",
          "minLength" : 20,
          "maxLength" : 2048
        },
        "KeyPrefix" : {
          "type" : "string",
          "pattern" : "[a-zA-Z0-9!_.*'()/{}:-]*/",
          "minLength" : 1,
          "maxLength" : 255
        }
      },
      "required" : [ "Bucket", "RoleArn" ]
    },
    "IotSiteWiseMultiLayerStorage" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CustomerManagedS3Storage" : {
          "$ref" : "#/definitions/CustomerManagedS3Storage"
        }
      }
    },
    "CustomerManagedS3Storage" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Bucket" : {
          "type" : "string",
          "pattern" : "[a-zA-Z0-9.\\-_]*",
          "minLength" : 3,
          "maxLength" : 255
        },
        "KeyPrefix" : {
          "type" : "string",
          "pattern" : "[a-zA-Z0-9!_.*'()/{}:-]*/",
          "minLength" : 1,
          "maxLength" : 255
        }
      },
      "required" : [ "Bucket" ]
    },
    "ServiceManagedS3" : {
      "type" : "object",
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
    "DatastorePartitions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Partitions" : {
          "type" : "array",
          "uniqueItems" : False,
          "insertionOrder" : False,
          "minItems" : 0,
          "maxItems" : 25,
          "items" : {
            "$ref" : "#/definitions/DatastorePartition"
          }
        }
      }
    },
    "DatastorePartition" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Partition" : {
          "$ref" : "#/definitions/Partition"
        },
        "TimestampPartition" : {
          "$ref" : "#/definitions/TimestampPartition"
        }
      }
    },
    "Partition" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AttributeName" : {
          "type" : "string",
          "pattern" : "[a-zA-Z0-9_]+"
        }
      },
      "required" : [ "AttributeName" ]
    },
    "TimestampPartition" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AttributeName" : {
          "type" : "string",
          "pattern" : "[a-zA-Z0-9_]+"
        },
        "TimestampFormat" : {
          "type" : "string",
          "pattern" : "[a-zA-Z0-9\\s\\[\\]_,.'/:-]*"
        }
      },
      "required" : [ "AttributeName" ]
    }
  },
  "primaryIdentifier" : [ "/properties/DatastoreName" ],
  "createOnlyProperties" : [ "/properties/DatastoreName" ],
  "readOnlyProperties" : [ "/properties/Id" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iotanalytics:CreateDatastore" ]
    },
    "read" : {
      "permissions" : [ "iotanalytics:DescribeDatastore", "iotanalytics:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "iotanalytics:UpdateDatastore", "iotanalytics:TagResource", "iotanalytics:UntagResource" ]
    },
    "delete" : {
      "permissions" : [ "iotanalytics:DeleteDatastore" ]
    },
    "list" : {
      "permissions" : [ "iotanalytics:ListDatastores" ]
    }
  }
}