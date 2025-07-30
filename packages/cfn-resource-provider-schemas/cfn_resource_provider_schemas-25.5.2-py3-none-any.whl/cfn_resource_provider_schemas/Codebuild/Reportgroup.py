SCHEMA = {
  "typeName" : "AWS::CodeBuild::ReportGroup",
  "description" : "Resource Type definition for AWS::CodeBuild::ReportGroup",
  "additionalProperties" : False,
  "properties" : {
    "Type" : {
      "type" : "string"
    },
    "ExportConfig" : {
      "$ref" : "#/definitions/ReportExportConfig"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "DeleteReports" : {
      "type" : "boolean"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "S3ReportExportConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Path" : {
          "type" : "string"
        },
        "Bucket" : {
          "type" : "string"
        },
        "Packaging" : {
          "type" : "string"
        },
        "EncryptionKey" : {
          "type" : "string"
        },
        "BucketOwner" : {
          "type" : "string"
        },
        "EncryptionDisabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Bucket" ]
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
    "ReportExportConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "S3Destination" : {
          "$ref" : "#/definitions/S3ReportExportConfig"
        },
        "ExportConfigType" : {
          "type" : "string"
        }
      },
      "required" : [ "ExportConfigType" ]
    }
  },
  "required" : [ "Type", "ExportConfig" ],
  "createOnlyProperties" : [ "/properties/Name", "/properties/Type" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Arn" ]
}