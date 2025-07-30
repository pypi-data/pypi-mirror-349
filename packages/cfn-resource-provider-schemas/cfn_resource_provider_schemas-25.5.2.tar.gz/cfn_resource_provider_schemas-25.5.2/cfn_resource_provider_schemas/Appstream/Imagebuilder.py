SCHEMA = {
  "typeName" : "AWS::AppStream::ImageBuilder",
  "description" : "Resource Type definition for AWS::AppStream::ImageBuilder",
  "additionalProperties" : False,
  "properties" : {
    "Description" : {
      "type" : "string"
    },
    "VpcConfig" : {
      "$ref" : "#/definitions/VpcConfig"
    },
    "EnableDefaultInternetAccess" : {
      "type" : "boolean"
    },
    "DomainJoinInfo" : {
      "$ref" : "#/definitions/DomainJoinInfo"
    },
    "AppstreamAgentVersion" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    },
    "ImageName" : {
      "type" : "string"
    },
    "DisplayName" : {
      "type" : "string"
    },
    "IamRoleArn" : {
      "type" : "string"
    },
    "InstanceType" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "StreamingUrl" : {
      "type" : "string"
    },
    "ImageArn" : {
      "type" : "string"
    },
    "AccessEndpoints" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/AccessEndpoint"
      }
    }
  },
  "definitions" : {
    "VpcConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecurityGroupIds" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "SubnetIds" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "DomainJoinInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OrganizationalUnitDistinguishedName" : {
          "type" : "string"
        },
        "DirectoryName" : {
          "type" : "string"
        }
      }
    },
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    },
    "AccessEndpoint" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "EndpointType" : {
          "type" : "string"
        },
        "VpceId" : {
          "type" : "string"
        }
      },
      "required" : [ "EndpointType", "VpceId" ]
    }
  },
  "required" : [ "InstanceType", "Name" ],
  "primaryIdentifier" : [ "/properties/Name" ],
  "readOnlyProperties" : [ "/properties/StreamingUrl" ],
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : True,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags"
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "appstream:CreateImageBuilder", "appstream:CreateImageBuilderStreamingURL", "appstream:CreateStreamingURL", "appstream:DeleteImageBuilder", "appstream:DescribeImageBuilders", "appstream:StartImageBuilder", "appstream:StopImageBuilder", "iam:CreateServiceLinkedRole", "iam:DeleteServiceLinkedRole", "iam:GetServiceLinkedRoleDeletionStatus" ]
    },
    "read" : {
      "permissions" : [ "appstream:CreateImageBuilder", "appstream:CreateImageBuilderStreamingURL", "appstream:CreateStreamingURL", "appstream:DeleteImageBuilder", "appstream:DescribeImageBuilders", "appstream:StartImageBuilder", "appstream:StopImageBuilder", "iam:CreateServiceLinkedRole", "iam:DeleteServiceLinkedRole", "iam:GetServiceLinkedRoleDeletionStatus" ]
    },
    "delete" : {
      "permissions" : [ "appstream:CreateImageBuilder", "appstream:CreateImageBuilderStreamingURL", "appstream:CreateStreamingURL", "appstream:DeleteImageBuilder", "appstream:DescribeImageBuilders", "appstream:StartImageBuilder", "appstream:StopImageBuilder", "iam:CreateServiceLinkedRole", "iam:DeleteServiceLinkedRole", "iam:GetServiceLinkedRoleDeletionStatus" ]
    },
    "list" : {
      "permissions" : [ "appstream:CreateImageBuilder", "appstream:CreateImageBuilderStreamingURL", "appstream:CreateStreamingURL", "appstream:DeleteImageBuilder", "appstream:DescribeImageBuilders", "appstream:StartImageBuilder", "appstream:StopImageBuilder", "iam:CreateServiceLinkedRole", "iam:DeleteServiceLinkedRole", "iam:GetServiceLinkedRoleDeletionStatus" ]
    }
  }
}