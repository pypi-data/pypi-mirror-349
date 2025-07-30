SCHEMA = {
  "typeName" : "AWS::Neptune::EventSubscription",
  "description" : "Resource Type definition for AWS::Neptune::EventSubscription",
  "additionalProperties" : False,
  "properties" : {
    "Enabled" : {
      "type" : "boolean"
    },
    "EventCategories" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "SnsTopicArn" : {
      "type" : "string"
    },
    "SourceIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Id" : {
      "type" : "string"
    },
    "SourceType" : {
      "type" : "string"
    }
  },
  "createOnlyProperties" : [ "/properties/SnsTopicArn" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}