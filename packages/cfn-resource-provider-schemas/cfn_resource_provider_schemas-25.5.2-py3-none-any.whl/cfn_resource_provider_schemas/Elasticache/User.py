SCHEMA = {
  "typeName" : "AWS::ElastiCache::User",
  "description" : "Resource Type definition for AWS::ElastiCache::User",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-elasticache",
  "definitions" : {
    "Tag" : {
      "description" : "A key-value pair to associate with a resource.",
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "description" : "The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with 'aws:'. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.",
          "type" : "string",
          "pattern" : "^(?!aws:)[a-zA-Z0-9 _\\.\\/=+:\\-@]*$",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "description" : "The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.",
          "type" : "string",
          "pattern" : "^[a-zA-Z0-9 _\\.\\/=+:\\-@]*$",
          "minLength" : 0,
          "maxLength" : 256
        }
      },
      "required" : [ "Key" ]
    }
  },
  "properties" : {
    "Status" : {
      "description" : "Indicates the user status. Can be \"active\", \"modifying\" or \"deleting\".",
      "type" : "string"
    },
    "UserId" : {
      "description" : "The ID of the user.",
      "pattern" : "[a-z][a-z0-9\\\\-]*",
      "type" : "string"
    },
    "UserName" : {
      "description" : "The username of the user.",
      "type" : "string"
    },
    "Engine" : {
      "description" : "The target cache engine for the user.",
      "type" : "string",
      "enum" : [ "redis", "valkey" ]
    },
    "AccessString" : {
      "description" : "Access permissions string used for this user account.",
      "type" : "string"
    },
    "NoPasswordRequired" : {
      "description" : "Indicates a password is not required for this user account.",
      "type" : "boolean"
    },
    "Passwords" : {
      "type" : "array",
      "$comment" : "List of passwords.",
      "uniqueItems" : True,
      "insertionOrder" : True,
      "items" : {
        "type" : "string"
      },
      "description" : "Passwords used for this user account. You can create up to two passwords for each user."
    },
    "Arn" : {
      "description" : "The Amazon Resource Name (ARN) of the user account.",
      "type" : "string"
    },
    "AuthenticationMode" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "description" : "Authentication Type",
          "type" : "string",
          "enum" : [ "password", "no-password-required", "iam" ]
        },
        "Passwords" : {
          "type" : "array",
          "$comment" : "List of passwords.",
          "uniqueItems" : True,
          "insertionOrder" : True,
          "items" : {
            "type" : "string"
          },
          "description" : "Passwords used for this user account. You can create up to two passwords for each user."
        }
      },
      "required" : [ "Type" ]
    },
    "Tags" : {
      "description" : "An array of key-value pairs to apply to this user.",
      "type" : "array",
      "maxItems" : 50,
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
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags"
  },
  "additionalProperties" : False,
  "required" : [ "UserId", "UserName", "Engine" ],
  "readOnlyProperties" : [ "/properties/Status", "/properties/Arn" ],
  "createOnlyProperties" : [ "/properties/UserId", "/properties/UserName" ],
  "writeOnlyProperties" : [ "/properties/Passwords", "/properties/NoPasswordRequired", "/properties/AccessString", "/properties/AuthenticationMode" ],
  "primaryIdentifier" : [ "/properties/UserId" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "elasticache:CreateUser", "elasticache:DescribeUsers", "elasticache:ListTagsForResource", "elasticache:AddTagsToResource" ]
    },
    "read" : {
      "permissions" : [ "elasticache:DescribeUsers", "elasticache:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "elasticache:ModifyUser", "elasticache:DescribeUsers", "elasticache:ListTagsForResource", "elasticache:AddTagsToResource", "elasticache:RemoveTagsFromResource" ]
    },
    "delete" : {
      "permissions" : [ "elasticache:DeleteUser", "elasticache:DescribeUsers" ]
    },
    "list" : {
      "permissions" : [ "elasticache:DescribeUsers", "elasticache:ListTagsForResource" ]
    }
  }
}