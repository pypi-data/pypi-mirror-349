SCHEMA = {
  "typeName" : "AWS::WorkSpaces::Workspace",
  "description" : "Resource Type definition for AWS::WorkSpaces::Workspace",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "BundleId" : {
      "type" : "string"
    },
    "DirectoryId" : {
      "type" : "string"
    },
    "RootVolumeEncryptionEnabled" : {
      "type" : "boolean"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "UserName" : {
      "type" : "string"
    },
    "UserVolumeEncryptionEnabled" : {
      "type" : "boolean"
    },
    "VolumeEncryptionKey" : {
      "type" : "string"
    },
    "WorkspaceProperties" : {
      "$ref" : "#/definitions/WorkspaceProperties"
    }
  },
  "definitions" : {
    "WorkspaceProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ComputeTypeName" : {
          "type" : "string"
        },
        "RootVolumeSizeGib" : {
          "type" : "integer"
        },
        "RunningMode" : {
          "type" : "string"
        },
        "RunningModeAutoStopTimeoutInMinutes" : {
          "type" : "integer"
        },
        "UserVolumeSizeGib" : {
          "type" : "integer"
        }
      }
    },
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    }
  },
  "required" : [ "BundleId", "DirectoryId", "UserName" ],
  "createOnlyProperties" : [ "/properties/UserName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}