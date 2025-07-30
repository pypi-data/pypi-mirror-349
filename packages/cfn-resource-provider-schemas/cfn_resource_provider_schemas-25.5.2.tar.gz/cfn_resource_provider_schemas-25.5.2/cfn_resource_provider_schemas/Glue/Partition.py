SCHEMA = {
  "typeName" : "AWS::Glue::Partition",
  "description" : "Resource Type definition for AWS::Glue::Partition",
  "additionalProperties" : False,
  "properties" : {
    "DatabaseName" : {
      "type" : "string"
    },
    "TableName" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "CatalogId" : {
      "type" : "string"
    },
    "PartitionInput" : {
      "$ref" : "#/definitions/PartitionInput"
    }
  },
  "definitions" : {
    "SchemaReference" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SchemaId" : {
          "$ref" : "#/definitions/SchemaId"
        },
        "SchemaVersionId" : {
          "type" : "string"
        },
        "SchemaVersionNumber" : {
          "type" : "integer"
        }
      }
    },
    "Order" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Column" : {
          "type" : "string"
        },
        "SortOrder" : {
          "type" : "integer"
        }
      },
      "required" : [ "Column" ]
    },
    "SkewedInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SkewedColumnValues" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "SkewedColumnValueLocationMaps" : {
          "type" : "object"
        },
        "SkewedColumnNames" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "Column" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Comment" : {
          "type" : "string"
        },
        "Type" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "Name" ]
    },
    "StorageDescriptor" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "StoredAsSubDirectories" : {
          "type" : "boolean"
        },
        "Parameters" : {
          "type" : "object"
        },
        "BucketColumns" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "NumberOfBuckets" : {
          "type" : "integer"
        },
        "OutputFormat" : {
          "type" : "string"
        },
        "Columns" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Column"
          }
        },
        "SerdeInfo" : {
          "$ref" : "#/definitions/SerdeInfo"
        },
        "SortColumns" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Order"
          }
        },
        "Compressed" : {
          "type" : "boolean"
        },
        "SchemaReference" : {
          "$ref" : "#/definitions/SchemaReference"
        },
        "SkewedInfo" : {
          "$ref" : "#/definitions/SkewedInfo"
        },
        "InputFormat" : {
          "type" : "string"
        },
        "Location" : {
          "type" : "string"
        }
      }
    },
    "SchemaId" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RegistryName" : {
          "type" : "string"
        },
        "SchemaName" : {
          "type" : "string"
        },
        "SchemaArn" : {
          "type" : "string"
        }
      }
    },
    "SerdeInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Parameters" : {
          "type" : "object"
        },
        "SerializationLibrary" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      }
    },
    "PartitionInput" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "StorageDescriptor" : {
          "$ref" : "#/definitions/StorageDescriptor"
        },
        "Values" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Parameters" : {
          "type" : "object"
        }
      },
      "required" : [ "Values" ]
    }
  },
  "required" : [ "TableName", "DatabaseName", "CatalogId", "PartitionInput" ],
  "createOnlyProperties" : [ "/properties/TableName", "/properties/DatabaseName", "/properties/CatalogId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}