SCHEMA = {
  "typeName" : "AWS::DMS::ReplicationTask",
  "description" : "Resource Type definition for AWS::DMS::ReplicationTask",
  "additionalProperties" : False,
  "properties" : {
    "ReplicationTaskSettings" : {
      "type" : "string"
    },
    "CdcStartPosition" : {
      "type" : "string"
    },
    "CdcStopPosition" : {
      "type" : "string"
    },
    "MigrationType" : {
      "type" : "string"
    },
    "TargetEndpointArn" : {
      "type" : "string"
    },
    "ReplicationInstanceArn" : {
      "type" : "string"
    },
    "TaskData" : {
      "type" : "string"
    },
    "CdcStartTime" : {
      "type" : "number"
    },
    "ResourceIdentifier" : {
      "type" : "string"
    },
    "TableMappings" : {
      "type" : "string"
    },
    "ReplicationTaskIdentifier" : {
      "type" : "string"
    },
    "SourceEndpointArn" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
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
    }
  },
  "required" : [ "TableMappings", "SourceEndpointArn", "MigrationType", "TargetEndpointArn", "ReplicationInstanceArn" ],
  "createOnlyProperties" : [ "/properties/ResourceIdentifier", "/properties/TargetEndpointArn", "/properties/ReplicationInstanceArn", "/properties/SourceEndpointArn" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}