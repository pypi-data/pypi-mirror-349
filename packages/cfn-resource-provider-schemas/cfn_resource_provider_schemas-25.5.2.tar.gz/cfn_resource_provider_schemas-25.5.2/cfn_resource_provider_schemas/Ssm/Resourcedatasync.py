SCHEMA = {
  "typeName" : "AWS::SSM::ResourceDataSync",
  "description" : "Resource Type definition for AWS::SSM::ResourceDataSync",
  "additionalProperties" : False,
  "properties" : {
    "S3Destination" : {
      "$ref" : "#/definitions/S3Destination"
    },
    "KMSKeyArn" : {
      "type" : "string",
      "minLength" : 0,
      "maxLength" : 512
    },
    "SyncSource" : {
      "$ref" : "#/definitions/SyncSource"
    },
    "BucketName" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 2048
    },
    "BucketRegion" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 64
    },
    "SyncFormat" : {
      "type" : "string",
      "minLength" : 0,
      "maxLength" : 1024
    },
    "SyncName" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 64
    },
    "SyncType" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 64
    },
    "BucketPrefix" : {
      "type" : "string",
      "minLength" : 0,
      "maxLength" : 64
    }
  },
  "definitions" : {
    "S3Destination" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "KMSKeyArn" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 512
        },
        "BucketPrefix" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 256
        },
        "BucketName" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 2048
        },
        "BucketRegion" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 64
        },
        "SyncFormat" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 1024
        }
      },
      "required" : [ "BucketName", "BucketRegion", "SyncFormat" ]
    },
    "SyncSource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IncludeFutureRegions" : {
          "type" : "boolean"
        },
        "SourceRegions" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "SourceType" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 64
        },
        "AwsOrganizationsSource" : {
          "$ref" : "#/definitions/AwsOrganizationsSource"
        }
      },
      "required" : [ "SourceType", "SourceRegions" ]
    },
    "AwsOrganizationsSource" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OrganizationalUnits" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "OrganizationSourceType" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 64
        }
      },
      "required" : [ "OrganizationSourceType" ]
    }
  },
  "required" : [ "SyncName" ],
  "createOnlyProperties" : [ "/properties/KMSKeyArn", "/properties/SyncFormat", "/properties/BucketPrefix", "/properties/SyncName", "/properties/BucketRegion", "/properties/BucketName", "/properties/S3Destination", "/properties/SyncType" ],
  "primaryIdentifier" : [ "/properties/SyncName" ],
  "tagging" : {
    "taggable" : False
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "ssm:CreateResourceDataSync", "ssm:ListResourceDataSync" ]
    },
    "delete" : {
      "permissions" : [ "ssm:ListResourceDataSync", "ssm:DeleteResourceDataSync" ]
    },
    "update" : {
      "permissions" : [ "ssm:ListResourceDataSync", "ssm:UpdateResourceDataSync" ]
    },
    "list" : {
      "permissions" : [ "ssm:ListResourceDataSync" ]
    },
    "read" : {
      "permissions" : [ "ssm:ListResourceDataSync" ]
    }
  }
}