SCHEMA = {
  "typeName" : "AWS::DocDB::EventSubscription",
  "description" : "Resource Type definition for AWS::DocDB::EventSubscription",
  "additionalProperties" : False,
  "properties" : {
    "SourceType" : {
      "type" : "string"
    },
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
    "SubscriptionName" : {
      "type" : "string"
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
    }
  },
  "required" : [ "SnsTopicArn" ],
  "createOnlyProperties" : [ "/properties/SubscriptionName", "/properties/SnsTopicArn" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}