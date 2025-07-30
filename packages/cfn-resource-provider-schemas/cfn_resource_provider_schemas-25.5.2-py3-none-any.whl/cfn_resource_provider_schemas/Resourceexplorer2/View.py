SCHEMA = {
  "typeName" : "AWS::ResourceExplorer2::View",
  "description" : "Definition of AWS::ResourceExplorer2::View Resource Type",
  "definitions" : {
    "IncludedProperty" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "type" : "string",
          "maxLength" : 1011,
          "minLength" : 1
        }
      },
      "required" : [ "Name" ],
      "additionalProperties" : False
    },
    "SearchFilter" : {
      "type" : "object",
      "properties" : {
        "FilterString" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 0
        }
      },
      "required" : [ "FilterString" ],
      "additionalProperties" : False
    },
    "TagMap" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    }
  },
  "properties" : {
    "Filters" : {
      "$ref" : "#/definitions/SearchFilter"
    },
    "IncludedProperties" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/IncludedProperty"
      }
    },
    "Scope" : {
      "type" : "string"
    },
    "Tags" : {
      "$ref" : "#/definitions/TagMap"
    },
    "ViewArn" : {
      "type" : "string"
    },
    "ViewName" : {
      "type" : "string",
      "pattern" : "^[a-zA-Z0-9\\-]{1,64}$"
    }
  },
  "required" : [ "ViewName" ],
  "readOnlyProperties" : [ "/properties/ViewArn" ],
  "createOnlyProperties" : [ "/properties/Scope", "/properties/ViewName" ],
  "primaryIdentifier" : [ "/properties/ViewArn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "resource-explorer-2:CreateView", "resource-explorer-2:TagResource" ]
    },
    "read" : {
      "permissions" : [ "resource-explorer-2:GetView" ]
    },
    "update" : {
      "permissions" : [ "resource-explorer-2:UpdateView", "resource-explorer-2:TagResource", "resource-explorer-2:UntagResource", "resource-explorer-2:ListTagsForResource" ]
    },
    "delete" : {
      "permissions" : [ "resource-explorer-2:DeleteView", "resource-explorer-2:GetView", "resource-explorer-2:UntagResource" ]
    },
    "list" : {
      "permissions" : [ "resource-explorer-2:ListViews" ]
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "cloudFormationSystemTags" : False,
    "tagUpdatable" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "resource-explorer-2:ListTagsForResource", "resource-explorer-2:TagResource", "resource-explorer-2:UntagResource" ]
  },
  "additionalProperties" : False
}