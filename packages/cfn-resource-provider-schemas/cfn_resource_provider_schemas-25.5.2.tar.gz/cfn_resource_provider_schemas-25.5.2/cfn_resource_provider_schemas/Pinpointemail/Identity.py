SCHEMA = {
  "typeName" : "AWS::PinpointEmail::Identity",
  "description" : "Resource Type definition for AWS::PinpointEmail::Identity",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "IdentityDNSRecordName3" : {
      "type" : "string"
    },
    "IdentityDNSRecordName1" : {
      "type" : "string"
    },
    "IdentityDNSRecordName2" : {
      "type" : "string"
    },
    "IdentityDNSRecordValue3" : {
      "type" : "string"
    },
    "IdentityDNSRecordValue2" : {
      "type" : "string"
    },
    "IdentityDNSRecordValue1" : {
      "type" : "string"
    },
    "FeedbackForwardingEnabled" : {
      "type" : "boolean"
    },
    "DkimSigningEnabled" : {
      "type" : "boolean"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tags"
      }
    },
    "Name" : {
      "type" : "string"
    },
    "MailFromAttributes" : {
      "$ref" : "#/definitions/MailFromAttributes"
    }
  },
  "definitions" : {
    "Tags" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      }
    },
    "MailFromAttributes" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MailFromDomain" : {
          "type" : "string"
        },
        "BehaviorOnMxFailure" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "Name" ],
  "readOnlyProperties" : [ "/properties/IdentityDNSRecordName1", "/properties/IdentityDNSRecordValue1", "/properties/IdentityDNSRecordName3", "/properties/IdentityDNSRecordValue2", "/properties/IdentityDNSRecordName2", "/properties/IdentityDNSRecordValue3", "/properties/Id" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ]
}