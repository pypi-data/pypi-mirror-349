SCHEMA = {
  "typeName" : "AWS::CloudFront::StreamingDistribution",
  "description" : "Resource Type definition for AWS::CloudFront::StreamingDistribution",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "DomainName" : {
      "type" : "string"
    },
    "StreamingDistributionConfig" : {
      "$ref" : "#/definitions/StreamingDistributionConfig"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "definitions" : {
    "StreamingDistributionConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Logging" : {
          "$ref" : "#/definitions/Logging"
        },
        "Comment" : {
          "type" : "string"
        },
        "PriceClass" : {
          "type" : "string"
        },
        "S3Origin" : {
          "$ref" : "#/definitions/S3Origin"
        },
        "Enabled" : {
          "type" : "boolean"
        },
        "Aliases" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "TrustedSigners" : {
          "$ref" : "#/definitions/TrustedSigners"
        }
      },
      "required" : [ "Comment", "Enabled", "S3Origin", "TrustedSigners" ]
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
    },
    "TrustedSigners" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "AwsAccountNumbers" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "Enabled" ]
    },
    "Logging" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Bucket" : {
          "type" : "string"
        },
        "Enabled" : {
          "type" : "boolean"
        },
        "Prefix" : {
          "type" : "string"
        }
      },
      "required" : [ "Bucket", "Enabled", "Prefix" ]
    },
    "S3Origin" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DomainName" : {
          "type" : "string"
        },
        "OriginAccessIdentity" : {
          "type" : "string"
        }
      },
      "required" : [ "DomainName", "OriginAccessIdentity" ]
    }
  },
  "required" : [ "StreamingDistributionConfig", "Tags" ],
  "readOnlyProperties" : [ "/properties/DomainName", "/properties/Id" ],
  "primaryIdentifier" : [ "/properties/Id" ]
}