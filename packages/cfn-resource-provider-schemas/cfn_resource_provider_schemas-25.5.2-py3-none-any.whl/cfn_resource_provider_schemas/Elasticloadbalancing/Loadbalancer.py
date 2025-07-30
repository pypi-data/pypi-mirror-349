SCHEMA = {
  "typeName" : "AWS::ElasticLoadBalancing::LoadBalancer",
  "description" : "Resource Type definition for AWS::ElasticLoadBalancing::LoadBalancer",
  "additionalProperties" : False,
  "properties" : {
    "SecurityGroups" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "ConnectionDrainingPolicy" : {
      "$ref" : "#/definitions/ConnectionDrainingPolicy"
    },
    "Policies" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Policies"
      }
    },
    "Scheme" : {
      "type" : "string"
    },
    "AvailabilityZones" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "SourceSecurityGroupOwnerAlias" : {
      "type" : "string"
    },
    "HealthCheck" : {
      "$ref" : "#/definitions/HealthCheck"
    },
    "CanonicalHostedZoneNameID" : {
      "type" : "string"
    },
    "CanonicalHostedZoneName" : {
      "type" : "string"
    },
    "DNSName" : {
      "type" : "string"
    },
    "AccessLoggingPolicy" : {
      "$ref" : "#/definitions/AccessLoggingPolicy"
    },
    "Instances" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "LoadBalancerName" : {
      "type" : "string"
    },
    "Listeners" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Listeners"
      }
    },
    "Subnets" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "CrossZone" : {
      "type" : "boolean"
    },
    "AppCookieStickinessPolicy" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/AppCookieStickinessPolicy"
      }
    },
    "LBCookieStickinessPolicy" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/LBCookieStickinessPolicy"
      }
    },
    "Id" : {
      "type" : "string"
    },
    "SourceSecurityGroupGroupName" : {
      "type" : "string"
    },
    "ConnectionSettings" : {
      "$ref" : "#/definitions/ConnectionSettings"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "definitions" : {
    "Listeners" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PolicyNames" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "InstancePort" : {
          "type" : "string"
        },
        "LoadBalancerPort" : {
          "type" : "string"
        },
        "Protocol" : {
          "type" : "string"
        },
        "SSLCertificateId" : {
          "type" : "string"
        },
        "InstanceProtocol" : {
          "type" : "string"
        }
      },
      "required" : [ "InstancePort", "LoadBalancerPort", "Protocol" ]
    },
    "ConnectionDrainingPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "Timeout" : {
          "type" : "integer"
        }
      },
      "required" : [ "Enabled" ]
    },
    "Policies" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Attributes" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "object"
          }
        },
        "PolicyType" : {
          "type" : "string"
        },
        "LoadBalancerPorts" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "PolicyName" : {
          "type" : "string"
        },
        "InstancePorts" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "PolicyType", "PolicyName", "Attributes" ]
    },
    "AppCookieStickinessPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CookieName" : {
          "type" : "string"
        },
        "PolicyName" : {
          "type" : "string"
        }
      },
      "required" : [ "PolicyName", "CookieName" ]
    },
    "LBCookieStickinessPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CookieExpirationPeriod" : {
          "type" : "string"
        },
        "PolicyName" : {
          "type" : "string"
        }
      }
    },
    "HealthCheck" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Target" : {
          "type" : "string"
        },
        "UnhealthyThreshold" : {
          "type" : "string"
        },
        "Timeout" : {
          "type" : "string"
        },
        "HealthyThreshold" : {
          "type" : "string"
        },
        "Interval" : {
          "type" : "string"
        }
      },
      "required" : [ "Target", "UnhealthyThreshold", "Timeout", "HealthyThreshold", "Interval" ]
    },
    "Tag" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Key" ]
    },
    "AccessLoggingPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        },
        "S3BucketName" : {
          "type" : "string"
        },
        "EmitInterval" : {
          "type" : "integer"
        },
        "S3BucketPrefix" : {
          "type" : "string"
        }
      },
      "required" : [ "Enabled", "S3BucketName" ]
    },
    "ConnectionSettings" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IdleTimeout" : {
          "type" : "integer"
        }
      },
      "required" : [ "IdleTimeout" ]
    }
  },
  "required" : [ "Listeners" ],
  "createOnlyProperties" : [ "/properties/LoadBalancerName", "/properties/Scheme" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/CanonicalHostedZoneName", "/properties/CanonicalHostedZoneNameID", "/properties/SourceSecurityGroup.GroupName", "/properties/DNSName", "/properties/SourceSecurityGroup.OwnerAlias" ]
}