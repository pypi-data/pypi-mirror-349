SCHEMA = {
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-transitgateway",
  "tagging" : {
    "permissions" : [ "ec2:CreateTags", "ec2:DeleteTags" ],
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "tagProperty" : "/properties/Tags",
    "cloudFormationSystemTags" : False
  },
  "handlers" : {
    "read" : {
      "permissions" : [ "ec2:DescribeTransitGatewayVpcAttachments", "ec2:DescribeTags" ]
    },
    "create" : {
      "permissions" : [ "ec2:DescribeTransitGatewayVpcAttachments", "ec2:CreateTransitGatewayVpcAttachment", "ec2:CreateTags", "ec2:DescribeTags" ]
    },
    "update" : {
      "permissions" : [ "ec2:DescribeTransitGatewayVpcAttachments", "ec2:DescribeTags", "ec2:CreateTransitGatewayVpcAttachment", "ec2:CreateTags", "ec2:DeleteTransitGatewayVpcAttachment", "ec2:DeleteTags", "ec2:ModifyTransitGatewayVpcAttachment" ]
    },
    "list" : {
      "permissions" : [ "ec2:DescribeTransitGatewayVpcAttachments", "ec2:DescribeTags" ]
    },
    "delete" : {
      "permissions" : [ "ec2:DescribeTransitGatewayVpcAttachments", "ec2:DeleteTransitGatewayVpcAttachment", "ec2:DeleteTags", "ec2:DescribeTags" ]
    }
  },
  "typeName" : "AWS::EC2::TransitGatewayAttachment",
  "readOnlyProperties" : [ "/properties/Id" ],
  "description" : "Resource Type definition for AWS::EC2::TransitGatewayAttachment",
  "createOnlyProperties" : [ "/properties/TransitGatewayId", "/properties/VpcId" ],
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/Id" ],
  "definitions" : {
    "Tag" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    }
  },
  "properties" : {
    "Options" : {
      "description" : "The options for the transit gateway vpc attachment.",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Ipv6Support" : {
          "description" : "Indicates whether to enable Ipv6 Support for Vpc Attachment. Valid Values: enable | disable",
          "type" : "string"
        },
        "ApplianceModeSupport" : {
          "description" : "Indicates whether to enable Ipv6 Support for Vpc Attachment. Valid Values: enable | disable",
          "type" : "string"
        },
        "SecurityGroupReferencingSupport" : {
          "description" : "Indicates whether to enable Security Group referencing support for Vpc Attachment. Valid Values: enable | disable",
          "type" : "string"
        },
        "DnsSupport" : {
          "description" : "Indicates whether to enable DNS Support for Vpc Attachment. Valid Values: enable | disable",
          "type" : "string"
        }
      }
    },
    "TransitGatewayId" : {
      "type" : "string"
    },
    "VpcId" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "SubnetIds" : {
      "uniqueItems" : False,
      "insertionOrder" : False,
      "type" : "array",
      "items" : {
        "relationshipRef" : {
          "typeName" : "AWS::EC2::Subnet",
          "propertyPath" : "/properties/SubnetId"
        },
        "type" : "string"
      }
    },
    "Tags" : {
      "uniqueItems" : False,
      "insertionOrder" : False,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "required" : [ "VpcId", "SubnetIds", "TransitGatewayId" ]
}