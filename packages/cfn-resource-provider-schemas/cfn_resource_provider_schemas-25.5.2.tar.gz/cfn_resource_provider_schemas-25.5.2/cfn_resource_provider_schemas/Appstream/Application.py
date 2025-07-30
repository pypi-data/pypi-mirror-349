SCHEMA = {
  "typeName" : "AWS::AppStream::Application",
  "description" : "Resource Type definition for AWS::AppStream::Application",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-appstream.git",
  "definitions" : {
    "S3Location" : {
      "type" : "object",
      "properties" : {
        "S3Bucket" : {
          "type" : "string"
        },
        "S3Key" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False,
      "required" : [ "S3Bucket", "S3Key" ]
    },
    "Arn" : {
      "type" : "string"
    },
    "PlatformType" : {
      "type" : "string"
    },
    "Tag" : {
      "oneOf" : [ {
        "type" : "object",
        "properties" : {
          "Key" : {
            "type" : "string"
          },
          "Value" : {
            "type" : "string"
          }
        },
        "required" : [ "Key", "Value" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "properties" : {
          "TagKey" : {
            "type" : "string"
          },
          "TagValue" : {
            "type" : "string"
          }
        },
        "required" : [ "TagKey", "TagValue" ],
        "additionalProperties" : False
      } ]
    },
    "ApplicationAttribute" : {
      "type" : "string"
    }
  },
  "properties" : {
    "Name" : {
      "type" : "string"
    },
    "DisplayName" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    },
    "LaunchPath" : {
      "type" : "string"
    },
    "LaunchParameters" : {
      "type" : "string"
    },
    "WorkingDirectory" : {
      "type" : "string"
    },
    "InstanceFamilies" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      },
      "insertionOrder" : False
    },
    "IconS3Location" : {
      "$ref" : "#/definitions/S3Location"
    },
    "Arn" : {
      "$ref" : "#/definitions/Arn"
    },
    "AppBlockArn" : {
      "$ref" : "#/definitions/Arn"
    },
    "Platforms" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/PlatformType"
      },
      "insertionOrder" : False
    },
    "Tags" : {
      "type" : "array",
      "insertionOrder" : False,
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "AttributesToDelete" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/ApplicationAttribute"
      },
      "insertionOrder" : False
    },
    "CreatedTime" : {
      "type" : "string"
    }
  },
  "additionalProperties" : False,
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags"
  },
  "required" : [ "Name", "IconS3Location", "LaunchPath", "Platforms", "InstanceFamilies", "AppBlockArn" ],
  "createOnlyProperties" : [ "/properties/Name", "/properties/InstanceFamilies", "/properties/Platforms" ],
  "readOnlyProperties" : [ "/properties/Arn", "/properties/CreatedTime" ],
  "writeOnlyProperties" : [ "/properties/Tags", "/properties/AttributesToDelete" ],
  "deprecatedProperties" : [ "/properties/Tags/TagKey", "/properties/Tags/TagValue" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "s3:GetObject", "appstream:CreateApplication", "appstream:TagResource" ]
    },
    "read" : {
      "permissions" : [ "appstream:DescribeApplications" ]
    },
    "update" : {
      "permissions" : [ "appstream:UpdateApplication", "s3:GetObject" ]
    },
    "delete" : {
      "permissions" : [ "appstream:DeleteApplication" ]
    }
  }
}