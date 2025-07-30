SCHEMA = {
  "typeName" : "AWS::EC2::InstanceConnectEndpoint",
  "description" : "Resource Type definition for AWS::EC2::InstanceConnectEndpoint",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : {
    "Tag" : {
      "description" : "A key-value pair to associate with a resource.",
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    },
    "SecurityGroupId" : {
      "description" : "A key-value pair to associate with a resource.",
      "type" : "string"
    }
  },
  "properties" : {
    "Id" : {
      "description" : "The id of the instance connect endpoint",
      "type" : "string"
    },
    "SubnetId" : {
      "description" : "The subnet id of the instance connect endpoint",
      "type" : "string"
    },
    "ClientToken" : {
      "description" : "The client token of the instance connect endpoint.",
      "type" : "string"
    },
    "PreserveClientIp" : {
      "description" : "If True, the address of the instance connect endpoint client is preserved when connecting to the end resource",
      "type" : "boolean"
    },
    "Tags" : {
      "description" : "The tags of the instance connect endpoint.",
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "SecurityGroupIds" : {
      "description" : "The security group IDs of the instance connect endpoint.",
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/SecurityGroupId"
      }
    }
  },
  "additionalProperties" : False,
  "required" : [ "SubnetId" ],
  "readOnlyProperties" : [ "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/SubnetId", "/properties/ClientToken", "/properties/PreserveClientIp", "/properties/SecurityGroupIds" ],
  "writeOnlyProperties" : [ "/properties/ClientToken" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "ec2:CreateTags", "ec2:DeleteTags" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "ec2:CreateInstanceConnectEndpoint", "ec2:DescribeInstanceConnectEndpoints", "ec2:CreateTags", "ec2:CreateNetworkInterface", "iam:CreateServiceLinkedRole" ]
    },
    "read" : {
      "permissions" : [ "ec2:DescribeInstanceConnectEndpoints" ]
    },
    "update" : {
      "permissions" : [ "ec2:DescribeInstanceConnectEndpoints", "ec2:CreateTags", "ec2:DeleteTags" ]
    },
    "delete" : {
      "permissions" : [ "ec2:DeleteInstanceConnectEndpoint", "ec2:DescribeInstanceConnectEndpoints" ]
    },
    "list" : {
      "permissions" : [ "ec2:DescribeInstanceConnectEndpoints" ]
    }
  }
}