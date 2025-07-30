SCHEMA = {
  "typeName" : "AWS::NetworkFirewall::RuleGroup",
  "description" : "Resource type definition for AWS::NetworkFirewall::RuleGroup",
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
    "RulesString" : {
      "type" : "string",
      "minLength" : 0,
      "maxLength" : 1000000
    },
    "RuleGroup" : {
      "type" : "object",
      "properties" : {
        "RuleVariables" : {
          "$ref" : "#/definitions/RuleVariables"
        },
        "ReferenceSets" : {
          "$ref" : "#/definitions/ReferenceSets"
        },
        "RulesSource" : {
          "$ref" : "#/definitions/RulesSource"
        },
        "StatefulRuleOptions" : {
          "$ref" : "#/definitions/StatefulRuleOptions"
        }
      },
      "required" : [ "RulesSource" ],
      "additionalProperties" : False
    },
    "RuleVariables" : {
      "type" : "object",
      "properties" : {
        "IPSets" : {
          "type" : "object",
          "patternProperties" : {
            "^[A-Za-z0-9_]{1,32}$" : {
              "$ref" : "#/definitions/IPSet"
            }
          },
          "additionalProperties" : False
        },
        "PortSets" : {
          "type" : "object",
          "patternProperties" : {
            "^[A-Za-z0-9_]{1,32}$" : {
              "$ref" : "#/definitions/PortSet"
            }
          },
          "additionalProperties" : False
        }
      },
      "additionalProperties" : False
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
    "PortSet" : {
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
    "VariableDefinition" : {
      "type" : "string",
      "minLength" : 1,
      "pattern" : "^.*$"
    },
    "ReferenceSets" : {
      "type" : "object",
      "properties" : {
        "IPSetReferences" : {
          "type" : "object",
          "patternProperties" : {
            "^[A-Za-z0-9_]{1,32}$" : {
              "$ref" : "#/definitions/IPSetReference"
            }
          },
          "additionalProperties" : False
        }
      },
      "additionalProperties" : False
    },
    "IPSetReference" : {
      "type" : "object",
      "properties" : {
        "ReferenceArn" : {
          "$ref" : "#/definitions/ResourceArn"
        }
      },
      "additionalProperties" : False
    },
    "RulesSource" : {
      "type" : "object",
      "properties" : {
        "RulesString" : {
          "$ref" : "#/definitions/RulesString"
        },
        "RulesSourceList" : {
          "$ref" : "#/definitions/RulesSourceList"
        },
        "StatefulRules" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/StatefulRule"
          }
        },
        "StatelessRulesAndCustomActions" : {
          "$ref" : "#/definitions/StatelessRulesAndCustomActions"
        }
      },
      "additionalProperties" : False
    },
    "RulesSourceList" : {
      "type" : "object",
      "properties" : {
        "Targets" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "TargetTypes" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/TargetType"
          }
        },
        "GeneratedRulesType" : {
          "$ref" : "#/definitions/GeneratedRulesType"
        }
      },
      "required" : [ "Targets", "TargetTypes", "GeneratedRulesType" ],
      "additionalProperties" : False
    },
    "TargetType" : {
      "type" : "string",
      "enum" : [ "TLS_SNI", "HTTP_HOST" ]
    },
    "GeneratedRulesType" : {
      "type" : "string",
      "enum" : [ "ALLOWLIST", "DENYLIST" ]
    },
    "StatefulRule" : {
      "type" : "object",
      "properties" : {
        "Action" : {
          "type" : "string",
          "enum" : [ "PASS", "DROP", "ALERT", "REJECT" ]
        },
        "Header" : {
          "$ref" : "#/definitions/Header"
        },
        "RuleOptions" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/RuleOption"
          }
        }
      },
      "required" : [ "Action", "Header", "RuleOptions" ],
      "additionalProperties" : False
    },
    "Header" : {
      "type" : "object",
      "properties" : {
        "Protocol" : {
          "type" : "string",
          "enum" : [ "IP", "TCP", "UDP", "ICMP", "HTTP", "FTP", "TLS", "SMB", "DNS", "DCERPC", "SSH", "SMTP", "IMAP", "MSN", "KRB5", "IKEV2", "TFTP", "NTP", "DHCP" ]
        },
        "Source" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 1024,
          "pattern" : "^.*$"
        },
        "SourcePort" : {
          "$ref" : "#/definitions/Port"
        },
        "Direction" : {
          "type" : "string",
          "enum" : [ "FORWARD", "ANY" ]
        },
        "Destination" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 1024,
          "pattern" : "^.*$"
        },
        "DestinationPort" : {
          "$ref" : "#/definitions/Port"
        }
      },
      "required" : [ "Protocol", "Source", "SourcePort", "Direction", "Destination", "DestinationPort" ],
      "additionalProperties" : False
    },
    "RuleOption" : {
      "type" : "object",
      "properties" : {
        "Keyword" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128,
          "pattern" : "^.*$"
        },
        "Settings" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Setting"
          }
        }
      },
      "required" : [ "Keyword" ],
      "additionalProperties" : False
    },
    "Setting" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 8192,
      "pattern" : "^.*$"
    },
    "Port" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 1024,
      "pattern" : "^.*$"
    },
    "StatelessRulesAndCustomActions" : {
      "type" : "object",
      "properties" : {
        "StatelessRules" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/StatelessRule"
          }
        },
        "CustomActions" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/CustomAction"
          }
        }
      },
      "required" : [ "StatelessRules" ],
      "additionalProperties" : False
    },
    "StatelessRule" : {
      "type" : "object",
      "properties" : {
        "RuleDefinition" : {
          "$ref" : "#/definitions/RuleDefinition"
        },
        "Priority" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 65535
        }
      },
      "required" : [ "RuleDefinition", "Priority" ],
      "additionalProperties" : False
    },
    "RuleDefinition" : {
      "type" : "object",
      "properties" : {
        "MatchAttributes" : {
          "$ref" : "#/definitions/MatchAttributes"
        },
        "Actions" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "MatchAttributes", "Actions" ],
      "additionalProperties" : False
    },
    "MatchAttributes" : {
      "type" : "object",
      "properties" : {
        "Sources" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Address"
          }
        },
        "Destinations" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Address"
          }
        },
        "SourcePorts" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/PortRange"
          }
        },
        "DestinationPorts" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/PortRange"
          }
        },
        "Protocols" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/ProtocolNumber"
          }
        },
        "TCPFlags" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/TCPFlagField"
          }
        }
      },
      "additionalProperties" : False
    },
    "Address" : {
      "type" : "object",
      "properties" : {
        "AddressDefinition" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 255,
          "pattern" : "^([a-fA-F\\d:\\.]+/\\d{1,3})$"
        }
      },
      "required" : [ "AddressDefinition" ],
      "additionalProperties" : False
    },
    "PortRange" : {
      "type" : "object",
      "properties" : {
        "FromPort" : {
          "$ref" : "#/definitions/PortRangeBound"
        },
        "ToPort" : {
          "$ref" : "#/definitions/PortRangeBound"
        }
      },
      "required" : [ "FromPort", "ToPort" ],
      "additionalProperties" : False
    },
    "PortRangeBound" : {
      "type" : "integer",
      "minimum" : 0,
      "maximum" : 65535
    },
    "ProtocolNumber" : {
      "type" : "integer",
      "minimum" : 0,
      "maximum" : 255
    },
    "TCPFlagField" : {
      "type" : "object",
      "properties" : {
        "Flags" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/TCPFlag"
          }
        },
        "Masks" : {
          "type" : "array",
          "insertionOrder" : True,
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/TCPFlag"
          }
        }
      },
      "required" : [ "Flags" ],
      "additionalProperties" : False
    },
    "TCPFlag" : {
      "type" : "string",
      "enum" : [ "FIN", "SYN", "RST", "PSH", "ACK", "URG", "ECE", "CWR" ]
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
    "StatefulRuleOptions" : {
      "type" : "object",
      "properties" : {
        "RuleOrder" : {
          "$ref" : "#/definitions/RuleOrder"
        }
      },
      "additionalProperties" : False
    },
    "RuleOrder" : {
      "type" : "string",
      "enum" : [ "DEFAULT_ACTION_ORDER", "STRICT_ORDER" ]
    }
  },
  "properties" : {
    "RuleGroupName" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 128,
      "pattern" : "^[a-zA-Z0-9-]+$"
    },
    "RuleGroupArn" : {
      "$ref" : "#/definitions/ResourceArn"
    },
    "RuleGroupId" : {
      "type" : "string",
      "minLength" : 36,
      "maxLength" : 36,
      "pattern" : "^([0-9a-f]{8})-([0-9a-f]{4}-){3}([0-9a-f]{12})$"
    },
    "RuleGroup" : {
      "$ref" : "#/definitions/RuleGroup"
    },
    "Type" : {
      "type" : "string",
      "enum" : [ "STATELESS", "STATEFUL" ]
    },
    "Capacity" : {
      "type" : "integer"
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
  "required" : [ "Type", "Capacity", "RuleGroupName" ],
  "readOnlyProperties" : [ "/properties/RuleGroupArn", "/properties/RuleGroupId" ],
  "createOnlyProperties" : [ "/properties/RuleGroupName", "/properties/Capacity", "/properties/Type" ],
  "primaryIdentifier" : [ "/properties/RuleGroupArn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "network-firewall:CreateRuleGroup", "network-firewall:DescribeRuleGroup", "network-firewall:TagResource", "network-firewall:ListRuleGroups", "iam:CreateServiceLinkedRole", "ec2:GetManagedPrefixListEntries" ]
    },
    "read" : {
      "permissions" : [ "network-firewall:DescribeRuleGroup", "network-firewall:ListTagsForResources" ]
    },
    "update" : {
      "permissions" : [ "network-firewall:UpdateRuleGroup", "network-firewall:DescribeRuleGroup", "network-firewall:TagResource", "network-firewall:UntagResource", "iam:CreateServiceLinkedRole", "ec2:GetManagedPrefixListEntries" ]
    },
    "delete" : {
      "permissions" : [ "network-firewall:DeleteRuleGroup", "network-firewall:DescribeRuleGroup", "network-firewall:UntagResource" ]
    },
    "list" : {
      "permissions" : [ "network-firewall:ListRuleGroups" ]
    }
  }
}