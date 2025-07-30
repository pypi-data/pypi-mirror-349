SCHEMA = {
  "typeName" : "AWS::AppStream::AppBlockBuilder",
  "description" : "Resource Type definition for AWS::AppStream::AppBlockBuilder.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-appstream.git",
  "definitions" : {
    "PlatformType" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "AccessEndpoint" : {
      "type" : "object",
      "properties" : {
        "EndpointType" : {
          "type" : "string"
        },
        "VpceId" : {
          "type" : "string"
        }
      },
      "required" : [ "EndpointType", "VpceId" ],
      "additionalProperties" : False
    },
    "Tag" : {
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
    "VpcConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecurityGroupIds" : {
          "type" : "array",
          "insertionOrder" : False,
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "SubnetIds" : {
          "type" : "array",
          "insertionOrder" : False,
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    }
  },
  "properties" : {
    "Name" : {
      "type" : "string"
    },
    "Arn" : {
      "$ref" : "#/definitions/Arn"
    },
    "Description" : {
      "type" : "string"
    },
    "DisplayName" : {
      "type" : "string"
    },
    "Platform" : {
      "$ref" : "#/definitions/PlatformType"
    },
    "AccessEndpoints" : {
      "type" : "array",
      "insertionOrder" : False,
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/AccessEndpoint"
      }
    },
    "Tags" : {
      "type" : "array",
      "insertionOrder" : False,
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "VpcConfig" : {
      "$ref" : "#/definitions/VpcConfig"
    },
    "EnableDefaultInternetAccess" : {
      "type" : "boolean"
    },
    "IamRoleArn" : {
      "type" : "string"
    },
    "CreatedTime" : {
      "type" : "string"
    },
    "InstanceType" : {
      "type" : "string"
    },
    "AppBlockArns" : {
      "type" : "array",
      "insertionOrder" : False,
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Arn"
      }
    }
  },
  "additionalProperties" : False,
  "required" : [ "Name", "Platform", "InstanceType", "VpcConfig" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "readOnlyProperties" : [ "/properties/Arn", "/properties/CreatedTime" ],
  "writeOnlyProperties" : [ "/properties/Tags", "/properties/AppBlockArns" ],
  "primaryIdentifier" : [ "/properties/Name" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags"
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "appstream:CreateAppBlockBuilder", "appstream:DescribeAppBlockBuilders", "appstream:StartAppBlockBuilder", "appstream:AssociateAppBlockBuilderAppBlock", "appstream:DescribeAppBlockBuilderAppBlockAssociations", "appstream:TagResource", "iam:PassRole" ]
    },
    "read" : {
      "permissions" : [ "appstream:DescribeAppBlockBuilders" ]
    },
    "update" : {
      "permissions" : [ "appstream:UpdateAppBlockBuilder", "appstream:DescribeAppBlockBuilders", "appstream:StartAppBlockBuilder", "appstream:StopAppBlockBuilder", "appstream:AssociateAppBlockBuilderAppBlock", "appstream:DisassociateAppBlockBuilderAppBlock", "appstream:DescribeAppBlockBuilderAppBlockAssociations", "appstream:ListTagsForResource", "appstream:TagResource", "appstream:UntagResource", "iam:PassRole" ]
    },
    "delete" : {
      "permissions" : [ "appstream:DescribeAppBlockBuilders", "appstream:DeleteAppBlockBuilder", "appstream:DisassociateAppBlockBuilderAppBlock", "appstream:DescribeAppBlockBuilderAppBlockAssociations" ]
    },
    "list" : {
      "permissions" : [ "appstream:DescribeAppBlockBuilders" ]
    }
  }
}