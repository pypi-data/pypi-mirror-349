SCHEMA = {
  "typeName" : "AWS::WAFRegional::RegexPatternSet",
  "description" : "Resource Type definition for AWS::WAFRegional::RegexPatternSet",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "RegexPatternStrings" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "Name" : {
      "type" : "string"
    }
  },
  "required" : [ "RegexPatternStrings", "Name" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}