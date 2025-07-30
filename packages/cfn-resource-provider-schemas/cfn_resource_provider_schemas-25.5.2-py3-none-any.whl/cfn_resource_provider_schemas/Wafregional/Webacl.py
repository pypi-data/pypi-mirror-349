SCHEMA = {
  "typeName" : "AWS::WAFRegional::WebACL",
  "description" : "Resource Type definition for AWS::WAFRegional::WebACL",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "MetricName" : {
      "type" : "string"
    },
    "DefaultAction" : {
      "$ref" : "#/definitions/Action"
    },
    "Rules" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Rule"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "Action" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        }
      },
      "required" : [ "Type" ]
    },
    "Rule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Action" : {
          "$ref" : "#/definitions/Action"
        },
        "Priority" : {
          "type" : "integer"
        },
        "RuleId" : {
          "type" : "string"
        }
      },
      "required" : [ "Action", "Priority", "RuleId" ]
    }
  },
  "required" : [ "DefaultAction", "MetricName", "Name" ],
  "createOnlyProperties" : [ "/properties/MetricName", "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}