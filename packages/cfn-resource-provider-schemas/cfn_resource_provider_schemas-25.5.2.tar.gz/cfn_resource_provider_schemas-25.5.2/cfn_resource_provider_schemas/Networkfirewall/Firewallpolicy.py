SCHEMA = {
  "typeName" : "AWS::NetworkFirewall::FirewallPolicy",
  "description" : "Resource type definition for AWS::NetworkFirewall::FirewallPolicy",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-networkfirewall.git",
  "additionalProperties" : False,
  "definitions" : {
    "ResourceArn" : {
      "description" : "A resource ARN.",
      "type" : "string",
      "pattern" : "^(arn:aws.*)$",
      "minLength" : 1,
      "maxLength" : 256
    },
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128,
          "pattern" : "^.*$"
        },
        "Value" : {
          "type" : "string",
          "minLength" : 0,
          "maxLength" : 255,
          "pattern" : "^.*$"
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    },
    "FirewallPolicy" : {
      "type" : "object",
      "properties" : {
        "StatelessDefaultActions" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "StatelessFragmentDefaultActions" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "StatelessCustomActions" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/CustomAction"
          }
        },
        "StatelessRuleGroupReferences" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/StatelessRuleGroupReference"
          }
        },
        "StatefulRuleGroupReferences" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/StatefulRuleGroupReference"
          }
        },
        "StatefulDefaultActions" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "StatefulEngineOptions" : {
          "$ref" : "#/definitions/StatefulEngineOptions"
        },
        "PolicyVariables" : {
          "type" : "object",
          "properties" : {
            "RuleVariables" : {
              "$ref" : "#/definitions/RuleVariables"
            }
          },
          "additionalProperties" : False
        },
        "TLSInspectionConfigurationArn" : {
          "$ref" : "#/definitions/ResourceArn"
        }
      },
      "required" : [ "StatelessDefaultActions", "StatelessFragmentDefaultActions" ],
      "additionalProperties" : False
    },
    "RuleVariables" : {
      "type" : "object",
      "patternProperties" : {
        "^[A-Za-z0-9_]{1,32}$" : {
          "$ref" : "#/definitions/IPSet"
        }
      },
      "additionalProperties" : False
    },
    "CustomAction" : {
      "type" : "object",
      "properties" : {
        "ActionName" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128,
          "pattern" : "^[a-zA-Z0-9]+$"
        },
        "ActionDefinition" : {
          "$ref" : "#/definitions/ActionDefinition"
        }
      },
      "required" : [ "ActionName", "ActionDefinition" ],
      "additionalProperties" : False
    },
    "ActionDefinition" : {
      "type" : "object",
      "properties" : {
        "PublishMetricAction" : {
          "$ref" : "#/definitions/PublishMetricAction"
        }
      },
      "additionalProperties" : False
    },
    "PublishMetricAction" : {
      "type" : "object",
      "properties" : {
        "Dimensions" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Dimension"
          }
        }
      },
      "required" : [ "Dimensions" ],
      "additionalProperties" : False
    },
    "Dimension" : {
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128,
          "pattern" : "^[a-zA-Z0-9-_ ]+$"
        }
      },
      "required" : [ "Value" ],
      "additionalProperties" : False
    },
    "StatefulRuleGroupReference" : {
      "type" : "object",
      "properties" : {
        "ResourceArn" : {
          "$ref" : "#/definitions/ResourceArn"
        },
        "Priority" : {
          "$ref" : "#/definitions/Priority"
        },
        "Override" : {
          "$ref" : "#/definitions/StatefulRuleGroupOverride"
        }
      },
      "required" : [ "ResourceArn" ],
      "additionalProperties" : False
    },
    "StatelessRuleGroupReference" : {
      "type" : "object",
      "properties" : {
        "ResourceArn" : {
          "$ref" : "#/definitions/ResourceArn"
        },
        "Priority" : {
          "$ref" : "#/definitions/Priority"
        }
      },
      "required" : [ "ResourceArn", "Priority" ],
      "additionalProperties" : False
    },
    "Priority" : {
      "type" : "integer",
      "minimum" : 1,
      "maximum" : 65535
    },
    "VariableDefinition" : {
      "type" : "string",
      "minLength" : 1,
      "pattern" : "^.*$"
    },
    "IPSet" : {
      "type" : "object",
      "properties" : {
        "Definition" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/VariableDefinition"
          }
        }
      },
      "additionalProperties" : False
    },
    "StatefulRuleGroupOverride" : {
      "type" : "object",
      "properties" : {
        "Action" : {
          "$ref" : "#/definitions/OverrideAction"
        }
      },
      "additionalProperties" : False
    },
    "OverrideAction" : {
      "type" : "string",
      "enum" : [ "DROP_TO_ALERT" ]
    },
    "StatefulEngineOptions" : {
      "type" : "object",
      "properties" : {
        "RuleOrder" : {
          "$ref" : "#/definitions/RuleOrder"
        },
        "StreamExceptionPolicy" : {
          "$ref" : "#/definitions/StreamExceptionPolicy"
        },
        "FlowTimeouts" : {
          "type" : "object",
          "properties" : {
            "TcpIdleTimeoutSeconds" : {
              "type" : "integer",
              "minimum" : 60,
              "maximum" : 6000
            }
          },
          "additionalProperties" : False
        }
      },
      "additionalProperties" : False
    },
    "RuleOrder" : {
      "type" : "string",
      "enum" : [ "DEFAULT_ACTION_ORDER", "STRICT_ORDER" ]
    },
    "StreamExceptionPolicy" : {
      "type" : "string",
      "enum" : [ "DROP", "CONTINUE", "REJECT" ]
    }
  },
  "properties" : {
    "FirewallPolicyName" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 128,
      "pattern" : "^[a-zA-Z0-9-]+$"
    },
    "FirewallPolicyArn" : {
      "$ref" : "#/definitions/ResourceArn"
    },
    "FirewallPolicy" : {
      "$ref" : "#/definitions/FirewallPolicy"
    },
    "FirewallPolicyId" : {
      "type" : "string",
      "minLength" : 36,
      "maxLength" : 36,
      "pattern" : "^([0-9a-f]{8})-([0-9a-f]{4}-){3}([0-9a-f]{12})$"
    },
    "Description" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 512,
      "pattern" : "^.*$"
    },
    "Tags" : {
      "type" : "array",
      "insertionOrder" : False,
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "network-firewall:TagResource", "network-firewall:UntagResource", "network-firewall:ListTagsForResource" ]
  },
  "required" : [ "FirewallPolicyName", "FirewallPolicy" ],
  "readOnlyProperties" : [ "/properties/FirewallPolicyArn", "/properties/FirewallPolicyId" ],
  "primaryIdentifier" : [ "/properties/FirewallPolicyArn" ],
  "createOnlyProperties" : [ "/properties/FirewallPolicyName" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "network-firewall:CreateFirewallPolicy", "network-firewall:DescribeFirewallPolicy", "network-firewall:ListTLSInspectionConfigurations", "network-firewall:TagResource", "network-firewall:ListRuleGroups" ]
    },
    "read" : {
      "permissions" : [ "network-firewall:DescribeFirewallPolicy", "network-firewall:ListTagsForResources" ]
    },
    "update" : {
      "permissions" : [ "network-firewall:UpdateFirewallPolicy", "network-firewall:DescribeFirewallPolicy", "network-firewall:TagResource", "network-firewall:UntagResource", "network-firewall:ListRuleGroups", "network-firewall:ListTLSInspectionConfigurations" ]
    },
    "delete" : {
      "permissions" : [ "network-firewall:DeleteFirewallPolicy", "network-firewall:DescribeFirewallPolicy", "network-firewall:UntagResource" ]
    },
    "list" : {
      "permissions" : [ "network-firewall:ListFirewallPolicies" ]
    }
  }
}