SCHEMA = {
  "typeName" : "AWS::GameLiftStreams::StreamGroup",
  "description" : "Definition of AWS::GameLiftStreams::StreamGroup Resource Type",
  "definitions" : {
    "DefaultApplication" : {
      "type" : "object",
      "properties" : {
        "Id" : {
          "type" : "string",
          "maxLength" : 32,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9-]+$"
        },
        "Arn" : {
          "type" : "string",
          "maxLength" : 128,
          "minLength" : 1,
          "pattern" : "^arn:aws:gameliftstreams:([^:\n]*):([0-9]{12}):([^:\n]*)$"
        }
      },
      "additionalProperties" : False
    },
    "LocationConfiguration" : {
      "type" : "object",
      "properties" : {
        "LocationName" : {
          "type" : "string",
          "maxLength" : 20,
          "minLength" : 1,
          "pattern" : "^[a-zA-Z0-9-]+$"
        },
        "AlwaysOnCapacity" : {
          "type" : "integer",
          "minimum" : 0
        },
        "OnDemandCapacity" : {
          "type" : "integer",
          "minimum" : 0
        }
      },
      "required" : [ "LocationName" ],
      "additionalProperties" : False
    },
    "Tags" : {
      "type" : "object",
      "maxProperties" : 50,
      "minProperties" : 1,
      "patternProperties" : {
        ".+" : {
          "type" : "string",
          "maxLength" : 256,
          "minLength" : 0
        }
      },
      "additionalProperties" : False
    },
    "Unit" : {
      "type" : "object",
      "additionalProperties" : False
    },
    "StreamClass" : {
      "type" : "string",
      "maxLength" : 20,
      "minLength" : 1
    }
  },
  "properties" : {
    "Arn" : {
      "type" : "string",
      "maxLength" : 128,
      "minLength" : 1,
      "pattern" : "^(^[a-zA-Z0-9-]+$)|(^arn:aws:gameliftstreams:([^:\n]*):([0-9]{12}):([^:\n]*)$)$"
    },
    "DefaultApplication" : {
      "$ref" : "#/definitions/DefaultApplication"
    },
    "Description" : {
      "type" : "string",
      "maxLength" : 80,
      "minLength" : 1,
      "pattern" : "^[a-zA-Z0-9-_.!+@/][a-zA-Z0-9-_.!+@/ ]*$"
    },
    "Id" : {
      "type" : "string",
      "maxLength" : 32,
      "minLength" : 1,
      "pattern" : "^[a-zA-Z0-9-]+$"
    },
    "StreamClass" : {
      "$ref" : "#/definitions/StreamClass"
    },
    "Tags" : {
      "$ref" : "#/definitions/Tags"
    },
    "LocationConfigurations" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/LocationConfiguration"
      },
      "maxItems" : 100,
      "minItems" : 1,
      "uniqueItems" : True,
      "insertionOrder" : False
    }
  },
  "required" : [ "Description", "LocationConfigurations", "StreamClass" ],
  "readOnlyProperties" : [ "/properties/Arn", "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/StreamClass", "/properties/DefaultApplication/Id" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "gameliftstreams:CreateStreamGroup", "gameliftstreams:UpdateStreamGroup", "gameliftstreams:GetStreamGroup", "gameliftstreams:TagResource", "gameliftstreams:ListTagsForResource", "gameliftstreams:AssociateApplications" ]
    },
    "read" : {
      "permissions" : [ "gameliftstreams:GetStreamGroup", "gameliftstreams:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "gameliftstreams:UpdateStreamGroup", "gameliftstreams:GetStreamGroup", "gameliftstreams:AddStreamGroupLocations", "gameliftstreams:RemoveStreamGroupLocations", "gameliftstreams:TagResource", "gameliftstreams:UntagResource", "gameliftstreams:ListTagsForResource" ]
    },
    "delete" : {
      "permissions" : [ "gameliftstreams:DeleteStreamGroup", "gameliftstreams:GetStreamGroup" ]
    },
    "list" : {
      "permissions" : [ "gameliftstreams:ListStreamGroups", "gameliftstreams:ListTagsForResource" ]
    }
  },
  "additionalProperties" : False,
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "gameliftstreams:TagResource", "gameliftstreams:UntagResource", "gameliftstreams:ListTagsForResource" ]
  },
  "additionalIdentifiers" : [ [ "/properties/Id" ] ]
}