SCHEMA = {
  "typeName" : "AWS::IoT::ThingType",
  "description" : "Resource Type definition for AWS::IoT::ThingType",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "ThingTypeName" : {
      "type" : "string",
      "pattern" : "[a-zA-Z0-9:_-]+",
      "minLength" : 1,
      "maxLength" : 128
    },
    "DeprecateThingType" : {
      "type" : "boolean"
    },
    "ThingTypeProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SearchableAttributes" : {
          "type" : "array",
          "maxItems" : 3,
          "uniqueItems" : True,
          "insertionOrder" : True,
          "items" : {
            "type" : "string",
            "pattern" : "[a-zA-Z0-9_.,@/:#-]+",
            "maxLength" : 128
          }
        },
        "ThingTypeDescription" : {
          "pattern" : "[\\p{Graph}\\x20]*",
          "type" : "string",
          "maxLength" : 2028
        },
        "Mqtt5Configuration" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "PropagatingAttributes" : {
              "type" : "array",
              "uniqueItems" : True,
              "items" : {
                "$ref" : "#/definitions/PropagatingAttribute"
              }
            }
          }
        }
      }
    },
    "Tags" : {
      "description" : "An array of key-value pairs to apply to this resource.",
      "type" : "array",
      "maxItems" : 50,
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "definitions" : {
    "Tag" : {
      "description" : "A key-value pair to associate with a resource.",
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "type" : "string",
          "description" : "Tag key (1-128 chars). No 'aws:' prefix. Allows: [A-Za-z0-9 _.:/=+-]",
          "minLength" : 1,
          "maxLength" : 128,
          "pattern" : "^([\\p{L}\\p{Z}\\p{N}_.:/=+\\-@]*)$"
        },
        "Value" : {
          "type" : "string",
          "description" : "Tag value (1-256 chars). No 'aws:' prefix. Allows: [A-Za-z0-9 _.:/=+-]",
          "minLength" : 1,
          "maxLength" : 256
        }
      },
      "required" : [ "Key", "Value" ]
    },
    "PropagatingAttribute" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "UserPropertyKey" : {
          "type" : "string",
          "pattern" : "[a-zA-Z0-9:$.]+",
          "maxLength" : 128
        },
        "ThingAttribute" : {
          "type" : "string",
          "pattern" : "[a-zA-Z0-9_.,@/:#-]+",
          "maxLength" : 128
        },
        "ConnectionAttribute" : {
          "type" : "string",
          "enum" : [ "iot:ClientId", "iot:Thing.ThingName" ]
        }
      },
      "required" : [ "UserPropertyKey" ]
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "iot:ListTagsForResource", "iot:TagResource", "iot:UntagResource" ]
  },
  "readOnlyProperties" : [ "/properties/Arn", "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/ThingTypeName" ],
  "primaryIdentifier" : [ "/properties/ThingTypeName" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iot:DescribeThingType", "iot:ListTagsForResource", "iot:CreateThingType", "iot:DeprecateThingType", "iot:TagResource" ]
    },
    "delete" : {
      "permissions" : [ "iot:DescribeThingType", "iot:DeleteThingType", "iot:DeprecateThingType" ]
    },
    "list" : {
      "permissions" : [ "iot:ListThingTypes", "iot:ListTagsForResource" ]
    },
    "read" : {
      "permissions" : [ "iot:DescribeThingType", "iot:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "iot:DescribeThingType", "iot:UpdateThingType", "iot:ListTagsForResource", "iot:TagResource", "iot:UntagResource", "iot:DeprecateThingType" ]
    }
  }
}