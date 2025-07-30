SCHEMA = {
  "typeName" : "AWS::MSK::ServerlessCluster",
  "description" : "Resource Type definition for AWS::MSK::ServerlessCluster",
  "additionalProperties" : False,
  "properties" : {
    "Arn" : {
      "type" : "string"
    },
    "ClusterName" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 64
    },
    "VpcConfigs" : {
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/VpcConfig"
      }
    },
    "ClientAuthentication" : {
      "$ref" : "#/definitions/ClientAuthentication"
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
    }
  },
  "definitions" : {
    "VpcConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecurityGroups" : {
          "type" : "array",
          "uniqueItems" : True,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        },
        "SubnetIds" : {
          "type" : "array",
          "uniqueItems" : True,
          "insertionOrder" : False,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "SubnetIds" ]
    },
    "ClientAuthentication" : {
      "type" : "object",
      "properties" : {
        "Sasl" : {
          "$ref" : "#/definitions/Sasl"
        }
      },
      "additionalProperties" : False,
      "required" : [ "Sasl" ]
    },
    "Sasl" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Iam" : {
          "$ref" : "#/definitions/Iam"
        }
      },
      "required" : [ "Iam" ]
    },
    "Iam" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ]
    }
  },
  "required" : [ "ClusterName", "VpcConfigs", "ClientAuthentication" ],
  "createOnlyProperties" : [ "/properties/ClusterName", "/properties/VpcConfigs", "/properties/ClientAuthentication", "/properties/Tags" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "readOnlyProperties" : [ "/properties/Arn" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "kafka:TagResource", "kafka:UntagResource", "kafka:ListTagsForResource" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "kafka:CreateClusterV2", "kafka:TagResource", "kafka:DescribeClusterV2", "ec2:CreateVpcEndpoint", "ec2:CreateTags", "ec2:DescribeVpcAttribute", "ec2:DescribeSubnets", "ec2:DescribeVpcEndpoints", "ec2:DescribeVpcs", "ec2:DescribeSecurityGroups" ],
      "timeoutInMinutes" : 120
    },
    "read" : {
      "permissions" : [ "kafka:DescribeClusterV2" ]
    },
    "delete" : {
      "permissions" : [ "kafka:DeleteCluster", "kafka:DescribeClusterV2", "ec2:DeleteVpcEndpoints" ],
      "timeoutInMinutes" : 75
    },
    "list" : {
      "permissions" : [ "kafka:ListClustersV2" ]
    }
  }
}