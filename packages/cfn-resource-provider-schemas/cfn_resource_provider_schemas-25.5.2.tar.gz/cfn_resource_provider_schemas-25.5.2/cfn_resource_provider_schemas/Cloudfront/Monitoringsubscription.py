SCHEMA = {
  "additionalProperties" : False,
  "createOnlyProperties" : [ "/properties/DistributionId" ],
  "definitions" : {
    "MonitoringSubscription" : {
      "additionalProperties" : False,
      "properties" : {
        "RealtimeMetricsSubscriptionConfig" : {
          "$ref" : "#/definitions/RealtimeMetricsSubscriptionConfig",
          "description" : "A subscription configuration for additional CloudWatch metrics."
        }
      },
      "type" : "object",
      "description" : "A monitoring subscription. This structure contains information about whether additional CloudWatch metrics are enabled for a given CloudFront distribution."
    },
    "RealtimeMetricsSubscriptionConfig" : {
      "additionalProperties" : False,
      "properties" : {
        "RealtimeMetricsSubscriptionStatus" : {
          "enum" : [ "Enabled", "Disabled" ],
          "type" : "string",
          "description" : "A flag that indicates whether additional CloudWatch metrics are enabled for a given CloudFront distribution."
        }
      },
      "required" : [ "RealtimeMetricsSubscriptionStatus" ],
      "type" : "object",
      "description" : "A subscription configuration for additional CloudWatch metrics."
    }
  },
  "description" : "A monitoring subscription. This structure contains information about whether additional CloudWatch metrics are enabled for a given CloudFront distribution.",
  "handlers" : {
    "create" : {
      "permissions" : [ "cloudfront:CreateMonitoringSubscription" ]
    },
    "delete" : {
      "permissions" : [ "cloudfront:DeleteMonitoringSubscription" ]
    },
    "read" : {
      "permissions" : [ "cloudfront:GetMonitoringSubscription" ]
    }
  },
  "primaryIdentifier" : [ "/properties/DistributionId" ],
  "properties" : {
    "DistributionId" : {
      "type" : "string",
      "description" : "The ID of the distribution that you are enabling metrics for."
    },
    "MonitoringSubscription" : {
      "$ref" : "#/definitions/MonitoringSubscription",
      "description" : "A subscription configuration for additional CloudWatch metrics."
    }
  },
  "required" : [ "DistributionId", "MonitoringSubscription" ],
  "tagging" : {
    "cloudFormationSystemTags" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "taggable" : False
  },
  "typeName" : "AWS::CloudFront::MonitoringSubscription"
}