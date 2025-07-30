SCHEMA = {
  "typeName" : "AWS::EC2::RouteServerAssociation",
  "description" : "VPC Route Server Association",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : { },
  "properties" : {
    "RouteServerId" : {
      "description" : "Route Server ID",
      "type" : "string"
    },
    "VpcId" : {
      "description" : "VPC ID",
      "type" : "string"
    }
  },
  "additionalProperties" : False,
  "required" : [ "RouteServerId", "VpcId" ],
  "primaryIdentifier" : [ "/properties/RouteServerId", "/properties/VpcId" ],
  "createOnlyProperties" : [ "/properties/RouteServerId", "/properties/VpcId" ],
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "ec2:AssociateRouteServer", "ec2:GetRouteServerAssociations" ]
    },
    "read" : {
      "permissions" : [ "ec2:GetRouteServerAssociations" ]
    },
    "delete" : {
      "permissions" : [ "ec2:GetRouteServerAssociations", "ec2:DisassociateRouteServer" ]
    },
    "list" : {
      "permissions" : [ "ec2:DescribeRouteServers", "ec2:GetRouteServerAssociations" ]
    }
  }
}