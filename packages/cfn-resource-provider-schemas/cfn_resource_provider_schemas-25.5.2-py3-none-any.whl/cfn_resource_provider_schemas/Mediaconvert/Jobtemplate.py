SCHEMA = {
  "typeName" : "AWS::MediaConvert::JobTemplate",
  "description" : "Resource Type definition for AWS::MediaConvert::JobTemplate",
  "additionalProperties" : False,
  "properties" : {
    "Category" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    },
    "AccelerationSettings" : {
      "$ref" : "#/definitions/AccelerationSettings"
    },
    "Priority" : {
      "type" : "integer"
    },
    "StatusUpdateInterval" : {
      "type" : "string"
    },
    "SettingsJson" : {
      "type" : "object"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "Queue" : {
      "type" : "string"
    },
    "HopDestinations" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/HopDestination"
      }
    },
    "Tags" : {
      "type" : "object"
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "AccelerationSettings" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Mode" : {
          "type" : "string"
        }
      },
      "required" : [ "Mode" ]
    },
    "HopDestination" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "WaitMinutes" : {
          "type" : "integer"
        },
        "Queue" : {
          "type" : "string"
        },
        "Priority" : {
          "type" : "integer"
        }
      }
    }
  },
  "required" : [ "SettingsJson" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Arn" ]
}