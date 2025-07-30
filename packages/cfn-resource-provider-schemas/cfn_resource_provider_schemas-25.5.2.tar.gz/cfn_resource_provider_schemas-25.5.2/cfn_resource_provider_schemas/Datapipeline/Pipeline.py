SCHEMA = {
  "typeName" : "AWS::DataPipeline::Pipeline",
  "description" : "Resource Type definition for AWS::DataPipeline::Pipeline",
  "additionalProperties" : False,
  "properties" : {
    "PipelineTags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/PipelineTag"
      }
    },
    "ParameterObjects" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/ParameterObject"
      }
    },
    "Description" : {
      "type" : "string"
    },
    "Activate" : {
      "type" : "boolean"
    },
    "PipelineObjects" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/PipelineObject"
      }
    },
    "Id" : {
      "type" : "string"
    },
    "ParameterValues" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/ParameterValue"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "ParameterAttribute" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "StringValue" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "StringValue", "Key" ]
    },
    "PipelineTag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    },
    "Field" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RefValue" : {
          "type" : "string"
        },
        "StringValue" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Key" ]
    },
    "ParameterValue" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "StringValue" : {
          "type" : "string"
        },
        "Id" : {
          "type" : "string"
        }
      },
      "required" : [ "Id", "StringValue" ]
    },
    "PipelineObject" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Fields" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Field"
          }
        },
        "Id" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "Fields", "Id", "Name" ]
    },
    "ParameterObject" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Attributes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/ParameterAttribute"
          }
        },
        "Id" : {
          "type" : "string"
        }
      },
      "required" : [ "Attributes", "Id" ]
    }
  },
  "required" : [ "ParameterObjects", "Name" ],
  "createOnlyProperties" : [ "/properties/Name", "/properties/Description" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}