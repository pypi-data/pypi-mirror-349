SCHEMA = {
  "typeName" : "AWS::IoTFleetWise::SignalCatalog",
  "description" : "Definition of AWS::IoTFleetWise::SignalCatalog Resource Type",
  "definitions" : {
    "Actuator" : {
      "type" : "object",
      "properties" : {
        "FullyQualifiedName" : {
          "type" : "string"
        },
        "DataType" : {
          "$ref" : "#/definitions/NodeDataType"
        },
        "Description" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^[^\\u0000-\\u001F\\u007F]+$"
        },
        "Unit" : {
          "type" : "string"
        },
        "AllowedValues" : {
          "$ref" : "#/definitions/AllowedValues"
        },
        "Min" : {
          "type" : "number"
        },
        "Max" : {
          "type" : "number"
        },
        "AssignedValue" : {
          "type" : "string"
        }
      },
      "required" : [ "DataType", "FullyQualifiedName" ],
      "additionalProperties" : False
    },
    "AllowedValues" : {
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "type" : "string"
      },
      "minItems" : 1
    },
    "Attribute" : {
      "type" : "object",
      "properties" : {
        "FullyQualifiedName" : {
          "type" : "string"
        },
        "DataType" : {
          "$ref" : "#/definitions/NodeDataType"
        },
        "Description" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^[^\\u0000-\\u001F\\u007F]+$"
        },
        "Unit" : {
          "type" : "string"
        },
        "AllowedValues" : {
          "$ref" : "#/definitions/AllowedValues"
        },
        "Min" : {
          "type" : "number"
        },
        "Max" : {
          "type" : "number"
        },
        "AssignedValue" : {
          "type" : "string"
        },
        "DefaultValue" : {
          "type" : "string"
        }
      },
      "required" : [ "DataType", "FullyQualifiedName" ],
      "additionalProperties" : False
    },
    "Branch" : {
      "type" : "object",
      "properties" : {
        "FullyQualifiedName" : {
          "type" : "string"
        },
        "Description" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^[^\\u0000-\\u001F\\u007F]+$"
        }
      },
      "required" : [ "FullyQualifiedName" ],
      "additionalProperties" : False
    },
    "Node" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "Branch",
        "properties" : {
          "Branch" : {
            "$ref" : "#/definitions/Branch"
          }
        },
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Sensor",
        "properties" : {
          "Sensor" : {
            "$ref" : "#/definitions/Sensor"
          }
        },
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Actuator",
        "properties" : {
          "Actuator" : {
            "$ref" : "#/definitions/Actuator"
          }
        },
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Attribute",
        "properties" : {
          "Attribute" : {
            "$ref" : "#/definitions/Attribute"
          }
        },
        "additionalProperties" : False
      } ]
    },
    "NodeCounts" : {
      "type" : "object",
      "properties" : {
        "TotalNodes" : {
          "type" : "number"
        },
        "TotalBranches" : {
          "type" : "number"
        },
        "TotalSensors" : {
          "type" : "number"
        },
        "TotalAttributes" : {
          "type" : "number"
        },
        "TotalActuators" : {
          "type" : "number"
        }
      },
      "additionalProperties" : False
    },
    "NodeDataType" : {
      "type" : "string",
      "enum" : [ "INT8", "UINT8", "INT16", "UINT16", "INT32", "UINT32", "INT64", "UINT64", "BOOLEAN", "FLOAT", "DOUBLE", "STRING", "UNIX_TIMESTAMP", "INT8_ARRAY", "UINT8_ARRAY", "INT16_ARRAY", "UINT16_ARRAY", "INT32_ARRAY", "UINT32_ARRAY", "INT64_ARRAY", "UINT64_ARRAY", "BOOLEAN_ARRAY", "FLOAT_ARRAY", "DOUBLE_ARRAY", "STRING_ARRAY", "UNIX_TIMESTAMP_ARRAY", "UNKNOWN" ]
    },
    "Sensor" : {
      "type" : "object",
      "properties" : {
        "FullyQualifiedName" : {
          "type" : "string"
        },
        "DataType" : {
          "$ref" : "#/definitions/NodeDataType"
        },
        "Description" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^[^\\u0000-\\u001F\\u007F]+$"
        },
        "Unit" : {
          "type" : "string"
        },
        "AllowedValues" : {
          "$ref" : "#/definitions/AllowedValues"
        },
        "Min" : {
          "type" : "number"
        },
        "Max" : {
          "type" : "number"
        }
      },
      "required" : [ "DataType", "FullyQualifiedName" ],
      "additionalProperties" : False
    },
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "maxLength" : 128,
          "minLength" : 1
        },
        "Value" : {
          "type" : "string",
          "maxLength" : 256,
          "minLength" : 0
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    }
  },
  "properties" : {
    "Arn" : {
      "type" : "string"
    },
    "CreationTime" : {
      "format" : "date-time",
      "type" : "string"
    },
    "Description" : {
      "type" : "string",
      "maxLength" : 2048,
      "minLength" : 1,
      "pattern" : "^[^\\u0000-\\u001F\\u007F]+$"
    },
    "LastModificationTime" : {
      "format" : "date-time",
      "type" : "string"
    },
    "Name" : {
      "type" : "string",
      "maxLength" : 100,
      "minLength" : 1,
      "pattern" : "^[a-zA-Z\\d\\-_:]+$"
    },
    "NodeCounts" : {
      "$ref" : "#/definitions/NodeCounts"
    },
    "Nodes" : {
      "type" : "array",
      "insertionOrder" : False,
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Node"
      },
      "maxItems" : 5000,
      "minItems" : 1
    },
    "Tags" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "insertionOrder" : False,
      "uniqueItems" : True,
      "maxItems" : 50,
      "minItems" : 0
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "iotfleetwise:UntagResource", "iotfleetwise:TagResource", "iotfleetwise:ListTagsForResource" ]
  },
  "readOnlyProperties" : [ "/properties/Arn", "/properties/CreationTime", "/properties/LastModificationTime", "/properties/NodeCounts/TotalNodes", "/properties/NodeCounts/TotalBranches", "/properties/NodeCounts/TotalSensors", "/properties/NodeCounts/TotalAttributes", "/properties/NodeCounts/TotalActuators" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Name" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iotfleetwise:GetSignalCatalog", "iotfleetwise:CreateSignalCatalog", "iotfleetwise:ListSignalCatalogNodes", "iotfleetwise:ListTagsForResource", "iotfleetwise:TagResource" ]
    },
    "read" : {
      "permissions" : [ "iotfleetwise:GetSignalCatalog", "iotfleetwise:ListSignalCatalogNodes", "iotfleetwise:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "iotfleetwise:GetSignalCatalog", "iotfleetwise:UpdateSignalCatalog", "iotfleetwise:ListSignalCatalogNodes", "iotfleetwise:ListTagsForResource", "iotfleetwise:TagResource", "iotfleetwise:UntagResource" ]
    },
    "delete" : {
      "permissions" : [ "iotfleetwise:GetSignalCatalog", "iotfleetwise:DeleteSignalCatalog" ]
    },
    "list" : {
      "permissions" : [ "iotfleetwise:ListSignalCatalogs" ]
    }
  },
  "additionalProperties" : False
}