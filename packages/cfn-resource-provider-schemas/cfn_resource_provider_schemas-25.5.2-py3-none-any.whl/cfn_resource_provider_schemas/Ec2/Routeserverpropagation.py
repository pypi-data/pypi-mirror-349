SCHEMA = {
  "typeName" : "AWS::EC2::RouteServerPropagation",
  "description" : "VPC Route Server Propagation",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : { },
  "properties" : {
    "RouteServerId" : {
      "description" : "Route Server ID",
      "type" : "string"
    },
    "RouteTableId" : {
      "description" : "Route Table ID",
      "type" : "string"
    }
  },
  "additionalProperties" : False,
  "required" : [ "RouteServerId", "RouteTableId" ],
  "primaryIdentifier" : [ "/properties/RouteServerId", "/properties/RouteTableId" ],
  "createOnlyProperties" : [ "/properties/RouteServerId", "/properties/RouteTableId" ],
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "ec2:EnableRouteServerPropagation", "ec2:GetRouteServerPropagations" ]
    },
    "read" : {
      "permissions" : [ "ec2:GetRouteServerPropagations" ]
    },
    "delete" : {
      "permissions" : [ "ec2:GetRouteServerPropagations", "ec2:DisableRouteServerPropagation" ]
    },
    "list" : {
      "permissions" : [ "ec2:DescribeRouteServers", "ec2:GetRouteServerPropagations" ]
    }
  }
}