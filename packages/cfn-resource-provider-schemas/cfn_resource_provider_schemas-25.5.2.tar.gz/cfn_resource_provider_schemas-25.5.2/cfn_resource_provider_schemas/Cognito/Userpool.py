SCHEMA = {
  "typeName" : "AWS::Cognito::UserPool",
  "description" : "Definition of AWS::Cognito::UserPool Resource Type",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/UserPoolTags",
    "permissions" : [ "cognito-idp:ListTagsForResource", "cognito-idp:UntagResource", "cognito-idp:TagResource" ]
  },
  "definitions" : {
    "PasswordPolicy" : {
      "type" : "object",
      "properties" : {
        "MinimumLength" : {
          "type" : "integer"
        },
        "RequireLowercase" : {
          "type" : "boolean"
        },
        "RequireNumbers" : {
          "type" : "boolean"
        },
        "RequireSymbols" : {
          "type" : "boolean"
        },
        "RequireUppercase" : {
          "type" : "boolean"
        },
        "TemporaryPasswordValidityDays" : {
          "type" : "integer"
        },
        "PasswordHistorySize" : {
          "type" : "integer"
        }
      },
      "additionalProperties" : False
    },
    "SignInPolicy" : {
      "type" : "object",
      "properties" : {
        "AllowedFirstAuthFactors" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        }
      },
      "additionalProperties" : False
    },
    "Policies" : {
      "type" : "object",
      "properties" : {
        "PasswordPolicy" : {
          "$ref" : "#/definitions/PasswordPolicy"
        },
        "SignInPolicy" : {
          "$ref" : "#/definitions/SignInPolicy"
        }
      },
      "additionalProperties" : False
    },
    "InviteMessageTemplate" : {
      "type" : "object",
      "properties" : {
        "EmailMessage" : {
          "type" : "string"
        },
        "EmailSubject" : {
          "type" : "string"
        },
        "SMSMessage" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "RecoveryOption" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "type" : "string"
        },
        "Priority" : {
          "type" : "integer"
        }
      },
      "additionalProperties" : False
    },
    "AccountRecoverySetting" : {
      "type" : "object",
      "properties" : {
        "RecoveryMechanisms" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/RecoveryOption"
          }
        }
      },
      "additionalProperties" : False
    },
    "AdminCreateUserConfig" : {
      "type" : "object",
      "properties" : {
        "AllowAdminCreateUserOnly" : {
          "type" : "boolean"
        },
        "InviteMessageTemplate" : {
          "$ref" : "#/definitions/InviteMessageTemplate"
        },
        "UnusedAccountValidityDays" : {
          "type" : "integer"
        }
      },
      "additionalProperties" : False
    },
    "DeviceConfiguration" : {
      "type" : "object",
      "properties" : {
        "ChallengeRequiredOnNewDevice" : {
          "type" : "boolean"
        },
        "DeviceOnlyRememberedOnUserPrompt" : {
          "type" : "boolean"
        }
      },
      "additionalProperties" : False
    },
    "EmailConfiguration" : {
      "type" : "object",
      "properties" : {
        "ReplyToEmailAddress" : {
          "type" : "string"
        },
        "SourceArn" : {
          "type" : "string"
        },
        "From" : {
          "type" : "string"
        },
        "ConfigurationSet" : {
          "type" : "string"
        },
        "EmailSendingAccount" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "CustomEmailSender" : {
      "type" : "object",
      "properties" : {
        "LambdaVersion" : {
          "type" : "string"
        },
        "LambdaArn" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "CustomSMSSender" : {
      "type" : "object",
      "properties" : {
        "LambdaVersion" : {
          "type" : "string"
        },
        "LambdaArn" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "PreTokenGenerationConfig" : {
      "type" : "object",
      "properties" : {
        "LambdaVersion" : {
          "type" : "string"
        },
        "LambdaArn" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "LambdaConfig" : {
      "type" : "object",
      "properties" : {
        "CreateAuthChallenge" : {
          "type" : "string"
        },
        "CustomMessage" : {
          "type" : "string"
        },
        "DefineAuthChallenge" : {
          "type" : "string"
        },
        "PostAuthentication" : {
          "type" : "string"
        },
        "PostConfirmation" : {
          "type" : "string"
        },
        "PreAuthentication" : {
          "type" : "string"
        },
        "PreSignUp" : {
          "type" : "string"
        },
        "VerifyAuthChallengeResponse" : {
          "type" : "string"
        },
        "UserMigration" : {
          "type" : "string"
        },
        "PreTokenGeneration" : {
          "type" : "string"
        },
        "CustomEmailSender" : {
          "$ref" : "#/definitions/CustomEmailSender"
        },
        "CustomSMSSender" : {
          "$ref" : "#/definitions/CustomSMSSender"
        },
        "KMSKeyID" : {
          "type" : "string"
        },
        "PreTokenGenerationConfig" : {
          "$ref" : "#/definitions/PreTokenGenerationConfig"
        }
      },
      "additionalProperties" : False
    },
    "SmsConfiguration" : {
      "type" : "object",
      "properties" : {
        "ExternalId" : {
          "type" : "string"
        },
        "SnsCallerArn" : {
          "type" : "string"
        },
        "SnsRegion" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "StringAttributeConstraints" : {
      "type" : "object",
      "properties" : {
        "MaxLength" : {
          "type" : "string"
        },
        "MinLength" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "NumberAttributeConstraints" : {
      "type" : "object",
      "properties" : {
        "MaxValue" : {
          "type" : "string"
        },
        "MinValue" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "SchemaAttribute" : {
      "type" : "object",
      "properties" : {
        "AttributeDataType" : {
          "type" : "string"
        },
        "DeveloperOnlyAttribute" : {
          "type" : "boolean"
        },
        "Mutable" : {
          "type" : "boolean"
        },
        "Name" : {
          "type" : "string"
        },
        "NumberAttributeConstraints" : {
          "$ref" : "#/definitions/NumberAttributeConstraints"
        },
        "StringAttributeConstraints" : {
          "$ref" : "#/definitions/StringAttributeConstraints"
        },
        "Required" : {
          "type" : "boolean"
        }
      },
      "additionalProperties" : False
    },
    "UsernameConfiguration" : {
      "type" : "object",
      "properties" : {
        "CaseSensitive" : {
          "type" : "boolean"
        }
      },
      "additionalProperties" : False
    },
    "UserAttributeUpdateSettings" : {
      "type" : "object",
      "properties" : {
        "AttributesRequireVerificationBeforeUpdate" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "AttributesRequireVerificationBeforeUpdate" ],
      "additionalProperties" : False
    },
    "VerificationMessageTemplate" : {
      "type" : "object",
      "properties" : {
        "DefaultEmailOption" : {
          "type" : "string"
        },
        "EmailMessage" : {
          "type" : "string"
        },
        "EmailMessageByLink" : {
          "type" : "string"
        },
        "EmailSubject" : {
          "type" : "string"
        },
        "EmailSubjectByLink" : {
          "type" : "string"
        },
        "SmsMessage" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "AdvancedSecurityAdditionalFlows" : {
      "type" : "object",
      "properties" : {
        "CustomAuthMode" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "UserPoolAddOns" : {
      "type" : "object",
      "properties" : {
        "AdvancedSecurityMode" : {
          "type" : "string"
        },
        "AdvancedSecurityAdditionalFlows" : {
          "$ref" : "#/definitions/AdvancedSecurityAdditionalFlows"
        }
      },
      "additionalProperties" : False
    }
  },
  "properties" : {
    "UserPoolName" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 128
    },
    "Policies" : {
      "$ref" : "#/definitions/Policies"
    },
    "AccountRecoverySetting" : {
      "$ref" : "#/definitions/AccountRecoverySetting"
    },
    "AdminCreateUserConfig" : {
      "$ref" : "#/definitions/AdminCreateUserConfig"
    },
    "AliasAttributes" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "UsernameAttributes" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "AutoVerifiedAttributes" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "DeviceConfiguration" : {
      "$ref" : "#/definitions/DeviceConfiguration"
    },
    "EmailConfiguration" : {
      "$ref" : "#/definitions/EmailConfiguration"
    },
    "EmailVerificationMessage" : {
      "type" : "string",
      "minLength" : 6,
      "maxLength" : 20000
    },
    "EmailVerificationSubject" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 140
    },
    "DeletionProtection" : {
      "type" : "string"
    },
    "LambdaConfig" : {
      "$ref" : "#/definitions/LambdaConfig"
    },
    "MfaConfiguration" : {
      "type" : "string"
    },
    "EnabledMfas" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "SmsAuthenticationMessage" : {
      "type" : "string",
      "minLength" : 6,
      "maxLength" : 140
    },
    "EmailAuthenticationMessage" : {
      "type" : "string",
      "minLength" : 6,
      "maxLength" : 20000
    },
    "EmailAuthenticationSubject" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 140
    },
    "SmsConfiguration" : {
      "$ref" : "#/definitions/SmsConfiguration"
    },
    "SmsVerificationMessage" : {
      "type" : "string",
      "minLength" : 6,
      "maxLength" : 140
    },
    "WebAuthnRelyingPartyID" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 63
    },
    "WebAuthnUserVerification" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 9
    },
    "Schema" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/SchemaAttribute"
      }
    },
    "UsernameConfiguration" : {
      "$ref" : "#/definitions/UsernameConfiguration"
    },
    "UserAttributeUpdateSettings" : {
      "$ref" : "#/definitions/UserAttributeUpdateSettings"
    },
    "UserPoolTags" : {
      "type" : "object",
      "patternProperties" : {
        "^([\\p{L}\\p{Z}\\p{N}_.:/=+\\-@]*)$" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "VerificationMessageTemplate" : {
      "$ref" : "#/definitions/VerificationMessageTemplate"
    },
    "UserPoolAddOns" : {
      "$ref" : "#/definitions/UserPoolAddOns"
    },
    "ProviderName" : {
      "type" : "string"
    },
    "ProviderURL" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "UserPoolId" : {
      "type" : "string"
    },
    "UserPoolTier" : {
      "type" : "string",
      "enum" : [ "LITE", "ESSENTIALS", "PLUS" ]
    }
  },
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/UserPoolId" ],
  "readOnlyProperties" : [ "/properties/ProviderName", "/properties/UserPoolId", "/properties/ProviderURL", "/properties/Arn" ],
  "writeOnlyProperties" : [ "/properties/EnabledMfas" ],
  "propertyTransform" : {
    "/properties/Schema/*/Name" : "'custom:' & '' & Name"
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "cognito-idp:CreateUserPool", "iam:PassRole", "cognito-idp:SetUserPoolMfaConfig", "cognito-idp:DescribeUserPool", "kms:CreateGrant", "iam:CreateServiceLinkedRole", "cognito-idp:TagResource" ],
      "timeoutInMinutes" : 2
    },
    "read" : {
      "permissions" : [ "cognito-idp:DescribeUserPool", "cognito-idp:GetUserPoolMfaConfig" ]
    },
    "update" : {
      "permissions" : [ "cognito-idp:UpdateUserPool", "cognito-idp:ListTagsForResource", "cognito-idp:UntagResource", "cognito-idp:TagResource", "cognito-idp:SetUserPoolMfaConfig", "cognito-idp:AddCustomAttributes", "cognito-idp:DescribeUserPool", "cognito-idp:GetUserPoolMfaConfig", "iam:PassRole" ],
      "timeoutInMinutes" : 2
    },
    "delete" : {
      "permissions" : [ "cognito-idp:DeleteUserPool" ],
      "timeoutInMinutes" : 2
    },
    "list" : {
      "permissions" : [ "cognito-idp:ListUserPools" ]
    }
  }
}