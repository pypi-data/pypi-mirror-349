SCHEMA = {
  "typeName" : "AWS::Glue::UsageProfile",
  "description" : "This creates a Resource of UsageProfile type.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-glue",
  "definitions" : {
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "description" : "A key to identify the tag.",
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "description" : "Corresponding tag value for the key.",
          "type" : "string",
          "minLength" : 0,
          "maxLength" : 256
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    },
    "ProfileConfiguration" : {
      "properties" : {
        "JobConfiguration" : {
          "patternProperties" : {
            "^.+$" : {
              "$ref" : "#/definitions/ConfigurationObject"
            }
          },
          "additionalProperties" : False
        },
        "SessionConfiguration" : {
          "patternProperties" : {
            "^.+$" : {
              "$ref" : "#/definitions/ConfigurationObject"
            }
          },
          "additionalProperties" : False
        }
      },
      "anyOf" : [ {
        "required" : [ "JobConfiguration" ]
      }, {
        "required" : [ "SessionConfiguration" ]
      } ],
      "additionalProperties" : False
    },
    "ConfigurationObject" : {
      "properties" : {
        "DefaultValue" : {
          "type" : "string"
        },
        "AllowedValues" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          },
          "insertionOrder" : False
        },
        "MinValue" : {
          "type" : "string"
        },
        "MaxValue" : {
          "type" : "string"
        }
      },
      "anyOf" : [ {
        "required" : [ "DefaultValue" ]
      }, {
        "oneOf" : [ {
          "required" : [ "AllowedValues" ]
        }, {
          "required" : [ "MinValue", "MaxValue" ]
        } ]
      } ],
      "additionalProperties" : False
    }
  },
  "properties" : {
    "Name" : {
      "description" : "The name of the UsageProfile.",
      "type" : "string",
      "maxLength" : 128,
      "minLength" : 5
    },
    "Description" : {
      "description" : "The description of the UsageProfile.",
      "type" : "string",
      "maxLength" : 512,
      "minLength" : 1,
      "pattern" : "[a-zA-Z0-9\\-\\:\\_]{1,64}"
    },
    "Configuration" : {
      "description" : "UsageProfile configuration for supported service ex: (Jobs, Sessions).",
      "$ref" : "#/definitions/ProfileConfiguration",
      "minItems" : 1
    },
    "Tags" : {
      "description" : "The tags to be applied to this UsageProfiles.",
      "type" : "array",
      "minItems" : 0,
      "maxItems" : 50,
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "uniqueItems" : True,
      "insertionOrder" : False
    },
    "CreatedOn" : {
      "description" : "Creation time.",
      "type" : "string",
      "maxLength" : 128,
      "minLength" : 1
    }
  },
  "additionalProperties" : False,
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "glue:TagResource", "glue:UntagResource", "glue:GetTags" ]
  },
  "required" : [ "Name" ],
  "readOnlyProperties" : [ "/properties/CreatedOn" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Name" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "glue:CreateUsageProfile", "glue:GetUsageProfile", "glue:GetTags", "glue:TagResource" ]
    },
    "read" : {
      "permissions" : [ "glue:GetUsageProfile", "glue:GetTags" ]
    },
    "update" : {
      "permissions" : [ "glue:UpdateUsageProfile", "glue:GetUsageProfile", "glue:TagResource", "glue:UntagResource", "glue:GetTags" ]
    },
    "delete" : {
      "permissions" : [ "glue:DeleteUsageProfile", "glue:GetUsageProfile" ]
    },
    "list" : {
      "permissions" : [ "glue:ListUsageProfiles" ]
    }
  }
}