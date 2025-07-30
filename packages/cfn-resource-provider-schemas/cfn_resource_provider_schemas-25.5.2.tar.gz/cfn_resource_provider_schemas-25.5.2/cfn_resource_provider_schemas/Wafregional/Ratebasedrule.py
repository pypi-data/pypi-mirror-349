SCHEMA = {
  "typeName" : "AWS::WAFRegional::RateBasedRule",
  "description" : "Resource Type definition for AWS::WAFRegional::RateBasedRule",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "MetricName" : {
      "type" : "string"
    },
    "RateLimit" : {
      "type" : "integer"
    },
    "MatchPredicates" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Predicate"
      }
    },
    "RateKey" : {
      "type" : "string"
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "Predicate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "DataId" : {
          "type" : "string"
        },
        "Negated" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Type", "Negated", "DataId" ]
    }
  },
  "required" : [ "MetricName", "RateLimit", "RateKey", "Name" ],
  "createOnlyProperties" : [ "/properties/MetricName", "/properties/RateKey", "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}