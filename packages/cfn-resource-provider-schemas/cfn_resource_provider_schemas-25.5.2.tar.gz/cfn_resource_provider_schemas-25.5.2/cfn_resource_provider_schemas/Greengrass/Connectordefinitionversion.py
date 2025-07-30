SCHEMA = {
  "typeName" : "AWS::Greengrass::ConnectorDefinitionVersion",
  "description" : "Resource Type definition for AWS::Greengrass::ConnectorDefinitionVersion",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Connectors" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Connector"
      }
    },
    "ConnectorDefinitionId" : {
      "type" : "string"
    }
  },
  "definitions" : {
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
  "required" : [ "Connectors", "ConnectorDefinitionId" ],
  "createOnlyProperties" : [ "/properties/ConnectorDefinitionId", "/properties/Connectors" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}