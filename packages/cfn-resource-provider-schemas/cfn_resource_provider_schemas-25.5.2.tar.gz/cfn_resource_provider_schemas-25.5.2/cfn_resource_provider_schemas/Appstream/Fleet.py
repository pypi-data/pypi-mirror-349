SCHEMA = {
  "typeName" : "AWS::AppStream::Fleet",
  "description" : "Resource Type definition for AWS::AppStream::Fleet",
  "additionalProperties" : False,
  "properties" : {
    "Description" : {
      "type" : "string"
    },
    "ComputeCapacity" : {
      "$ref" : "#/definitions/ComputeCapacity"
    },
    "Platform" : {
      "type" : "string"
    },
    "VpcConfig" : {
      "$ref" : "#/definitions/VpcConfig"
    },
    "FleetType" : {
      "type" : "string"
    },
    "EnableDefaultInternetAccess" : {
      "type" : "boolean"
    },
    "DomainJoinInfo" : {
      "$ref" : "#/definitions/DomainJoinInfo"
    },
    "SessionScriptS3Location" : {
      "$ref" : "#/definitions/S3Location"
    },
    "Name" : {
      "type" : "string"
    },
    "ImageName" : {
      "type" : "string"
    },
    "MaxUserDurationInSeconds" : {
      "type" : "integer"
    },
    "IdleDisconnectTimeoutInSeconds" : {
      "type" : "integer"
    },
    "UsbDeviceFilterStrings" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "DisconnectTimeoutInSeconds" : {
      "type" : "integer"
    },
    "DisplayName" : {
      "type" : "string"
    },
    "StreamView" : {
      "type" : "string"
    },
    "IamRoleArn" : {
      "type" : "string"
    },
    "MaxSessionsPerInstance" : {
      "type" : "integer"
    },
    "Id" : {
      "type" : "string"
    },
    "InstanceType" : {
      "type" : "string"
    },
    "MaxConcurrentSessions" : {
      "type" : "integer"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "ImageArn" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "ComputeCapacity" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DesiredInstances" : {
          "type" : "integer"
        },
        "DesiredSessions" : {
          "type" : "integer"
        }
      }
    },
    "VpcConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SubnetIds" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "SecurityGroupIds" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "DomainJoinInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OrganizationalUnitDistinguishedName" : {
          "type" : "string"
        },
        "DirectoryName" : {
          "type" : "string"
        }
      }
    },
    "Tag" : {
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
    "S3Location" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "S3Bucket" : {
          "type" : "string"
        },
        "S3Key" : {
          "type" : "string"
        }
      },
      "required" : [ "S3Bucket", "S3Key" ]
    }
  },
  "required" : [ "InstanceType", "Name" ],
  "createOnlyProperties" : [ "/properties/Name", "/properties/FleetType" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}