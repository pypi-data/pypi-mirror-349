SCHEMA = {
  "typeName" : "AWS::WAF::WebACL",
  "description" : "Resource Type definition for AWS::WAF::WebACL",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "DefaultAction" : {
      "$ref" : "#/definitions/WafAction"
    },
    "MetricName" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    },
    "Rules" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/ActivatedRule"
      }
    }
  },
  "definitions" : {
    "ActivatedRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Action" : {
          "$ref" : "#/definitions/WafAction"
        },
        "Priority" : {
          "type" : "integer"
        },
        "RuleId" : {
          "type" : "string"
        }
      },
      "required" : [ "Priority", "RuleId" ]
    },
    "WafAction" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        }
      },
      "required" : [ "Type" ]
    }
  },
  "required" : [ "DefaultAction", "MetricName", "Name" ],
  "createOnlyProperties" : [ "/properties/MetricName", "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}