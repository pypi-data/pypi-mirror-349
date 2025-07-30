SCHEMA = {
  "typeName" : "Alexa::ASK::Skill",
  "description" : "Resource Type definition for Alexa::ASK::Skill",
  "additionalProperties" : False,
  "properties" : {
    "AuthenticationConfiguration" : {
      "$ref" : "#/definitions/AuthenticationConfiguration"
    },
    "Id" : {
      "type" : "string"
    },
    "VendorId" : {
      "type" : "string"
    },
    "SkillPackage" : {
      "$ref" : "#/definitions/SkillPackage"
    }
  },
  "definitions" : {
    "AuthenticationConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ClientId" : {
          "type" : "string"
        },
        "RefreshToken" : {
          "type" : "string"
        },
        "ClientSecret" : {
          "type" : "string"
        }
      },
      "required" : [ "RefreshToken", "ClientSecret", "ClientId" ]
    },
    "Overrides" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Manifest" : {
          "type" : "object"
        }
      }
    },
    "SkillPackage" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "S3BucketRole" : {
          "type" : "string"
        },
        "Overrides" : {
          "$ref" : "#/definitions/Overrides"
        },
        "S3ObjectVersion" : {
          "type" : "string"
        },
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
  "required" : [ "AuthenticationConfiguration", "VendorId", "SkillPackage" ],
  "createOnlyProperties" : [ "/properties/VendorId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}