SCHEMA = {
  "typeName" : "AWS::AppMesh::VirtualService",
  "description" : "Resource Type definition for AWS::AppMesh::VirtualService",
  "additionalProperties" : False,
  "properties" : {
    "Uid" : {
      "type" : "string"
    },
    "MeshName" : {
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
    "VirtualServiceName" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "Spec" : {
      "$ref" : "#/definitions/VirtualServiceSpec"
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
    "VirtualNodeServiceProvider" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VirtualNodeName" : {
          "type" : "string"
        }
      },
      "required" : [ "VirtualNodeName" ]
    },
    "VirtualServiceProvider" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VirtualNode" : {
          "$ref" : "#/definitions/VirtualNodeServiceProvider"
        },
        "VirtualRouter" : {
          "$ref" : "#/definitions/VirtualRouterServiceProvider"
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
    "VirtualServiceSpec" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Provider" : {
          "$ref" : "#/definitions/VirtualServiceProvider"
        }
      }
    },
    "VirtualRouterServiceProvider" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VirtualRouterName" : {
          "type" : "string"
        }
      },
      "required" : [ "VirtualRouterName" ]
    }
  },
  "required" : [ "MeshName", "VirtualServiceName", "Spec" ],
  "createOnlyProperties" : [ "/properties/MeshName", "/properties/VirtualServiceName", "/properties/MeshOwner" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/ResourceOwner", "/properties/Arn", "/properties/Uid" ]
}