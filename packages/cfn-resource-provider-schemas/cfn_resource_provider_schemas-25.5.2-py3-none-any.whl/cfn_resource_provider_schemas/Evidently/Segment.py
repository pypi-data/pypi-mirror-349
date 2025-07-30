SCHEMA = {
  "typeName" : "AWS::Evidently::Segment",
  "description" : "Resource Type definition for AWS::Evidently::Segment",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-evidently",
  "definitions" : {
    "Tag" : {
      "description" : "A key-value pair to associate with a resource.",
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "pattern" : "^(?!aws:)[a-zA-Z+-=._:/]+$",
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
    "Arn" : {
      "type" : "string",
      "pattern" : "arn:[^:]*:[^:]*:[^:]*:[^:]*:segment/[-a-zA-Z0-9._]*",
      "minLength" : 0,
      "maxLength" : 2048
    },
    "Name" : {
      "type" : "string",
      "pattern" : "[-a-zA-Z0-9._]*",
      "minLength" : 1,
      "maxLength" : 127
    },
    "Description" : {
      "type" : "string",
      "minLength" : 0,
      "maxLength" : 160
    },
    "Pattern" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 1024
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
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags"
  },
  "additionalProperties" : False,
  "required" : [ "Name" ],
  "readOnlyProperties" : [ "/properties/Arn" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "evidently:CreateSegment", "evidently:GetSegment", "evidently:TagResource" ]
    },
    "read" : {
      "permissions" : [ "evidently:GetSegment", "evidently:ListTagsForResource" ]
    },
    "delete" : {
      "permissions" : [ "evidently:DeleteSegment", "evidently:GetSegment", "evidently:UntagResource" ]
    },
    "list" : {
      "permissions" : [ "evidently:ListSegment", "evidently:ListTagsForResource" ]
    }
  }
}