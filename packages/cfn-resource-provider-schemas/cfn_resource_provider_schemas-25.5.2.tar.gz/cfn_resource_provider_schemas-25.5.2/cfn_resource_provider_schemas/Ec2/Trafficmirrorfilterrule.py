SCHEMA = {
  "typeName" : "AWS::EC2::TrafficMirrorFilterRule",
  "description" : "Resource Type definition for AWS::EC2::TrafficMirrorFilterRule",
  "additionalProperties" : False,
  "properties" : {
    "DestinationPortRange" : {
      "$ref" : "#/definitions/TrafficMirrorPortRange"
    },
    "Description" : {
      "type" : "string"
    },
    "SourcePortRange" : {
      "$ref" : "#/definitions/TrafficMirrorPortRange"
    },
    "RuleAction" : {
      "type" : "string"
    },
    "SourceCidrBlock" : {
      "type" : "string"
    },
    "RuleNumber" : {
      "type" : "integer"
    },
    "DestinationCidrBlock" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "TrafficMirrorFilterId" : {
      "type" : "string"
    },
    "TrafficDirection" : {
      "type" : "string"
    },
    "Protocol" : {
      "type" : "integer"
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
    "TrafficMirrorPortRange" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ToPort" : {
          "type" : "integer"
        },
        "FromPort" : {
          "type" : "integer"
        }
      },
      "required" : [ "FromPort", "ToPort" ]
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
    }
  },
  "required" : [ "RuleAction", "SourceCidrBlock", "RuleNumber", "DestinationCidrBlock", "TrafficMirrorFilterId", "TrafficDirection" ],
  "createOnlyProperties" : [ "/properties/TrafficMirrorFilterId" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}