SCHEMA = {
  "typeName" : "AWS::AppMesh::Route",
  "description" : "Resource Type definition for AWS::AppMesh::Route",
  "additionalProperties" : False,
  "properties" : {
    "Uid" : {
      "type" : "string"
    },
    "MeshName" : {
      "type" : "string"
    },
    "VirtualRouterName" : {
      "type" : "string"
    },
    "MeshOwner" : {
      "type" : "string"
    },
    "ResourceOwner" : {
      "type" : "string"
    },
    "RouteName" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "Spec" : {
      "$ref" : "#/definitions/RouteSpec"
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
    "HttpRetryPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxRetries" : {
          "type" : "integer"
        },
        "TcpRetryEvents" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "PerRetryTimeout" : {
          "$ref" : "#/definitions/Duration"
        },
        "HttpRetryEvents" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "MaxRetries", "PerRetryTimeout" ]
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
    "GrpcRoute" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Action" : {
          "$ref" : "#/definitions/GrpcRouteAction"
        },
        "RetryPolicy" : {
          "$ref" : "#/definitions/GrpcRetryPolicy"
        },
        "Timeout" : {
          "$ref" : "#/definitions/GrpcTimeout"
        },
        "Match" : {
          "$ref" : "#/definitions/GrpcRouteMatch"
        }
      },
      "required" : [ "Action", "Match" ]
    },
    "HttpRouteAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "WeightedTargets" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/WeightedTarget"
          }
        }
      },
      "required" : [ "WeightedTargets" ]
    },
    "TcpRoute" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Action" : {
          "$ref" : "#/definitions/TcpRouteAction"
        },
        "Timeout" : {
          "$ref" : "#/definitions/TcpTimeout"
        },
        "Match" : {
          "$ref" : "#/definitions/TcpRouteMatch"
        }
      },
      "required" : [ "Action" ]
    },
    "HttpRouteHeader" : {
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
          "$ref" : "#/definitions/HeaderMatchMethod"
        }
      },
      "required" : [ "Name" ]
    },
    "GrpcTimeout" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PerRequest" : {
          "$ref" : "#/definitions/Duration"
        },
        "Idle" : {
          "$ref" : "#/definitions/Duration"
        }
      }
    },
    "GrpcRouteMetadataMatchMethod" : {
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
          "$ref" : "#/definitions/MatchRange"
        }
      }
    },
    "GrpcRouteMetadata" : {
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
          "$ref" : "#/definitions/GrpcRouteMetadataMatchMethod"
        }
      },
      "required" : [ "Name" ]
    },
    "HeaderMatchMethod" : {
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
          "$ref" : "#/definitions/MatchRange"
        }
      }
    },
    "GrpcRetryPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxRetries" : {
          "type" : "integer"
        },
        "TcpRetryEvents" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "PerRetryTimeout" : {
          "$ref" : "#/definitions/Duration"
        },
        "GrpcRetryEvents" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "HttpRetryEvents" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "MaxRetries", "PerRetryTimeout" ]
    },
    "TcpTimeout" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Idle" : {
          "$ref" : "#/definitions/Duration"
        }
      }
    },
    "WeightedTarget" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VirtualNode" : {
          "type" : "string"
        },
        "Weight" : {
          "type" : "integer"
        },
        "Port" : {
          "type" : "integer"
        }
      },
      "required" : [ "VirtualNode", "Weight" ]
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
    "HttpTimeout" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PerRequest" : {
          "$ref" : "#/definitions/Duration"
        },
        "Idle" : {
          "$ref" : "#/definitions/Duration"
        }
      }
    },
    "TcpRouteAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "WeightedTargets" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/WeightedTarget"
          }
        }
      },
      "required" : [ "WeightedTargets" ]
    },
    "GrpcRouteMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Metadata" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/GrpcRouteMetadata"
          }
        },
        "MethodName" : {
          "type" : "string"
        },
        "ServiceName" : {
          "type" : "string"
        },
        "Port" : {
          "type" : "integer"
        }
      }
    },
    "MatchRange" : {
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
    "Duration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "integer"
        },
        "Unit" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Unit" ]
    },
    "RouteSpec" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "HttpRoute" : {
          "$ref" : "#/definitions/HttpRoute"
        },
        "Http2Route" : {
          "$ref" : "#/definitions/HttpRoute"
        },
        "GrpcRoute" : {
          "$ref" : "#/definitions/GrpcRoute"
        },
        "TcpRoute" : {
          "$ref" : "#/definitions/TcpRoute"
        },
        "Priority" : {
          "type" : "integer"
        }
      }
    },
    "TcpRouteMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Port" : {
          "type" : "integer"
        }
      }
    },
    "HttpRoute" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Action" : {
          "$ref" : "#/definitions/HttpRouteAction"
        },
        "RetryPolicy" : {
          "$ref" : "#/definitions/HttpRetryPolicy"
        },
        "Timeout" : {
          "$ref" : "#/definitions/HttpTimeout"
        },
        "Match" : {
          "$ref" : "#/definitions/HttpRouteMatch"
        }
      },
      "required" : [ "Action", "Match" ]
    },
    "GrpcRouteAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "WeightedTargets" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/WeightedTarget"
          }
        }
      },
      "required" : [ "WeightedTargets" ]
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
    "HttpRouteMatch" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Path" : {
          "$ref" : "#/definitions/HttpPathMatch"
        },
        "Scheme" : {
          "type" : "string"
        },
        "Headers" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/HttpRouteHeader"
          }
        },
        "Port" : {
          "type" : "integer"
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
    }
  },
  "required" : [ "MeshName", "VirtualRouterName", "Spec" ],
  "createOnlyProperties" : [ "/properties/MeshName", "/properties/VirtualRouterName", "/properties/RouteName", "/properties/MeshOwner" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/ResourceOwner", "/properties/Arn", "/properties/Uid" ]
}