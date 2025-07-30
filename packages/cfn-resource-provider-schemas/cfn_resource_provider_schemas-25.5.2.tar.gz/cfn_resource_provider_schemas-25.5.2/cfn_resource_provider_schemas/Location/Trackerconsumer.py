SCHEMA = {
  "typeName" : "AWS::Location::TrackerConsumer",
  "description" : "Definition of AWS::Location::TrackerConsumer Resource Type",
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "properties" : {
    "ConsumerArn" : {
      "type" : "string",
      "maxLength" : 1600,
      "pattern" : "^arn(:[a-z0-9]+([.-][a-z0-9]+)*){2}(:([a-z0-9]+([.-][a-z0-9]+)*)?){2}:([^/].*)?$"
    },
    "TrackerName" : {
      "type" : "string",
      "maxLength" : 100,
      "minLength" : 1,
      "pattern" : "^[-._\\w]+$"
    }
  },
  "additionalProperties" : False,
  "required" : [ "ConsumerArn", "TrackerName" ],
  "createOnlyProperties" : [ "/properties/TrackerName", "/properties/ConsumerArn" ],
  "primaryIdentifier" : [ "/properties/TrackerName", "/properties/ConsumerArn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "geo:AssociateTrackerConsumer", "geo:ListTrackerConsumers" ]
    },
    "delete" : {
      "permissions" : [ "geo:DisassociateTrackerConsumer", "geo:ListTrackerConsumers" ]
    },
    "list" : {
      "permissions" : [ "geo:ListTrackerConsumers" ]
    },
    "read" : {
      "permissions" : [ "geo:ListTrackerConsumers" ]
    }
  }
}