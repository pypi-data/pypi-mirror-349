SCHEMA = {
  "typeName" : "AWS::SES::VdmAttributes",
  "description" : "Resource Type definition for AWS::SES::VdmAttributes",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-ses.git",
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/VdmAttributesResourceId" ],
  "properties" : {
    "VdmAttributesResourceId" : {
      "type" : "string",
      "description" : "Unique identifier for this resource"
    },
    "DashboardAttributes" : {
      "$ref" : "#/definitions/DashboardAttributes"
    },
    "GuardianAttributes" : {
      "$ref" : "#/definitions/GuardianAttributes"
    }
  },
  "definitions" : {
    "DashboardAttributes" : {
      "type" : "object",
      "additionalProperties" : False,
      "description" : "Preferences regarding the Dashboard feature.",
      "properties" : {
        "EngagementMetrics" : {
          "type" : "string",
          "description" : "Whether emails sent from this account have engagement tracking enabled.",
          "pattern" : "ENABLED|DISABLED"
        }
      }
    },
    "GuardianAttributes" : {
      "type" : "object",
      "additionalProperties" : False,
      "description" : "Preferences regarding the Guardian feature.",
      "properties" : {
        "OptimizedSharedDelivery" : {
          "type" : "string",
          "description" : "Whether emails sent from this account have optimized delivery algorithm enabled.",
          "pattern" : "ENABLED|DISABLED"
        }
      }
    }
  },
  "readOnlyProperties" : [ "/properties/VdmAttributesResourceId" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "ses:PutAccountVdmAttributes", "ses:GetAccount" ]
    },
    "read" : {
      "permissions" : [ "ses:GetAccount" ]
    },
    "update" : {
      "permissions" : [ "ses:PutAccountVdmAttributes", "ses:GetAccount" ]
    },
    "delete" : {
      "permissions" : [ "ses:PutAccountVdmAttributes", "ses:GetAccount" ]
    }
  },
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  }
}