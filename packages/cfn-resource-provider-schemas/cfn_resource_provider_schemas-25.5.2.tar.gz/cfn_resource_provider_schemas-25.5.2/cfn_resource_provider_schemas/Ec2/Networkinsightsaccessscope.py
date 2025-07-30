SCHEMA = {
  "typeName" : "AWS::EC2::NetworkInsightsAccessScope",
  "description" : "Resource schema for AWS::EC2::NetworkInsightsAccessScope",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-ec2-ni.git",
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
      "required" : [ "Key" ]
    },
    "AccessScopePathRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Source" : {
          "$ref" : "#/definitions/PathStatementRequest"
        },
        "Destination" : {
          "$ref" : "#/definitions/PathStatementRequest"
        },
        "ThroughResources" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "$ref" : "#/definitions/ThroughResourcesStatementRequest"
          }
        }
      }
    },
    "PathStatementRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PacketHeaderStatement" : {
          "$ref" : "#/definitions/PacketHeaderStatementRequest"
        },
        "ResourceStatement" : {
          "$ref" : "#/definitions/ResourceStatementRequest"
        }
      }
    },
    "PacketHeaderStatementRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SourceAddresses" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "type" : "string"
          }
        },
        "DestinationAddresses" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "type" : "string"
          }
        },
        "SourcePorts" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "type" : "string"
          }
        },
        "DestinationPorts" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "type" : "string"
          }
        },
        "SourcePrefixLists" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "type" : "string"
          }
        },
        "DestinationPrefixLists" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "type" : "string"
          }
        },
        "Protocols" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "$ref" : "#/definitions/Protocol"
          }
        }
      }
    },
    "Protocol" : {
      "type" : "string",
      "enum" : [ "tcp", "udp" ]
    },
    "ResourceStatementRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Resources" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "type" : "string"
          }
        },
        "ResourceTypes" : {
          "type" : "array",
          "insertionOrder" : True,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "ThroughResourcesStatementRequest" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ResourceStatement" : {
          "$ref" : "#/definitions/ResourceStatementRequest"
        }
      }
    }
  },
  "properties" : {
    "NetworkInsightsAccessScopeId" : {
      "type" : "string"
    },
    "NetworkInsightsAccessScopeArn" : {
      "type" : "string"
    },
    "CreatedDate" : {
      "type" : "string"
    },
    "UpdatedDate" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "MatchPaths" : {
      "type" : "array",
      "insertionOrder" : True,
      "items" : {
        "$ref" : "#/definitions/AccessScopePathRequest"
      }
    },
    "ExcludePaths" : {
      "type" : "array",
      "insertionOrder" : True,
      "items" : {
        "$ref" : "#/definitions/AccessScopePathRequest"
      }
    }
  },
  "additionalProperties" : False,
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "ec2:CreateTags", "ec2:DeleteTags" ]
  },
  "readOnlyProperties" : [ "/properties/NetworkInsightsAccessScopeId", "/properties/NetworkInsightsAccessScopeArn", "/properties/CreatedDate", "/properties/UpdatedDate" ],
  "createOnlyProperties" : [ "/properties/MatchPaths", "/properties/ExcludePaths" ],
  "writeOnlyProperties" : [ "/properties/MatchPaths", "/properties/ExcludePaths" ],
  "primaryIdentifier" : [ "/properties/NetworkInsightsAccessScopeId" ],
  "additionalIdentifiers" : [ [ "/properties/NetworkInsightsAccessScopeArn" ] ],
  "handlers" : {
    "create" : {
      "permissions" : [ "ec2:CreateNetworkInsightsAccessScope", "ec2:CreateTags", "tiros:CreateQuery" ]
    },
    "read" : {
      "permissions" : [ "ec2:DescribeNetworkInsightsAccessScopes", "ec2:GetNetworkInsightsAccessScopeContent" ]
    },
    "update" : {
      "permissions" : [ "ec2:DescribeNetworkInsightsAccessScopes", "ec2:GetNetworkInsightsAccessScopeContent", "ec2:CreateTags", "ec2:DeleteTags" ]
    },
    "delete" : {
      "permissions" : [ "ec2:DeleteNetworkInsightsAccessScope", "ec2:DeleteTags" ]
    },
    "list" : {
      "permissions" : [ "ec2:DescribeNetworkInsightsAccessScopes" ]
    }
  }
}