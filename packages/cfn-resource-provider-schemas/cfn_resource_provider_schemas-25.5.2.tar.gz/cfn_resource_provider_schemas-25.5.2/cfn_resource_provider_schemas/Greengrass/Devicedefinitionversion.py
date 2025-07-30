SCHEMA = {
  "typeName" : "AWS::Greengrass::DeviceDefinitionVersion",
  "description" : "Resource Type definition for AWS::Greengrass::DeviceDefinitionVersion",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "DeviceDefinitionId" : {
      "type" : "string"
    },
    "Devices" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Device"
      }
    }
  },
  "definitions" : {
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
  "required" : [ "Devices", "DeviceDefinitionId" ],
  "createOnlyProperties" : [ "/properties/DeviceDefinitionId", "/properties/Devices" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}