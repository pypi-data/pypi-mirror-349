SCHEMA = {
  "propertyTransform" : {
    "/properties/AutoScalingGroupProvider/AutoScalingGroupArn" : "$split(AutoScalingGroupProvider.AutoScalingGroupArn, \"autoScalingGroupName/\")[-1] $OR $split(AutoScalingGroupArn, \"autoScalingGroupName/\")[-1]"
  },
  "tagging" : {
    "permissions" : [ "ecs:TagResource", "ecs:UntagResource", "ecs:ListTagsForResource" ],
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "tagProperty" : "/properties/Tags",
    "cloudFormationSystemTags" : True
  },
  "handlers" : {
    "read" : {
      "permissions" : [ "ecs:DescribeCapacityProviders" ]
    },
    "create" : {
      "permissions" : [ "autoscaling:CreateOrUpdateTags", "ecs:CreateCapacityProvider", "ecs:DescribeCapacityProviders", "ecs:TagResource" ]
    },
    "update" : {
      "permissions" : [ "ecs:UpdateCapacityProvider", "ecs:DescribeCapacityProviders", "ecs:ListTagsForResource", "ecs:TagResource", "ecs:UntagResource" ]
    },
    "list" : {
      "permissions" : [ "ecs:DescribeCapacityProviders" ]
    },
    "delete" : {
      "permissions" : [ "ecs:DescribeCapacityProviders", "ecs:DeleteCapacityProvider" ]
    }
  },
  "typeName" : "AWS::ECS::CapacityProvider",
  "description" : "Resource Type definition for AWS::ECS::CapacityProvider.",
  "createOnlyProperties" : [ "/properties/AutoScalingGroupProvider/AutoScalingGroupArn", "/properties/Name" ],
  "additionalProperties" : False,
  "primaryIdentifier" : [ "/properties/Name" ],
  "definitions" : {
    "AutoScalingGroupProvider" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "ManagedScaling" : {
          "$ref" : "#/definitions/ManagedScaling"
        },
        "AutoScalingGroupArn" : {
          "type" : "string"
        },
        "ManagedTerminationProtection" : {
          "type" : "string",
          "enum" : [ "DISABLED", "ENABLED" ]
        },
        "ManagedDraining" : {
          "type" : "string",
          "enum" : [ "DISABLED", "ENABLED" ]
        }
      },
      "required" : [ "AutoScalingGroupArn" ]
    },
    "ManagedScaling" : {
      "description" : "The managed scaling settings for the Auto Scaling group capacity provider.",
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Status" : {
          "type" : "string",
          "enum" : [ "DISABLED", "ENABLED" ]
        },
        "MinimumScalingStepSize" : {
          "type" : "integer"
        },
        "InstanceWarmupPeriod" : {
          "type" : "integer"
        },
        "TargetCapacity" : {
          "type" : "integer"
        },
        "MaximumScalingStepSize" : {
          "type" : "integer"
        }
      }
    },
    "Tag" : {
      "additionalProperties" : False,
      "type" : "object",
      "properties" : {
        "Value" : {
          "minLength" : 1,
          "type" : "string"
        },
        "Key" : {
          "minLength" : 1,
          "type" : "string"
        }
      }
    }
  },
  "properties" : {
    "AutoScalingGroupProvider" : {
      "$ref" : "#/definitions/AutoScalingGroupProvider"
    },
    "Tags" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "Name" : {
      "type" : "string"
    }
  }
}