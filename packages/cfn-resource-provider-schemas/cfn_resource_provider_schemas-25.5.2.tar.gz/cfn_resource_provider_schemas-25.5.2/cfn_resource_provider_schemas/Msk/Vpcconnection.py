SCHEMA = {
  "typeName" : "AWS::MSK::VpcConnection",
  "description" : "Resource Type definition for AWS::MSK::VpcConnection",
  "definitions" : {
    "Authentication" : {
      "type" : "string",
      "description" : "The type of private link authentication",
      "minLength" : 3,
      "maxLength" : 10,
      "enum" : [ "SASL_IAM", "SASL_SCRAM", "TLS" ]
    },
    "ClientSubnets" : {
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "type" : "string",
        "pattern" : "^(subnet-)([a-z0-9]+)\\Z"
      }
    },
    "SecurityGroups" : {
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "type" : "string",
        "pattern" : "^(sg-)([a-z0-9]+)\\Z"
      }
    },
    "Tags" : {
      "type" : "object",
      "description" : "A key-value pair to associate with a resource.",
      "patternProperties" : {
        "^([\\p{L}\\p{Z}\\p{N}_.:/=+\\-@]*)$" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "VpcId" : {
      "type" : "string",
      "pattern" : "^(vpc-)([a-z0-9]+)\\Z"
    }
  },
  "properties" : {
    "Arn" : {
      "type" : "string"
    },
    "Authentication" : {
      "$ref" : "#/definitions/Authentication"
    },
    "ClientSubnets" : {
      "$ref" : "#/definitions/ClientSubnets"
    },
    "TargetClusterArn" : {
      "description" : "The Amazon Resource Name (ARN) of the target cluster",
      "type" : "string",
      "pattern" : "^arn:[\\w-]+:kafka:[\\w-]+:\\d+:cluster.*\\Z"
    },
    "SecurityGroups" : {
      "$ref" : "#/definitions/SecurityGroups"
    },
    "Tags" : {
      "$ref" : "#/definitions/Tags"
    },
    "VpcId" : {
      "$ref" : "#/definitions/VpcId"
    }
  },
  "additionalProperties" : False,
  "required" : [ "Authentication", "ClientSubnets", "SecurityGroups", "TargetClusterArn", "VpcId" ],
  "createOnlyProperties" : [ "/properties/ClientSubnets", "/properties/Authentication", "/properties/SecurityGroups", "/properties/TargetClusterArn", "/properties/VpcId" ],
  "readOnlyProperties" : [ "/properties/Arn" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "kafka:TagResource", "kafka:UntagResource", "kafka:ListTagsForResource" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "ec2:CreateVpcEndpoint", "ec2:DescribeSecurityGroups", "ec2:DescribeSubnets", "ec2:DescribeVpcAttribute", "ec2:DescribeVpcs", "ec2:DescribeVpcEndpoints", "ec2:AcceptVpcEndpointConnections", "ec2:RejectVpcEndpointConnections", "ec2:DescribeVpcEndpointConnections", "ec2:CreateTags", "iam:AttachRolePolicy", "iam:CreateServiceLinkedRole", "iam:PutRolePolicy", "kafka:CreateVpcConnection", "kafka:DescribeVpcConnection", "kafka:TagResource", "kms:CreateGrant", "kms:DescribeKey" ]
    },
    "read" : {
      "permissions" : [ "kafka:DescribeVpcConnection", "kms:CreateGrant", "kms:DescribeKey" ]
    },
    "update" : {
      "permissions" : [ "kafka:DescribeVpcConnection", "kms:CreateGrant", "kms:DescribeKey", "kafka:TagResource", "kafka:UntagResource" ]
    },
    "delete" : {
      "permissions" : [ "ec2:DeleteVpcEndpoint", "ec2:DeleteVpcEndpoints", "ec2:DescribeVpcEndpoints", "ec2:DescribeVpcEndpointConnections", "kafka:DeleteVpcConnection", "kafka:DescribeVpcConnection", "kms:CreateGrant", "kms:DescribeKey" ]
    },
    "list" : {
      "permissions" : [ "kafka:ListVpcConnections", "kms:CreateGrant", "kms:DescribeKey" ]
    }
  }
}