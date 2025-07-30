SCHEMA = {
  "typeName" : "AWS::Oam::Link",
  "description" : "Definition of AWS::Oam::Link Resource Type",
  "definitions" : {
    "ResourceType" : {
      "type" : "string",
      "enum" : [ "AWS::CloudWatch::Metric", "AWS::Logs::LogGroup", "AWS::XRay::Trace", "AWS::ApplicationInsights::Application", "AWS::InternetMonitor::Monitor", "AWS::ApplicationSignals::Service", "AWS::ApplicationSignals::ServiceLevelObjective" ]
    },
    "LinkConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MetricConfiguration" : {
          "$ref" : "#/definitions/LinkFilter"
        },
        "LogGroupConfiguration" : {
          "$ref" : "#/definitions/LinkFilter"
        }
      }
    },
    "LinkFilter" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Filter" : {
          "type" : "string",
          "maxLength" : 2000,
          "minLength" : 1
        }
      },
      "required" : [ "Filter" ]
    }
  },
  "properties" : {
    "Arn" : {
      "type" : "string",
      "maxLength" : 2048
    },
    "Label" : {
      "type" : "string"
    },
    "LabelTemplate" : {
      "type" : "string",
      "maxLength" : 64,
      "minLength" : 1
    },
    "ResourceTypes" : {
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/ResourceType"
      },
      "maxItems" : 50,
      "minItems" : 1,
      "uniqueItems" : True
    },
    "SinkIdentifier" : {
      "type" : "string",
      "maxLength" : 2048,
      "minLength" : 1
    },
    "LinkConfiguration" : {
      "$ref" : "#/definitions/LinkConfiguration"
    },
    "Tags" : {
      "description" : "Tags to apply to the link",
      "type" : "object",
      "additionalProperties" : False,
      "patternProperties" : {
        "^(?!aws:.*).{1,128}$" : {
          "type" : "string",
          "description" : "The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:.",
          "pattern" : "^(?!aws:.*).{0,256}$",
          "minLength" : 0,
          "maxLength" : 256
        }
      }
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "oam:ListTagsForResource", "oam:UntagResource", "oam:TagResource" ]
  },
  "required" : [ "ResourceTypes", "SinkIdentifier" ],
  "readOnlyProperties" : [ "/properties/Arn", "/properties/Label" ],
  "createOnlyProperties" : [ "/properties/SinkIdentifier", "/properties/LabelTemplate" ],
  "writeOnlyProperties" : [ "/properties/LabelTemplate" ],
  "primaryIdentifier" : [ "/properties/Arn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "oam:CreateLink", "oam:GetLink", "oam:TagResource", "oam:ListTagsForResource", "cloudwatch:Link", "logs:Link", "xray:Link", "applicationinsights:Link", "internetmonitor:Link", "application-signals:Link" ]
    },
    "read" : {
      "permissions" : [ "oam:GetLink", "oam:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "oam:GetLink", "oam:UpdateLink", "cloudwatch:Link", "logs:Link", "xray:Link", "applicationinsights:Link", "internetmonitor:Link", "application-signals:Link", "oam:TagResource", "oam:UntagResource", "oam:ListTagsForResource" ]
    },
    "delete" : {
      "permissions" : [ "oam:DeleteLink", "oam:GetLink" ]
    },
    "list" : {
      "permissions" : [ "oam:ListLinks" ]
    }
  },
  "replacementStrategy" : "delete_then_create",
  "additionalProperties" : False
}