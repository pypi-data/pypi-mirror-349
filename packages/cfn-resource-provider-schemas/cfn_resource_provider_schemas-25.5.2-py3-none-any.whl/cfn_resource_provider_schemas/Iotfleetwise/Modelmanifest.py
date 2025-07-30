SCHEMA = {
  "typeName" : "AWS::IoTFleetWise::ModelManifest",
  "description" : "Definition of AWS::IoTFleetWise::ModelManifest Resource Type",
  "definitions" : {
    "ManifestStatus" : {
      "type" : "string",
      "enum" : [ "ACTIVE", "DRAFT" ],
      "default" : "DRAFT"
    },
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "maxLength" : 128,
          "minLength" : 1
        },
        "Value" : {
          "type" : "string",
          "maxLength" : 256,
          "minLength" : 0
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    }
  },
  "properties" : {
    "Arn" : {
      "type" : "string"
    },
    "CreationTime" : {
      "type" : "string",
      "format" : "date-time"
    },
    "Description" : {
      "type" : "string",
      "maxLength" : 2048,
      "minLength" : 1,
      "pattern" : "^[^\\u0000-\\u001F\\u007F]+$"
    },
    "LastModificationTime" : {
      "type" : "string",
      "format" : "date-time"
    },
    "Name" : {
      "type" : "string",
      "maxLength" : 100,
      "minLength" : 1,
      "pattern" : "^[a-zA-Z\\d\\-_:]+$"
    },
    "Nodes" : {
      "insertionOrder" : False,
      "uniqueItems" : True,
      "minItems" : 1,
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "SignalCatalogArn" : {
      "type" : "string"
    },
    "Status" : {
      "$ref" : "#/definitions/ManifestStatus"
    },
    "Tags" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "insertionOrder" : False,
      "uniqueItems" : True,
      "maxItems" : 50,
      "minItems" : 0
    }
  },
  "required" : [ "SignalCatalogArn", "Name" ],
  "readOnlyProperties" : [ "/properties/Arn", "/properties/CreationTime", "/properties/LastModificationTime" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Name" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iotfleetwise:CreateModelManifest", "iotfleetwise:GetModelManifest", "iotfleetwise:UpdateModelManifest", "iotfleetwise:ListModelManifestNodes", "iotfleetwise:ListTagsForResource", "iotfleetwise:TagResource" ]
    },
    "read" : {
      "permissions" : [ "iotfleetwise:GetModelManifest", "iotfleetwise:ListModelManifestNodes", "iotfleetwise:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "iotfleetwise:UpdateModelManifest", "iotfleetwise:GetModelManifest", "iotfleetwise:ListModelManifestNodes", "iotfleetwise:ListTagsForResource", "iotfleetwise:TagResource", "iotfleetwise:UntagResource" ]
    },
    "delete" : {
      "permissions" : [ "iotfleetwise:DeleteModelManifest", "iotfleetwise:GetModelManifest" ]
    },
    "list" : {
      "permissions" : [ "iotfleetwise:ListModelManifests" ]
    }
  },
  "additionalProperties" : False,
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "iotfleetwise:UntagResource", "iotfleetwise:TagResource", "iotfleetwise:ListTagsForResource" ]
  }
}