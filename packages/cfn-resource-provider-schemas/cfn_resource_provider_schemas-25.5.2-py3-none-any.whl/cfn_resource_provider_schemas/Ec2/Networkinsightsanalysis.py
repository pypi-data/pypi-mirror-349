SCHEMA = {
  "tagging" : {
    "permissions" : [ "ec2:CreateTags", "ec2:DeleteTags" ],
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "tagProperty" : "/properties/Tags",
    "cloudFormationSystemTags" : False
  },
  "typeName" : "AWS::EC2::NetworkInsightsAnalysis",
  "readOnlyProperties" : [ "/properties/NetworkInsightsAnalysisId", "/properties/NetworkInsightsAnalysisArn", "/properties/StartDate", "/properties/Status", "/properties/StatusMessage", "/properties/NetworkPathFound", "/properties/ForwardPathComponents", "/properties/ReturnPathComponents", "/properties/Explanations", "/properties/AlternatePathHints", "/properties/SuggestedAccounts" ],
  "description" : "Resource schema for AWS::EC2::NetworkInsightsAnalysis",
  "createOnlyProperties" : [ "/properties/NetworkInsightsPathId", "/properties/FilterInArns", "/properties/FilterOutArns" ],
  "primaryIdentifier" : [ "/properties/NetworkInsightsAnalysisId" ],
  "required" : [ "NetworkInsightsPathId" ],
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-ec2-ni.git",
  "handlers" : {
    "read" : {
      "permissions" : [ "ec2:Describe*" ]
    },
    "create" : {
      "permissions" : [ "ec2:CreateTags", "ec2:StartNetworkInsightsAnalysis", "ec2:GetTransitGatewayRouteTablePropagations", "ec2:SearchTransitGatewayRoutes", "ec2:Describe*", "ec2:GetManagedPrefixListEntries", "elasticloadbalancing:Describe*", "directconnect:Describe*", "tiros:CreateQuery", "tiros:GetQueryAnswer", "tiros:GetQueryExplanation" ]
    },
    "update" : {
      "permissions" : [ "ec2:CreateTags", "ec2:Describe*", "ec2:DeleteTags" ]
    },
    "list" : {
      "permissions" : [ "ec2:Describe*" ]
    },
    "delete" : {
      "permissions" : [ "ec2:DeleteNetworkInsightsAnalysis", "ec2:DeleteTags" ]
    }
  },
  "additionalIdentifiers" : [ [ "/properties/NetworkInsightsAnalysisArn" ] ],
  "additionalProperties" : False,
  "definitions" : {
    "PathComponent" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "AdditionalDetails" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/AdditionalDetail"
          }
        },
        "InboundHeader" : {
          "$ref" : "#/definitions/AnalysisPacketHeader"
        },
        "Vpc" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "DestinationVpc" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "SecurityGroupRule" : {
          "$ref" : "#/definitions/AnalysisSecurityGroupRule"
        },
        "TransitGateway" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "ElasticLoadBalancerListener" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "Explanations" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Explanation"
          }
        },
        "ServiceName" : {
          "type" : "string"
        },
        "SequenceNumber" : {
          "type" : "integer"
        },
        "SourceVpc" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "OutboundHeader" : {
          "$ref" : "#/definitions/AnalysisPacketHeader"
        },
        "AclRule" : {
          "$ref" : "#/definitions/AnalysisAclRule"
        },
        "TransitGatewayRouteTableRoute" : {
          "$ref" : "#/definitions/TransitGatewayRouteTableRoute"
        },
        "Component" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "Subnet" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "RouteTableRoute" : {
          "$ref" : "#/definitions/AnalysisRouteTableRoute"
        }
      }
    },
    "AnalysisLoadBalancerListener" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "InstancePort" : {
          "$ref" : "#/definitions/Port"
        },
        "LoadBalancerPort" : {
          "$ref" : "#/definitions/Port"
        }
      }
    },
    "AnalysisLoadBalancerTarget" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Address" : {
          "$ref" : "#/definitions/IpAddress"
        },
        "Instance" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "Port" : {
          "$ref" : "#/definitions/Port"
        },
        "AvailabilityZone" : {
          "type" : "string"
        }
      }
    },
    "Explanation" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "VpnGateway" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "PacketField" : {
          "type" : "string"
        },
        "TransitGatewayAttachment" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "Protocols" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Protocol"
          }
        },
        "IngressRouteTable" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "ClassicLoadBalancerListener" : {
          "$ref" : "#/definitions/AnalysisLoadBalancerListener"
        },
        "VpcPeeringConnection" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "Address" : {
          "$ref" : "#/definitions/IpAddress"
        },
        "Port" : {
          "$ref" : "#/definitions/Port"
        },
        "Addresses" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/IpAddress"
          }
        },
        "ElasticLoadBalancerListener" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "TransitGatewayRouteTable" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "ExplanationCode" : {
          "type" : "string"
        },
        "InternetGateway" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "SourceVpc" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "AttachedTo" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "PrefixList" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "TransitGatewayRouteTableRoute" : {
          "$ref" : "#/definitions/TransitGatewayRouteTableRoute"
        },
        "ComponentRegion" : {
          "type" : "string"
        },
        "LoadBalancerTargetGroup" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "NetworkInterface" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "CustomerGateway" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "DestinationVpc" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "SecurityGroup" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "TransitGateway" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "RouteTable" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "State" : {
          "type" : "string"
        },
        "LoadBalancerListenerPort" : {
          "$ref" : "#/definitions/Port"
        },
        "vpcEndpoint" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "Subnet" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "Cidrs" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "Destination" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "SecurityGroups" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/AnalysisComponent"
          }
        },
        "ComponentAccount" : {
          "type" : "string"
        },
        "VpnConnection" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "Vpc" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "NatGateway" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "Direction" : {
          "type" : "string"
        },
        "LoadBalancerTargetPort" : {
          "$ref" : "#/definitions/Port"
        },
        "LoadBalancerTarget" : {
          "$ref" : "#/definitions/AnalysisLoadBalancerTarget"
        },
        "LoadBalancerTargetGroups" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/AnalysisComponent"
          }
        },
        "Component" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "MissingComponent" : {
          "type" : "string"
        },
        "RouteTableRoute" : {
          "$ref" : "#/definitions/AnalysisRouteTableRoute"
        },
        "AvailabilityZones" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "PortRanges" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PortRange"
          }
        },
        "Acl" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "SecurityGroupRule" : {
          "$ref" : "#/definitions/AnalysisSecurityGroupRule"
        },
        "SubnetRouteTable" : {
          "$ref" : "#/definitions/AnalysisComponent"
        },
        "LoadBalancerArn" : {
          "$ref" : "#/definitions/ResourceArn"
        },
        "AclRule" : {
          "$ref" : "#/definitions/AnalysisAclRule"
        }
      }
    },
    "Port" : {
      "type" : "integer"
    },
    "AnalysisPacketHeader" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "DestinationPortRanges" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PortRange"
          }
        },
        "SourcePortRanges" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PortRange"
          }
        },
        "DestinationAddresses" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/IpAddress"
          }
        },
        "Protocol" : {
          "$ref" : "#/definitions/Protocol"
        },
        "SourceAddresses" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/IpAddress"
          }
        }
      }
    },
    "AdditionalDetail" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ServiceName" : {
          "type" : "string"
        },
        "AdditionalDetailType" : {
          "type" : "string"
        },
        "LoadBalancers" : {
          "uniqueItems" : False,
          "insertionOrder" : True,
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/AnalysisComponent"
          }
        },
        "Component" : {
          "$ref" : "#/definitions/AnalysisComponent"
        }
      }
    },
    "AlternatePathHint" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ComponentArn" : {
          "type" : "string"
        },
        "ComponentId" : {
          "type" : "string"
        }
      }
    },
    "TransitGatewayRouteTableRoute" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PrefixListId" : {
          "type" : "string"
        },
        "ResourceId" : {
          "type" : "string"
        },
        "State" : {
          "type" : "string"
        },
        "ResourceType" : {
          "type" : "string"
        },
        "RouteOrigin" : {
          "type" : "string"
        },
        "DestinationCidr" : {
          "type" : "string"
        },
        "AttachmentId" : {
          "type" : "string"
        }
      }
    },
    "Protocol" : {
      "type" : "string"
    },
    "Tags" : {
      "uniqueItems" : True,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "AnalysisSecurityGroupRule" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PortRange" : {
          "$ref" : "#/definitions/PortRange"
        },
        "Cidr" : {
          "type" : "string"
        },
        "PrefixListId" : {
          "type" : "string"
        },
        "SecurityGroupId" : {
          "type" : "string"
        },
        "Protocol" : {
          "$ref" : "#/definitions/Protocol"
        },
        "Direction" : {
          "type" : "string"
        }
      }
    },
    "AnalysisComponent" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Id" : {
          "type" : "string"
        },
        "Arn" : {
          "type" : "string"
        }
      }
    },
    "AnalysisAclRule" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "PortRange" : {
          "$ref" : "#/definitions/PortRange"
        },
        "Cidr" : {
          "type" : "string"
        },
        "RuleAction" : {
          "type" : "string"
        },
        "Egress" : {
          "type" : "boolean"
        },
        "RuleNumber" : {
          "type" : "integer"
        },
        "Protocol" : {
          "$ref" : "#/definitions/Protocol"
        }
      }
    },
    "AnalysisRouteTableRoute" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Origin" : {
          "type" : "string"
        },
        "destinationPrefixListId" : {
          "type" : "string"
        },
        "destinationCidr" : {
          "type" : "string"
        },
        "NetworkInterfaceId" : {
          "type" : "string"
        },
        "TransitGatewayId" : {
          "type" : "string"
        },
        "VpcPeeringConnectionId" : {
          "type" : "string"
        },
        "instanceId" : {
          "type" : "string"
        },
        "State" : {
          "type" : "string"
        },
        "egressOnlyInternetGatewayId" : {
          "type" : "string"
        },
        "NatGatewayId" : {
          "type" : "string"
        },
        "gatewayId" : {
          "type" : "string"
        }
      }
    },
    "ResourceArn" : {
      "type" : "string"
    },
    "PortRange" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "From" : {
          "type" : "integer"
        },
        "To" : {
          "type" : "integer"
        }
      }
    },
    "IpAddress" : {
      "type" : "string"
    },
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
      "required" : [ "Key" ]
    }
  },
  "properties" : {
    "Status" : {
      "type" : "string",
      "enum" : [ "running", "failed", "succeeded" ]
    },
    "ReturnPathComponents" : {
      "uniqueItems" : False,
      "insertionOrder" : True,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/PathComponent"
      }
    },
    "NetworkInsightsAnalysisId" : {
      "type" : "string"
    },
    "FilterOutArns" : {
      "uniqueItems" : False,
      "insertionOrder" : True,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/ResourceArn"
      }
    },
    "NetworkInsightsPathId" : {
      "type" : "string"
    },
    "NetworkPathFound" : {
      "type" : "boolean"
    },
    "SuggestedAccounts" : {
      "uniqueItems" : True,
      "insertionOrder" : True,
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "FilterInArns" : {
      "uniqueItems" : False,
      "insertionOrder" : True,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/ResourceArn"
      }
    },
    "NetworkInsightsAnalysisArn" : {
      "type" : "string"
    },
    "StatusMessage" : {
      "type" : "string"
    },
    "StartDate" : {
      "type" : "string"
    },
    "AlternatePathHints" : {
      "uniqueItems" : False,
      "insertionOrder" : True,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/AlternatePathHint"
      }
    },
    "Explanations" : {
      "uniqueItems" : False,
      "insertionOrder" : True,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Explanation"
      }
    },
    "ForwardPathComponents" : {
      "uniqueItems" : False,
      "insertionOrder" : True,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/PathComponent"
      }
    },
    "AdditionalAccounts" : {
      "uniqueItems" : True,
      "insertionOrder" : True,
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "Tags" : {
      "uniqueItems" : True,
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  }
}