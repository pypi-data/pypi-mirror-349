SCHEMA = {
  "typeName" : "AWS::AppMesh::VirtualRouter",
  "description" : "Resource Type definition for AWS::AppMesh::VirtualRouter",
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
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "Spec" : {
      "$ref" : "#/definitions/VirtualRouterSpec"
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
    "VirtualRouterSpec" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Listeners" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/VirtualRouterListener"
          }
        }
      },
      "required" : [ "Listeners" ]
    },
    "VirtualRouterListener" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PortMapping" : {
          "$ref" : "#/definitions/PortMapping"
        }
      },
      "required" : [ "PortMapping" ]
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
    "PortMapping" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Protocol" : {
          "type" : "string"
        },
        "Port" : {
          "type" : "integer"
        }
      },
      "required" : [ "Port", "Protocol" ]
    }
  },
  "required" : [ "MeshName", "Spec" ],
  "createOnlyProperties" : [ "/properties/MeshName", "/properties/VirtualRouterName", "/properties/MeshOwner" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/ResourceOwner", "/properties/Arn", "/properties/Uid" ]
}