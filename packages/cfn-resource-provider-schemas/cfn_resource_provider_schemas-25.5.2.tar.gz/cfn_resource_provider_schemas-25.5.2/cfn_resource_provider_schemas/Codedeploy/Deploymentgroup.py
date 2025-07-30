SCHEMA = {
  "typeName" : "AWS::CodeDeploy::DeploymentGroup",
  "description" : "Resource Type definition for AWS::CodeDeploy::DeploymentGroup",
  "additionalProperties" : False,
  "properties" : {
    "OnPremisesTagSet" : {
      "$ref" : "#/definitions/OnPremisesTagSet"
    },
    "ApplicationName" : {
      "type" : "string"
    },
    "DeploymentStyle" : {
      "$ref" : "#/definitions/DeploymentStyle"
    },
    "ServiceRoleArn" : {
      "type" : "string"
    },
    "BlueGreenDeploymentConfiguration" : {
      "$ref" : "#/definitions/BlueGreenDeploymentConfiguration"
    },
    "AutoScalingGroups" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "type" : "string"
      }
    },
    "Ec2TagSet" : {
      "$ref" : "#/definitions/EC2TagSet"
    },
    "OutdatedInstancesStrategy" : {
      "type" : "string"
    },
    "TriggerConfigurations" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/TriggerConfig"
      }
    },
    "Deployment" : {
      "$ref" : "#/definitions/Deployment"
    },
    "DeploymentConfigName" : {
      "type" : "string"
    },
    "AlarmConfiguration" : {
      "$ref" : "#/definitions/AlarmConfiguration"
    },
    "Ec2TagFilters" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/EC2TagFilter"
      }
    },
    "TerminationHookEnabled" : {
      "type" : "boolean"
    },
    "ECSServices" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/ECSService"
      }
    },
    "AutoRollbackConfiguration" : {
      "$ref" : "#/definitions/AutoRollbackConfiguration"
    },
    "LoadBalancerInfo" : {
      "$ref" : "#/definitions/LoadBalancerInfo"
    },
    "Id" : {
      "type" : "string"
    },
    "DeploymentGroupName" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "OnPremisesInstanceTagFilters" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/TagFilter"
      }
    }
  },
  "definitions" : {
    "OnPremisesTagSet" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OnPremisesTagSetList" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/OnPremisesTagSetListObject"
          }
        }
      }
    },
    "DeploymentStyle" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DeploymentOption" : {
          "type" : "string"
        },
        "DeploymentType" : {
          "type" : "string"
        }
      }
    },
    "BlueGreenDeploymentConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "GreenFleetProvisioningOption" : {
          "$ref" : "#/definitions/GreenFleetProvisioningOption"
        },
        "DeploymentReadyOption" : {
          "$ref" : "#/definitions/DeploymentReadyOption"
        },
        "TerminateBlueInstancesOnDeploymentSuccess" : {
          "$ref" : "#/definitions/BlueInstanceTerminationOption"
        }
      }
    },
    "TagFilter" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Type" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      }
    },
    "TriggerConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TriggerTargetArn" : {
          "type" : "string"
        },
        "TriggerName" : {
          "type" : "string"
        },
        "TriggerEvents" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "GitHubLocation" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Repository" : {
          "type" : "string"
        },
        "CommitId" : {
          "type" : "string"
        }
      },
      "required" : [ "Repository", "CommitId" ]
    },
    "Deployment" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Description" : {
          "type" : "string"
        },
        "Revision" : {
          "$ref" : "#/definitions/RevisionLocation"
        },
        "IgnoreApplicationStopFailures" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Revision" ]
    },
    "ELBInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        }
      }
    },
    "EC2TagSetListObject" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Ec2TagGroup" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/EC2TagFilter"
          }
        }
      }
    },
    "S3Location" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "BundleType" : {
          "type" : "string"
        },
        "Bucket" : {
          "type" : "string"
        },
        "ETag" : {
          "type" : "string"
        },
        "Version" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      },
      "required" : [ "Bucket", "Key" ]
    },
    "AutoRollbackConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Events" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        },
        "Enabled" : {
          "type" : "boolean"
        }
      }
    },
    "DeploymentReadyOption" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "WaitTimeInMinutes" : {
          "type" : "integer"
        },
        "ActionOnTimeout" : {
          "type" : "string"
        }
      }
    },
    "EC2TagFilter" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Type" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        }
      }
    },
    "RevisionLocation" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "S3Location" : {
          "$ref" : "#/definitions/S3Location"
        },
        "GitHubLocation" : {
          "$ref" : "#/definitions/GitHubLocation"
        },
        "RevisionType" : {
          "type" : "string"
        }
      }
    },
    "GreenFleetProvisioningOption" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Action" : {
          "type" : "string"
        }
      }
    },
    "LoadBalancerInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TargetGroupInfoList" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/TargetGroupInfo"
          }
        },
        "ElbInfoList" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/ELBInfo"
          }
        },
        "TargetGroupPairInfoList" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/TargetGroupPairInfo"
          }
        }
      }
    },
    "AlarmConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Alarms" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/Alarm"
          }
        },
        "IgnorePollAlarmFailure" : {
          "type" : "boolean"
        },
        "Enabled" : {
          "type" : "boolean"
        }
      }
    },
    "EC2TagSet" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Ec2TagSetList" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/EC2TagSetListObject"
          }
        }
      }
    },
    "TrafficRoute" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ListenerArns" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "ECSService" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ServiceName" : {
          "type" : "string"
        },
        "ClusterName" : {
          "type" : "string"
        }
      },
      "required" : [ "ServiceName", "ClusterName" ]
    },
    "TargetGroupPairInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ProdTrafficRoute" : {
          "$ref" : "#/definitions/TrafficRoute"
        },
        "TestTrafficRoute" : {
          "$ref" : "#/definitions/TrafficRoute"
        },
        "TargetGroups" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/TargetGroupInfo"
          }
        }
      }
    },
    "Alarm" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        }
      }
    },
    "TargetGroupInfo" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Name" : {
          "type" : "string"
        }
      }
    },
    "OnPremisesTagSetListObject" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "OnPremisesTagGroup" : {
          "type" : "array",
          "uniqueItems" : True,
          "items" : {
            "$ref" : "#/definitions/TagFilter"
          }
        }
      }
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
    "BlueInstanceTerminationOption" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TerminationWaitTimeInMinutes" : {
          "type" : "integer"
        },
        "Action" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "ApplicationName", "ServiceRoleArn" ],
  "createOnlyProperties" : [ "/properties/DeploymentGroupName", "/properties/ApplicationName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}