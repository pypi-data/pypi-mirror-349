SCHEMA = {
  "typeName" : "AWS::EC2::TrafficMirrorSession",
  "description" : "Resource Type definition for AWS::EC2::TrafficMirrorSession",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "TrafficMirrorTargetId" : {
      "type" : "string"
    },
    "Description" : {
      "type" : "string"
    },
    "SessionNumber" : {
      "type" : "integer"
    },
    "VirtualNetworkId" : {
      "type" : "integer"
    },
    "PacketLength" : {
      "type" : "integer"
    },
    "NetworkInterfaceId" : {
      "type" : "string"
    },
    "TrafficMirrorFilterId" : {
      "type" : "string"
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
  "required" : [ "TrafficMirrorTargetId", "NetworkInterfaceId", "TrafficMirrorFilterId", "SessionNumber" ],
  "createOnlyProperties" : [ "/properties/NetworkInterfaceId" ],
  "readOnlyProperties" : [ "/properties/Id" ],
  "primaryIdentifier" : [ "/properties/Id" ]
}