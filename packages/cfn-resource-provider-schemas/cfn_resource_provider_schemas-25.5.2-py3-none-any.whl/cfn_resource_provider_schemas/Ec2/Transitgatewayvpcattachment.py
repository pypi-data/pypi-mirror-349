SCHEMA = {
  "typeName" : "AWS::EC2::TransitGatewayVpcAttachment",
  "description" : "Resource Type definition for AWS::EC2::TransitGatewayVpcAttachment",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-transitgateway",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "TransitGatewayId" : {
      "type" : "string"
    },
    "VpcId" : {
      "type" : "string"
    },
    "SubnetIds" : {
      "type" : "array",
      "insertionOrder" : False,
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "AddSubnetIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "type" : "string"
      }
    },
    "RemoveSubnetIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "Options" : {
      "description" : "The options for the transit gateway vpc attachment.",
      "type" : "object",
      "properties" : {
        "DnsSupport" : {
          "description" : "Indicates whether to enable DNS Support for Vpc Attachment. Valid Values: enable | disable",
          "type" : "string"
        },
        "Ipv6Support" : {
          "description" : "Indicates whether to enable Ipv6 Support for Vpc Attachment. Valid Values: enable | disable",
          "type" : "string"
        },
        "ApplianceModeSupport" : {
          "description" : "Indicates whether to enable Ipv6 Support for Vpc Attachment. Valid Values: enable | disable",
          "type" : "string"
        },
        "SecurityGroupReferencingSupport" : {
          "description" : "Indicates whether to enable Security Group referencing support for Vpc Attachment. Valid values: enable | disable",
          "type" : "string"
        }
      },
      "additionalProperties" : False
    }
  },
  "definitions" : {
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "type" : "string"
        },
        "Value" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    }
  },
  "createOnlyProperties" : [ "/properties/TransitGatewayId", "/properties/SubnetIds", "/properties/VpcId" ],
  "required" : [ "SubnetIds", "VpcId", "TransitGatewayId" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "ec2:CreateTags", "ec2:DeleteTags" ]
  },
  "readOnlyProperties" : [ "/properties/Id" ],
  "writeOnlyProperties" : [ "/properties/AddSubnetIds", "/properties/RemoveSubnetIds" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "ec2:DescribeTransitGatewayVpcAttachments", "ec2:CreateTransitGatewayVpcAttachment", "ec2:CreateTags", "ec2:DescribeTags" ]
    },
    "read" : {
      "permissions" : [ "ec2:DescribeTransitGatewayVpcAttachments", "ec2:DescribeTags" ]
    },
    "delete" : {
      "permissions" : [ "ec2:DescribeTransitGatewayVpcAttachments", "ec2:DeleteTransitGatewayVpcAttachment", "ec2:DeleteTags", "ec2:DescribeTags" ]
    },
    "list" : {
      "permissions" : [ "ec2:DescribeTransitGatewayVpcAttachments", "ec2:DescribeTags" ]
    },
    "update" : {
      "permissions" : [ "ec2:DescribeTransitGatewayVpcAttachments", "ec2:DescribeTags", "ec2:CreateTransitGatewayVpcAttachment", "ec2:CreateTags", "ec2:DeleteTransitGatewayVpcAttachment", "ec2:DeleteTags", "ec2:ModifyTransitGatewayVpcAttachment" ]
    }
  }
}