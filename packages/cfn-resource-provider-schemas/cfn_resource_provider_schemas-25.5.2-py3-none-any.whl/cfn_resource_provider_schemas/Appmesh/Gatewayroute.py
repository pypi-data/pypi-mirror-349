SCHEMA = {
  "typeName" : "AWS::AppMesh::GatewayRoute",
  "description" : "Resource Type definition for AWS::AppMesh::GatewayRoute",
  "additionalProperties" : False,
  "properties" : {
    "Uid" : {
      "type" : "string"
    },
    "MeshName" : {
      "type" : "string"
    },
    "VirtualGatewayName" : {
      "type" : "string"
    },
    "MeshOwner" : {
      "type" : "string"
    },
    "ResourceOwner" : {
      "type" : "string"
    },
    "GatewayRouteName" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "Spec" : {
      "$ref" : "#/definitions/GatewayRouteSpec"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "definitions" : {
    "GatewayRouteHostnameMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Suffix" : {
          "type" : "string"
        },
        "Exact" : {
          "type" : "string"
        }
      }
    },
    "QueryParameter" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "Match" : {
          "$ref" : "#/definitions/HttpQueryParameterMatch"
        }
      },
      "required" : [ "Name" ]
    },
    "GatewayRouteVirtualService" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VirtualServiceName" : {
          "type" : "string"
        }
      },
      "required" : [ "VirtualServiceName" ]
    },
    "GatewayRouteTarget" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VirtualService" : {
          "$ref" : "#/definitions/GatewayRouteVirtualService"
        },
        "Port" : {
          "type" : "integer"
        }
      },
      "required" : [ "VirtualService" ]
    },
    "GrpcGatewayRouteMetadata" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Invert" : {
          "type" : "boolean"
        },
        "Name" : {
          "type" : "string"
        },
        "Match" : {
          "$ref" : "#/definitions/GatewayRouteMetadataMatch"
        }
      },
      "required" : [ "Name" ]
    },
    "GrpcGatewayRouteMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Hostname" : {
          "$ref" : "#/definitions/GatewayRouteHostnameMatch"
        },
        "Metadata" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/GrpcGatewayRouteMetadata"
          }
        },
        "ServiceName" : {
          "type" : "string"
        },
        "Port" : {
          "type" : "integer"
        }
      }
    },
    "HttpQueryParameterMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Exact" : {
          "type" : "string"
        }
      }
    },
    "HttpGatewayRoutePrefixRewrite" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "DefaultPrefix" : {
          "type" : "string"
        }
      }
    },
    "GrpcGatewayRoute" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Action" : {
          "$ref" : "#/definitions/GrpcGatewayRouteAction"
        },
        "Match" : {
          "$ref" : "#/definitions/GrpcGatewayRouteMatch"
        }
      },
      "required" : [ "Action", "Match" ]
    },
    "GatewayRouteSpec" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "HttpRoute" : {
          "$ref" : "#/definitions/HttpGatewayRoute"
        },
        "Http2Route" : {
          "$ref" : "#/definitions/HttpGatewayRoute"
        },
        "GrpcRoute" : {
          "$ref" : "#/definitions/GrpcGatewayRoute"
        },
        "Priority" : {
          "type" : "integer"
        }
      }
    },
    "HttpGatewayRouteMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Path" : {
          "$ref" : "#/definitions/HttpPathMatch"
        },
        "Headers" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/HttpGatewayRouteHeader"
          }
        },
        "Port" : {
          "type" : "integer"
        },
        "Hostname" : {
          "$ref" : "#/definitions/GatewayRouteHostnameMatch"
        },
        "Prefix" : {
          "type" : "string"
        },
        "Method" : {
          "type" : "string"
        },
        "QueryParameters" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/QueryParameter"
          }
        }
      }
    },
    "HttpGatewayRouteAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Target" : {
          "$ref" : "#/definitions/GatewayRouteTarget"
        },
        "Rewrite" : {
          "$ref" : "#/definitions/HttpGatewayRouteRewrite"
        }
      },
      "required" : [ "Target" ]
    },
    "GrpcGatewayRouteRewrite" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Hostname" : {
          "$ref" : "#/definitions/GatewayRouteHostnameRewrite"
        }
      }
    },
    "HttpGatewayRouteHeader" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Invert" : {
          "type" : "boolean"
        },
        "Name" : {
          "type" : "string"
        },
        "Match" : {
          "$ref" : "#/definitions/HttpGatewayRouteHeaderMatch"
        }
      },
      "required" : [ "Name" ]
    },
    "GatewayRouteRangeMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Start" : {
          "type" : "integer"
        },
        "End" : {
          "type" : "integer"
        }
      },
      "required" : [ "Start", "End" ]
    },
    "GrpcGatewayRouteAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Target" : {
          "$ref" : "#/definitions/GatewayRouteTarget"
        },
        "Rewrite" : {
          "$ref" : "#/definitions/GrpcGatewayRouteRewrite"
        }
      },
      "required" : [ "Target" ]
    },
    "HttpGatewayRouteHeaderMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Suffix" : {
          "type" : "string"
        },
        "Exact" : {
          "type" : "string"
        },
        "Prefix" : {
          "type" : "string"
        },
        "Regex" : {
          "type" : "string"
        },
        "Range" : {
          "$ref" : "#/definitions/GatewayRouteRangeMatch"
        }
      }
    },
    "HttpGatewayRoutePathRewrite" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Exact" : {
          "type" : "string"
        }
      }
    },
    "GatewayRouteMetadataMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Suffix" : {
          "type" : "string"
        },
        "Exact" : {
          "type" : "string"
        },
        "Prefix" : {
          "type" : "string"
        },
        "Regex" : {
          "type" : "string"
        },
        "Range" : {
          "$ref" : "#/definitions/GatewayRouteRangeMatch"
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
    "HttpPathMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Regex" : {
          "type" : "string"
        },
        "Exact" : {
          "type" : "string"
        }
      }
    },
    "HttpGatewayRoute" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Action" : {
          "$ref" : "#/definitions/HttpGatewayRouteAction"
        },
        "Match" : {
          "$ref" : "#/definitions/HttpGatewayRouteMatch"
        }
      },
      "required" : [ "Action", "Match" ]
    },
    "HttpGatewayRouteRewrite" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Path" : {
          "$ref" : "#/definitions/HttpGatewayRoutePathRewrite"
        },
        "Hostname" : {
          "$ref" : "#/definitions/GatewayRouteHostnameRewrite"
        },
        "Prefix" : {
          "$ref" : "#/definitions/HttpGatewayRoutePrefixRewrite"
        }
      }
    },
    "GatewayRouteHostnameRewrite" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DefaultTargetHostname" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "MeshName", "VirtualGatewayName", "Spec" ],
  "createOnlyProperties" : [ "/properties/MeshName", "/properties/VirtualGatewayName", "/properties/MeshOwner", "/properties/GatewayRouteName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/ResourceOwner", "/properties/Arn", "/properties/Uid" ]
}