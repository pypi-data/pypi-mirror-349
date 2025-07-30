SCHEMA = {
  "typeName" : "AWS::Greengrass::LoggerDefinition",
  "description" : "Resource Type definition for AWS::Greengrass::LoggerDefinition",
  "additionalProperties" : False,
  "properties" : {
    "LatestVersionArn" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    },
    "InitialVersion" : {
      "$ref" : "#/definitions/LoggerDefinitionVersion"
    },
    "Tags" : {
      "type" : "object"
    }
  },
  "definitions" : {
    "LoggerDefinitionVersion" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Loggers" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Logger"
          }
        }
      },
      "required" : [ "Loggers" ]
    },
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
  "required" : [ "Name" ],
  "readOnlyProperties" : [ "/properties/LatestVersionArn", "/properties/Arn", "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/InitialVersion" ],
  "primaryIdentifier" : [ "/properties/Id" ]
}