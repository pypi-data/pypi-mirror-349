SCHEMA = {
  "typeName" : "AWS::Glue::SecurityConfiguration",
  "description" : "Resource Type definition for AWS::Glue::SecurityConfiguration",
  "additionalProperties" : False,
  "properties" : {
    "EncryptionConfiguration" : {
      "$ref" : "#/definitions/EncryptionConfiguration"
    },
    "Name" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "S3Encryptions" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "EncryptionConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "S3Encryptions" : {
          "$ref" : "#/definitions/S3Encryptions"
        },
        "JobBookmarksEncryption" : {
          "$ref" : "#/definitions/JobBookmarksEncryption"
        },
        "CloudWatchEncryption" : {
          "$ref" : "#/definitions/CloudWatchEncryption"
        }
      }
    },
    "CloudWatchEncryption" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "KmsKeyArn" : {
          "type" : "string"
        },
        "CloudWatchEncryptionMode" : {
          "type" : "string"
        }
      }
    },
    "JobBookmarksEncryption" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "KmsKeyArn" : {
          "type" : "string"
        },
        "JobBookmarksEncryptionMode" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "EncryptionConfiguration", "Name" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}