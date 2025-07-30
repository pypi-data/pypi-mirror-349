SCHEMA = {
  "typeName" : "AWS::IoTWireless::NetworkAnalyzerConfiguration",
  "description" : "Create and manage NetworkAnalyzerConfiguration resource.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : {
    "WirelessDeviceFrameInfo" : {
      "type" : "string",
      "enum" : [ "ENABLED", "DISABLED" ]
    },
    "LogLevel" : {
      "type" : "string",
      "enum" : [ "INFO", "ERROR", "DISABLED" ]
    },
    "Tag" : {
      "description" : "A key-value pair to associate with a resource.",
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "description" : "The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "type" : "string",
          "description" : "The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.",
          "minLength" : 0,
          "maxLength" : 256
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    }
  },
  "properties" : {
    "Name" : {
      "description" : "Name of the network analyzer configuration",
      "type" : "string",
      "pattern" : "^[a-zA-Z0-9-_]+$",
      "maxLength" : 1024
    },
    "Description" : {
      "description" : "The description of the new resource",
      "type" : "string",
      "maxLength" : 2048
    },
    "TraceContent" : {
      "description" : "Trace content for your wireless gateway and wireless device resources",
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "WirelessDeviceFrameInfo" : {
          "$ref" : "#/definitions/WirelessDeviceFrameInfo"
        },
        "LogLevel" : {
          "$ref" : "#/definitions/LogLevel"
        }
      }
    },
    "WirelessDevices" : {
      "description" : "List of wireless gateway resources that have been added to the network analyzer configuration",
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "type" : "string"
      },
      "maxItems" : 250
    },
    "WirelessGateways" : {
      "description" : "List of wireless gateway resources that have been added to the network analyzer configuration",
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "type" : "string"
      },
      "maxItems" : 250
    },
    "Arn" : {
      "description" : "Arn for network analyzer configuration, Returned upon successful create.",
      "type" : "string"
    },
    "Tags" : {
      "description" : "An array of key-value pairs to apply to this resource.",
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
      "maxItems" : 200,
      "items" : {
        "$ref" : "#/definitions/Tag"
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
    "permissions" : [ "iotwireless:TagResource", "iotwireless:UntagResource", "iotwireless:ListTagsForResource" ]
  },
  "required" : [ "Name" ],
  "readOnlyProperties" : [ "/properties/Arn" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Name" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iotwireless:CreateNetworkAnalyzerConfiguration", "iotwireless:TagResource" ]
    },
    "read" : {
      "permissions" : [ "iotwireless:GetNetworkAnalyzerConfiguration", "iotwireless:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "iotwireless:UpdateNetworkAnalyzerConfiguration", "iotwireless:GetNetworkAnalyzerConfiguration", "iotwireless:TagResource", "iotwireless:UntagResource" ]
    },
    "delete" : {
      "permissions" : [ "iotwireless:DeleteNetworkAnalyzerConfiguration" ]
    },
    "list" : {
      "permissions" : [ "iotwireless:ListNetworkAnalyzerConfigurations", "iotwireless:ListTagsForResource" ]
    }
  }
}