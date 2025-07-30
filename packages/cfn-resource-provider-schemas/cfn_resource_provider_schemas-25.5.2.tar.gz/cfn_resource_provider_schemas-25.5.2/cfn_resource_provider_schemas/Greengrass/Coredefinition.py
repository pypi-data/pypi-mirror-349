SCHEMA = {
  "typeName" : "AWS::Greengrass::CoreDefinition",
  "description" : "Resource Type definition for AWS::Greengrass::CoreDefinition",
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
      "$ref" : "#/definitions/CoreDefinitionVersion"
    },
    "Tags" : {
      "type" : "object"
    }
  },
  "definitions" : {
    "CoreDefinitionVersion" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Cores" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Core"
          }
        }
      },
      "required" : [ "Cores" ]
    },
    "Core" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SyncShadow" : {
          "type" : "boolean"
        },
        "ThingArn" : {
          "type" : "string"
        },
        "Id" : {
          "type" : "string"
        },
        "CertificateArn" : {
          "type" : "string"
        }
      },
      "required" : [ "ThingArn", "Id", "CertificateArn" ]
    }
  },
  "required" : [ "Name" ],
  "readOnlyProperties" : [ "/properties/LatestVersionArn", "/properties/Arn", "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/InitialVersion" ],
  "primaryIdentifier" : [ "/properties/Id" ]
}