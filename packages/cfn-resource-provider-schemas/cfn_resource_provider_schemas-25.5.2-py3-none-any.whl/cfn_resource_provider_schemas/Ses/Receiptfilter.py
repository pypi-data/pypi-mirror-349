SCHEMA = {
  "typeName" : "AWS::SES::ReceiptFilter",
  "description" : "Resource Type definition for AWS::SES::ReceiptFilter",
  "additionalProperties" : False,
  "properties" : {
    "Filter" : {
      "$ref" : "#/definitions/Filter"
    },
    "Id" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "IpFilter" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Policy" : {
          "type" : "string"
        },
        "Cidr" : {
          "type" : "string"
        }
      },
      "required" : [ "Policy", "Cidr" ]
    },
    "Filter" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IpFilter" : {
          "$ref" : "#/definitions/IpFilter"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "IpFilter" ]
    }
  },
  "required" : [ "Filter" ],
  "createOnlyProperties" : [ "/properties/Filter" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}