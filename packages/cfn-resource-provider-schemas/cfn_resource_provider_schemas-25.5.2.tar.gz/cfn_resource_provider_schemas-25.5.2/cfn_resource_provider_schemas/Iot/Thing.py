SCHEMA = {
  "typeName" : "AWS::IoT::Thing",
  "description" : "Resource Type definition for AWS::IoT::Thing",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "AttributePayload" : {
      "$ref" : "#/definitions/AttributePayload"
    },
    "ThingName" : {
      "type" : "string",
      "pattern" : "[a-zA-Z0-9:_-]+",
      "minLength" : 1,
      "maxLength" : 128
    }
  },
  "definitions" : {
    "AttributePayload" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Attributes" : {
          "type" : "object",
          "additionalProperties" : False,
          "patternProperties" : {
            "[a-zA-Z0-9_.,@/:#-]+" : {
              "type" : "string"
            }
          }
        }
      }
    }
  },
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : True
  },
  "createOnlyProperties" : [ "/properties/ThingName" ],
  "primaryIdentifier" : [ "/properties/ThingName" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Arn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iot:CreateThing", "iot:DescribeThing" ]
    },
    "delete" : {
      "permissions" : [ "iot:DeleteThing", "iot:DescribeThing" ]
    },
    "list" : {
      "permissions" : [ "iot:ListThings" ]
    },
    "read" : {
      "permissions" : [ "iot:DescribeThing" ]
    },
    "update" : {
      "permissions" : [ "iot:UpdateThing", "iot:DescribeThing" ]
    }
  }
}