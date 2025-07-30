SCHEMA = {
  "typeName" : "AWS::GreengrassV2::Deployment",
  "description" : "Resource for Greengrass V2 deployment.",
  "definitions" : {
    "ComponentDeploymentSpecification" : {
      "type" : "object",
      "properties" : {
        "ComponentVersion" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 64
        },
        "ConfigurationUpdate" : {
          "$ref" : "#/definitions/ComponentConfigurationUpdate"
        },
        "RunWith" : {
          "$ref" : "#/definitions/ComponentRunWith"
        }
      },
      "additionalProperties" : False
    },
    "SystemResourceLimits" : {
      "type" : "object",
      "properties" : {
        "Memory" : {
          "type" : "integer",
          "format" : "int64",
          "minimum" : 0,
          "maximum" : 9223372036854771712
        },
        "Cpus" : {
          "type" : "number",
          "minimum" : 0
        }
      },
      "additionalProperties" : False
    },
    "ComponentRunWith" : {
      "type" : "object",
      "properties" : {
        "PosixUser" : {
          "type" : "string",
          "minLength" : 1
        },
        "SystemResourceLimits" : {
          "$ref" : "#/definitions/SystemResourceLimits"
        },
        "WindowsUser" : {
          "type" : "string",
          "minLength" : 1
        }
      },
      "additionalProperties" : False
    },
    "ComponentConfigurationUpdate" : {
      "type" : "object",
      "properties" : {
        "Merge" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 10485760
        },
        "Reset" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "minLength" : 0,
            "maxLength" : 256
          },
          "insertionOrder" : False
        }
      },
      "additionalProperties" : False
    },
    "DeploymentIoTJobConfiguration" : {
      "type" : "object",
      "properties" : {
        "JobExecutionsRolloutConfig" : {
          "$ref" : "#/definitions/IoTJobExecutionsRolloutConfig"
        },
        "AbortConfig" : {
          "$ref" : "#/definitions/IoTJobAbortConfig"
        },
        "TimeoutConfig" : {
          "$ref" : "#/definitions/IoTJobTimeoutConfig"
        }
      },
      "additionalProperties" : False
    },
    "IoTJobExecutionsRolloutConfig" : {
      "type" : "object",
      "properties" : {
        "ExponentialRate" : {
          "$ref" : "#/definitions/IoTJobExponentialRolloutRate"
        },
        "MaximumPerMinute" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 1000
        }
      },
      "additionalProperties" : False
    },
    "IoTJobAbortConfig" : {
      "type" : "object",
      "properties" : {
        "CriteriaList" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/IoTJobAbortCriteria"
          },
          "minItems" : 1,
          "insertionOrder" : False
        }
      },
      "required" : [ "CriteriaList" ],
      "additionalProperties" : False
    },
    "IoTJobAbortCriteria" : {
      "type" : "object",
      "properties" : {
        "FailureType" : {
          "type" : "string",
          "enum" : [ "FAILED", "REJECTED", "TIMED_OUT", "ALL" ]
        },
        "Action" : {
          "type" : "string",
          "enum" : [ "CANCEL" ]
        },
        "ThresholdPercentage" : {
          "type" : "number",
          "minimum" : 0,
          "maximum" : 100
        },
        "MinNumberOfExecutedThings" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 2147483647
        }
      },
      "required" : [ "FailureType", "Action", "ThresholdPercentage", "MinNumberOfExecutedThings" ],
      "additionalProperties" : False
    },
    "IoTJobTimeoutConfig" : {
      "type" : "object",
      "properties" : {
        "InProgressTimeoutInMinutes" : {
          "type" : "integer",
          "minimum" : 0,
          "maximum" : 2147483647
        }
      },
      "additionalProperties" : False
    },
    "IoTJobExponentialRolloutRate" : {
      "type" : "object",
      "properties" : {
        "BaseRatePerMinute" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 1000
        },
        "IncrementFactor" : {
          "type" : "number",
          "minimum" : 1,
          "maximum" : 5
        },
        "RateIncreaseCriteria" : {
          "$ref" : "#/definitions/IoTJobRateIncreaseCriteria"
        }
      },
      "required" : [ "BaseRatePerMinute", "IncrementFactor", "RateIncreaseCriteria" ],
      "additionalProperties" : False
    },
    "IoTJobRateIncreaseCriteria" : {
      "type" : "object",
      "oneOf" : [ {
        "type" : "object",
        "additionalProperties" : False,
        "properties" : {
          "NumberOfNotifiedThings" : {
            "$ref" : "#/definitions/NumberOfThings"
          }
        }
      }, {
        "type" : "object",
        "additionalProperties" : False,
        "properties" : {
          "NumberOfSucceededThings" : {
            "$ref" : "#/definitions/NumberOfThings"
          }
        }
      } ]
    },
    "NumberOfThings" : {
      "type" : "integer",
      "minimum" : 1,
      "maximum" : 2147483647
    },
    "DeploymentPolicies" : {
      "type" : "object",
      "properties" : {
        "FailureHandlingPolicy" : {
          "type" : "string",
          "enum" : [ "ROLLBACK", "DO_NOTHING" ]
        },
        "ComponentUpdatePolicy" : {
          "$ref" : "#/definitions/DeploymentComponentUpdatePolicy"
        },
        "ConfigurationValidationPolicy" : {
          "$ref" : "#/definitions/DeploymentConfigurationValidationPolicy"
        }
      },
      "additionalProperties" : False
    },
    "DeploymentComponentUpdatePolicy" : {
      "type" : "object",
      "properties" : {
        "TimeoutInSeconds" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 2147483647
        },
        "Action" : {
          "type" : "string",
          "enum" : [ "NOTIFY_COMPONENTS", "SKIP_NOTIFY_COMPONENTS" ]
        }
      },
      "additionalProperties" : False
    },
    "DeploymentConfigurationValidationPolicy" : {
      "type" : "object",
      "properties" : {
        "TimeoutInSeconds" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 2147483647
        }
      },
      "additionalProperties" : False
    }
  },
  "properties" : {
    "TargetArn" : {
      "type" : "string",
      "pattern" : "arn:[^:]*:iot:[^:]*:[0-9]+:(thing|thinggroup)/.+"
    },
    "ParentTargetArn" : {
      "type" : "string",
      "pattern" : "arn:[^:]*:iot:[^:]*:[0-9]+:thinggroup/.+"
    },
    "DeploymentId" : {
      "type" : "string",
      "pattern" : ".+"
    },
    "DeploymentName" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 256
    },
    "Components" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "$ref" : "#/definitions/ComponentDeploymentSpecification"
        }
      },
      "additionalProperties" : False
    },
    "IotJobConfiguration" : {
      "$ref" : "#/definitions/DeploymentIoTJobConfiguration"
    },
    "DeploymentPolicies" : {
      "$ref" : "#/definitions/DeploymentPolicies"
    },
    "Tags" : {
      "type" : "object",
      "patternProperties" : {
        ".*" : {
          "type" : "string",
          "maxLength" : 256
        }
      },
      "maxProperties" : 200,
      "additionalProperties" : False
    }
  },
  "required" : [ "TargetArn" ],
  "primaryIdentifier" : [ "/properties/DeploymentId" ],
  "additionalProperties" : False,
  "readOnlyProperties" : [ "/properties/DeploymentId" ],
  "createOnlyProperties" : [ "/properties/TargetArn", "/properties/ParentTargetArn", "/properties/DeploymentName", "/properties/Components", "/properties/IotJobConfiguration", "/properties/DeploymentPolicies" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "greengrass:CreateDeployment", "greengrass:GetDeployment", "greengrass:TagResource", "iot:CancelJob", "iot:CreateJob", "iot:DeleteThingShadow", "iot:DescribeJob", "iot:DescribeThing", "iot:DescribeThingGroup", "iot:GetThingShadow", "iot:UpdateJob", "iot:UpdateThingShadow" ]
    },
    "read" : {
      "permissions" : [ "greengrass:GetDeployment", "iot:DescribeJob", "iot:DescribeThing", "iot:DescribeThingGroup", "iot:GetThingShadow" ]
    },
    "update" : {
      "permissions" : [ "greengrass:GetDeployment", "greengrass:TagResource", "greengrass:UntagResource", "iot:DescribeJob" ]
    },
    "delete" : {
      "permissions" : [ "greengrass:DeleteDeployment", "greengrass:CancelDeployment", "iot:CancelJob", "iot:DeleteJob", "iot:DescribeJob" ]
    },
    "list" : {
      "permissions" : [ "greengrass:ListDeployments", "iot:DescribeJob", "iot:DescribeThing", "iot:DescribeThingGroup", "iot:GetThingShadow" ]
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags"
  }
}