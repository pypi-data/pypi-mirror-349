SCHEMA = {
  "typeName" : "AWS::Greengrass::LoggerDefinitionVersion",
  "description" : "Resource Type definition for AWS::Greengrass::LoggerDefinitionVersion",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "LoggerDefinitionId" : {
      "type" : "string"
    },
    "Loggers" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Logger"
      }
    }
  },
  "definitions" : {
    "Logger" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Space" : {
          "type" : "integer"
        },
        "Type" : {
          "type" : "string"
        },
        "Level" : {
          "type" : "string"
        },
        "Id" : {
          "type" : "string"
        },
        "Component" : {
          "type" : "string"
        }
      },
      "required" : [ "Type", "Level", "Id", "Component" ]
    }
  },
  "required" : [ "Loggers", "LoggerDefinitionId" ],
  "createOnlyProperties" : [ "/properties/LoggerDefinitionId", "/properties/Loggers" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}