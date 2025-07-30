SCHEMA = {
  "typeName" : "AWS::MemoryDB::SubnetGroup",
  "description" : "The AWS::MemoryDB::SubnetGroup resource creates an Amazon MemoryDB Subnet Group.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-memorydb",
  "definitions" : {
    "Tag" : {
      "description" : "A key-value pair to associate with a resource.",
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "description" : "The key for the tag. May not be None.",
          "pattern" : "^(?!aws:)(?!memorydb:)[a-zA-Z0-9 _\\.\\/=+:\\-@]{1,128}$",
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "description" : "The tag's value. May be None.",
          "type" : "string",
          "pattern" : "^(?!aws:)(?!memorydb:)[a-zA-Z0-9 _\\.\\/=+:\\-@]{1,256}$",
          "minLength" : 1,
          "maxLength" : 256
        }
      },
      "required" : [ "Key", "Value" ]
    }
  },
  "properties" : {
    "SubnetGroupName" : {
      "description" : "The name of the subnet group. This value must be unique as it also serves as the subnet group identifier.",
      "pattern" : "[a-z][a-z0-9\\-]*",
      "type" : "string"
    },
    "Description" : {
      "description" : "An optional description of the subnet group.",
      "type" : "string"
    },
    "SubnetIds" : {
      "description" : "A list of VPC subnet IDs for the subnet group.",
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Tags" : {
      "description" : "An array of key-value pairs to apply to this subnet group.",
      "type" : "array",
      "maxItems" : 50,
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "ARN" : {
      "description" : "The Amazon Resource Name (ARN) of the subnet group.",
      "type" : "string"
    },
    "SupportedNetworkTypes" : {
      "description" : "Supported network types would be a list of network types supported by subnet group and can be either [ipv4] or [ipv4, dual_stack] or [ipv6].",
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "type" : "string"
      }
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "memorydb:TagResource", "memorydb:ListTags", "memorydb:UntagResource" ]
  },
  "additionalProperties" : False,
  "required" : [ "SubnetGroupName", "SubnetIds" ],
  "primaryIdentifier" : [ "/properties/SubnetGroupName" ],
  "createOnlyProperties" : [ "/properties/SubnetGroupName" ],
  "readOnlyProperties" : [ "/properties/ARN", "/properties/SupportedNetworkTypes" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "memorydb:CreateSubnetGroup", "memorydb:DescribeSubnetGroups", "memorydb:TagResource", "memorydb:ListTags", "iam:CreateServiceLinkedRole" ]
    },
    "read" : {
      "permissions" : [ "memorydb:DescribeSubnetGroups", "memorydb:ListTags" ]
    },
    "update" : {
      "permissions" : [ "memorydb:UpdateSubnetGroup", "memorydb:DescribeSubnetGroups", "memorydb:ListTags", "memorydb:TagResource", "memorydb:UntagResource" ]
    },
    "delete" : {
      "permissions" : [ "memorydb:DeleteSubnetGroup", "memorydb:DescribeSubnetGroups" ]
    },
    "list" : {
      "permissions" : [ "memorydb:DescribeSubnetGroups" ]
    }
  }
}