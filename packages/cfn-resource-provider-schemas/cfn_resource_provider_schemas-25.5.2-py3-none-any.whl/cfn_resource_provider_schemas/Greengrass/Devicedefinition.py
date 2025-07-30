SCHEMA = {
  "typeName" : "AWS::Greengrass::DeviceDefinition",
  "description" : "Resource Type definition for AWS::Greengrass::DeviceDefinition",
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
      "$ref" : "#/definitions/DeviceDefinitionVersion"
    },
    "Tags" : {
      "type" : "object"
    }
  },
  "definitions" : {
    "DeviceDefinitionVersion" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Devices" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Device"
          }
        }
      },
      "required" : [ "Devices" ]
    },
    "Device" : {
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