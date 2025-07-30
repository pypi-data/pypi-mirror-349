SCHEMA = {
  "typeName" : "AWS::Greengrass::ConnectorDefinition",
  "description" : "Resource Type definition for AWS::Greengrass::ConnectorDefinition",
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
      "$ref" : "#/definitions/ConnectorDefinitionVersion"
    },
    "Tags" : {
      "type" : "object"
    }
  },
  "definitions" : {
    "ConnectorDefinitionVersion" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Connectors" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Connector"
          }
        }
      },
      "required" : [ "Connectors" ]
    },
    "Connector" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ConnectorArn" : {
          "type" : "string"
        },
        "Parameters" : {
          "type" : "object"
        },
        "Id" : {
          "type" : "string"
        }
      },
      "required" : [ "ConnectorArn", "Id" ]
    }
  },
  "required" : [ "Name" ],
  "readOnlyProperties" : [ "/properties/LatestVersionArn", "/properties/Arn", "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/InitialVersion" ],
  "primaryIdentifier" : [ "/properties/Id" ]
}