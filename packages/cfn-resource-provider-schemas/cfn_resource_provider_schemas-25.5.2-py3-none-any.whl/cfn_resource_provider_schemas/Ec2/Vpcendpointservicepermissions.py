SCHEMA = {
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "handlers" : {
    "read" : {
      "permissions" : [ "ec2:CreateVpcEndpointServicePermissions", "ec2:ModifyVpcEndpointServicePermissions", "ec2:DeleteVpcEndpointServicePermissions", "ec2:DescribeVpcEndpointServicePermissions" ]
    },
    "create" : {
      "permissions" : [ "ec2:CreateVpcEndpointServicePermissions", "ec2:ModifyVpcEndpointServicePermissions", "ec2:DeleteVpcEndpointServicePermissions", "ec2:DescribeVpcEndpointServicePermissions" ]
    },
    "update" : {
      "permissions" : [ "ec2:CreateVpcEndpointServicePermissions", "ec2:ModifyVpcEndpointServicePermissions", "ec2:DeleteVpcEndpointServicePermissions", "ec2:DescribeVpcEndpointServicePermissions" ]
    },
    "list" : {
      "permissions" : [ "ec2:CreateVpcEndpointServicePermissions", "ec2:ModifyVpcEndpointServicePermissions", "ec2:DeleteVpcEndpointServicePermissions", "ec2:DescribeVpcEndpointServicePermissions" ]
    },
    "delete" : {
      "permissions" : [ "ec2:CreateVpcEndpointServicePermissions", "ec2:ModifyVpcEndpointServicePermissions", "ec2:DeleteVpcEndpointServicePermissions", "ec2:DescribeVpcEndpointServicePermissions" ]
    }
  },
  "typeName" : "AWS::EC2::VPCEndpointServicePermissions",
  "description" : "Resource Type definition for AWS::EC2::VPCEndpointServicePermissions",
  "createOnlyProperties" : [ "/properties/ServiceId" ],
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/ServiceId" ],
  "properties" : {
    "AllowedPrincipals" : {
      "uniqueItems" : False,
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "ServiceId" : {
      "type" : "string"
    }
  },
  "required" : [ "ServiceId" ]
}