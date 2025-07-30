SCHEMA = {
  "typeName" : "AWS::Config::DeliveryChannel",
  "description" : "Resource Type definition for AWS::Config::DeliveryChannel",
  "additionalProperties" : False,
  "properties" : {
    "S3KeyPrefix" : {
      "type" : "string"
    },
    "ConfigSnapshotDeliveryProperties" : {
      "$ref" : "#/definitions/ConfigSnapshotDeliveryProperties"
    },
    "S3BucketName" : {
      "type" : "string"
    },
    "SnsTopicARN" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "S3KmsKeyArn" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "ConfigSnapshotDeliveryProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DeliveryFrequency" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "S3BucketName" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}