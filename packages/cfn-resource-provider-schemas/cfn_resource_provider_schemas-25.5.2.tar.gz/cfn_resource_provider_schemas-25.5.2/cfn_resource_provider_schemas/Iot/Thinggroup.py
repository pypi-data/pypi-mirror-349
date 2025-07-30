SCHEMA = {
  "typeName" : "AWS::IoT::ThingGroup",
  "description" : "Resource Type definition for AWS::IoT::ThingGroup",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "ThingGroupName" : {
      "type" : "string",
      "pattern" : "[a-zA-Z0-9:_-]+",
      "minLength" : 1,
      "maxLength" : 128
    },
    "ParentGroupName" : {
      "type" : "string",
      "pattern" : "[a-zA-Z0-9:_-]+",
      "minLength" : 1,
      "maxLength" : 128
    },
    "QueryString" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 1000
    },
    "ThingGroupProperties" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AttributePayload" : {
          "$ref" : "#/definitions/AttributePayload"
        },
        "ThingGroupDescription" : {
          "type" : "string",
          "pattern" : "[\\p{Graph}\\x20]*",
          "maxLength" : 2028
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
    "AttributePayload" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Attributes" : {
          "type" : "object",
          "patternProperties" : {
            "[a-zA-Z0-9_.,@/:#-]+" : {
              "type" : "string"
            }
          },
          "additionalProperties" : False
        }
      }
    },
    "Tag" : {
      "description" : "A key-value pair to associate with a resource.",
      "type" : "object",
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
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
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
  "createOnlyProperties" : [ "/properties/ThingGroupName", "/properties/ParentGroupName" ],
  "primaryIdentifier" : [ "/properties/ThingGroupName" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iot:DescribeThingGroup", "iot:ListTagsForResource", "iot:CreateThingGroup", "iot:CreateDynamicThingGroup", "iot:TagResource" ]
    },
    "delete" : {
      "permissions" : [ "iot:DescribeThingGroup", "iot:DeleteThingGroup", "iot:DeleteDynamicThingGroup" ]
    },
    "list" : {
      "permissions" : [ "iot:ListThingGroups", "iot:ListTagsForResource" ]
    },
    "read" : {
      "permissions" : [ "iot:DescribeThingGroup", "iot:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "iot:ListTagsForResource", "iot:DescribeThingGroup", "iot:UpdateThingGroup", "iot:UpdateDynamicThingGroup", "iot:TagResource", "iot:UntagResource" ]
    }
  }
}