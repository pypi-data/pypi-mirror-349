SCHEMA = {
  "typeName" : "AWS::IoT::AccountAuditConfiguration",
  "description" : "Configures the Device Defender audit settings for this account. Settings include how audit notifications are sent and which audit checks are enabled or disabled.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-iot.git",
  "definitions" : {
    "AuditCheckConfigurations" : {
      "description" : "Specifies which audit checks are enabled and disabled for this account.",
      "type" : "object",
      "properties" : {
        "AuthenticatedCognitoRoleOverlyPermissiveCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "CaCertificateExpiringCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "CaCertificateKeyQualityCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "ConflictingClientIdsCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "DeviceCertificateExpiringCheck" : {
          "$ref" : "#/definitions/DeviceCertExpirationAuditCheckConfiguration"
        },
        "DeviceCertificateKeyQualityCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "DeviceCertificateSharedCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "IotPolicyOverlyPermissiveCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "IotRoleAliasAllowsAccessToUnusedServicesCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "IotRoleAliasOverlyPermissiveCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "LoggingDisabledCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "RevokedCaCertificateStillActiveCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "RevokedDeviceCertificateStillActiveCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "UnauthenticatedCognitoRoleOverlyPermissiveCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "IntermediateCaRevokedForActiveDeviceCertificatesCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "IoTPolicyPotentialMisConfigurationCheck" : {
          "$ref" : "#/definitions/AuditCheckConfiguration"
        },
        "DeviceCertificateAgeCheck" : {
          "$ref" : "#/definitions/DeviceCertAgeAuditCheckConfiguration"
        }
      },
      "additionalProperties" : False
    },
    "AuditNotificationTargetConfigurations" : {
      "description" : "Information about the targets to which audit notifications are sent.",
      "type" : "object",
      "properties" : {
        "Sns" : {
          "$ref" : "#/definitions/AuditNotificationTarget"
        }
      },
      "additionalProperties" : False
    },
    "AuditCheckConfiguration" : {
      "description" : "The configuration for a specific audit check.",
      "type" : "object",
      "properties" : {
        "Enabled" : {
          "description" : "True if the check is enabled.",
          "type" : "boolean"
        }
      },
      "additionalProperties" : False
    },
    "DeviceCertAgeAuditCheckConfiguration" : {
      "description" : "A structure containing the configName and corresponding configValue for configuring DeviceCertAgeCheck.",
      "type" : "object",
      "properties" : {
        "Enabled" : {
          "description" : "True if the check is enabled.",
          "type" : "boolean"
        },
        "Configuration" : {
          "$ref" : "#/definitions/CertAgeCheckCustomConfiguration"
        }
      },
      "additionalProperties" : False
    },
    "DeviceCertExpirationAuditCheckConfiguration" : {
      "description" : "A structure containing the configName and corresponding configValue for configuring DeviceCertExpirationCheck.",
      "type" : "object",
      "properties" : {
        "Enabled" : {
          "description" : "True if the check is enabled.",
          "type" : "boolean"
        },
        "Configuration" : {
          "$ref" : "#/definitions/CertExpirationCheckCustomConfiguration"
        }
      },
      "additionalProperties" : False
    },
    "AuditNotificationTarget" : {
      "type" : "object",
      "properties" : {
        "TargetArn" : {
          "description" : "The ARN of the target (SNS topic) to which audit notifications are sent.",
          "type" : "string",
          "maxLength" : 2048
        },
        "RoleArn" : {
          "description" : "The ARN of the role that grants permission to send notifications to the target.",
          "type" : "string",
          "minLength" : 20,
          "maxLength" : 2048
        },
        "Enabled" : {
          "description" : "True if notifications to the target are enabled.",
          "type" : "boolean"
        }
      },
      "additionalProperties" : False
    },
    "ConfigValue" : {
      "type" : "string",
      "description" : "The configValue for configuring audit checks.",
      "minLength" : 1,
      "maxLength" : 64
    },
    "CertAgeCheckCustomConfiguration" : {
      "type" : "object",
      "description" : "A structure containing the configName and corresponding configValue for configuring audit checks.",
      "properties" : {
        "CertAgeThresholdInDays" : {
          "$ref" : "#/definitions/ConfigValue"
        }
      },
      "additionalProperties" : False
    },
    "CertExpirationCheckCustomConfiguration" : {
      "type" : "object",
      "description" : "A structure containing the configName and corresponding configValue for configuring audit checks.",
      "properties" : {
        "CertExpirationThresholdInDays" : {
          "$ref" : "#/definitions/ConfigValue"
        }
      },
      "additionalProperties" : False
    }
  },
  "properties" : {
    "AccountId" : {
      "description" : "Your 12-digit account ID (used as the primary identifier for the CloudFormation resource).",
      "type" : "string",
      "minLength" : 12,
      "maxLength" : 12
    },
    "AuditCheckConfigurations" : {
      "$ref" : "#/definitions/AuditCheckConfigurations"
    },
    "AuditNotificationTargetConfigurations" : {
      "$ref" : "#/definitions/AuditNotificationTargetConfigurations"
    },
    "RoleArn" : {
      "description" : "The ARN of the role that grants permission to AWS IoT to access information about your devices, policies, certificates and other items as required when performing an audit.",
      "type" : "string",
      "minLength" : 20,
      "maxLength" : 2048
    }
  },
  "tagging" : {
    "taggable" : False
  },
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/AccountId" ],
  "required" : [ "AccountId", "AuditCheckConfigurations", "RoleArn" ],
  "createOnlyProperties" : [ "/properties/AccountId" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iot:UpdateAccountAuditConfiguration", "iot:DescribeAccountAuditConfiguration", "iam:PassRole" ]
    },
    "read" : {
      "permissions" : [ "iot:DescribeAccountAuditConfiguration" ]
    },
    "update" : {
      "permissions" : [ "iot:UpdateAccountAuditConfiguration", "iot:DescribeAccountAuditConfiguration", "iam:PassRole" ]
    },
    "delete" : {
      "permissions" : [ "iot:DescribeAccountAuditConfiguration", "iot:DeleteAccountAuditConfiguration" ]
    },
    "list" : {
      "permissions" : [ "iot:DescribeAccountAuditConfiguration" ]
    }
  }
}