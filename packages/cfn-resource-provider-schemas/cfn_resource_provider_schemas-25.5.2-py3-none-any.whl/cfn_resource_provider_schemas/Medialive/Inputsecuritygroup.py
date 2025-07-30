SCHEMA = {
  "typeName" : "AWS::MediaLive::InputSecurityGroup",
  "description" : "Resource Type definition for AWS::MediaLive::InputSecurityGroup",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "WhitelistRules" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/InputWhitelistRuleCidr"
      }
    },
    "Tags" : {
      "type" : "object"
    }
  },
  "definitions" : {
    "InputWhitelistRuleCidr" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Cidr" : {
          "type" : "string"
        }
      }
    }
  },
  "createOnlyProperties" : [ "/properties/Tags" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Arn" ]
}