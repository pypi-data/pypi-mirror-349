SCHEMA = {
  "typeName" : "AWS::SES::ReceiptRuleSet",
  "description" : "Resource Type definition for AWS::SES::ReceiptRuleSet",
  "additionalProperties" : False,
  "properties" : {
    "RuleSetName" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    }
  },
  "createOnlyProperties" : [ "/properties/RuleSetName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}