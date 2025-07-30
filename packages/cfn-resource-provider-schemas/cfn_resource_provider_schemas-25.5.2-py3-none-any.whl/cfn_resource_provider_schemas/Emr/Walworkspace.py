SCHEMA = {
  "typeName" : "AWS::EMR::WALWorkspace",
  "description" : "Resource schema for AWS::EMR::WALWorkspace Type",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-emrwal",
  "definitions" : {
    "Tag" : {
      "description" : "A key-value pair to associate with a resource.",
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "description" : "The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "type" : "string",
          "description" : "The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.",
          "minLength" : 0,
          "maxLength" : 256
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    }
  },
  "properties" : {
    "WALWorkspaceName" : {
      "description" : "The name of the emrwal container",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 32,
      "pattern" : "^[a-zA-Z0-9]+$"
    },
    "Tags" : {
      "description" : "An array of key-value pairs to apply to this resource.",
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "additionalProperties" : False,
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "emrwal:TagResource", "emrwal:UntagResource", "emrwal:ListTagsForResource" ]
  },
  "primaryIdentifier" : [ "/properties/WALWorkspaceName" ],
  "createOnlyProperties" : [ "/properties/WALWorkspaceName" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "emrwal:CreateWorkspace", "emrwal:TagResource", "iam:CreateServiceLinkedRole" ]
    },
    "read" : {
      "permissions" : [ "emrwal:ListTagsForResource" ]
    },
    "delete" : {
      "permissions" : [ "emrwal:DeleteWorkspace" ]
    },
    "list" : {
      "permissions" : [ "emrwal:ListWorkspaces" ]
    },
    "update" : {
      "permissions" : [ "emrwal:TagResource", "emrwal:UntagResource", "emrwal:ListTagsForResource" ]
    }
  }
}