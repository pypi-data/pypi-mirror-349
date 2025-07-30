SCHEMA = {
  "typeName" : "AWS::CloudWatch::InsightRule",
  "description" : "Resource Type definition for AWS::CloudWatch::InsightRule",
  "additionalProperties" : False,
  "properties" : {
    "RuleState" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "RuleBody" : {
      "type" : "string"
    },
    "RuleName" : {
      "type" : "string"
    },
    "Tags" : {
      "$ref" : "#/definitions/Tags"
    }
  },
  "definitions" : {
    "Tags" : {
      "type" : "object",
      "additionalProperties" : False
    }
  },
  "required" : [ "RuleState", "RuleBody", "RuleName" ],
  "createOnlyProperties" : [ "/properties/RuleName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Arn" ]
}