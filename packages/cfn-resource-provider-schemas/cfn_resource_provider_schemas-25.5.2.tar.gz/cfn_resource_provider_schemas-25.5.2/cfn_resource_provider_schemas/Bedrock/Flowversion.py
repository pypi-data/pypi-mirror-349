SCHEMA = {
  "typeName" : "AWS::Bedrock::FlowVersion",
  "description" : "Definition of AWS::Bedrock::FlowVersion Resource Type",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-bedrock-flows",
  "definitions" : {
    "ConditionFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Condition flow node configuration",
      "properties" : {
        "Conditions" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FlowCondition"
          },
          "maxItems" : 5,
          "minItems" : 1,
          "description" : "List of conditions in a condition node",
          "insertionOrder" : True
        }
      },
      "required" : [ "Conditions" ],
      "additionalProperties" : False
    },
    "FlowCondition" : {
      "type" : "object",
      "description" : "Condition branch for a condition node",
      "properties" : {
        "Name" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z]([_]?[0-9a-zA-Z]){1,50}$",
          "description" : "Name of a condition in a flow"
        },
        "Expression" : {
          "type" : "string",
          "maxLength" : 64,
          "minLength" : 1,
          "description" : "Expression for a condition in a flow"
        }
      },
      "required" : [ "Name" ],
      "additionalProperties" : False
    },
    "FlowConditionalConnectionConfiguration" : {
      "type" : "object",
      "description" : "Conditional connection configuration",
      "properties" : {
        "Condition" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z]([_]?[0-9a-zA-Z]){1,50}$",
          "description" : "Name of a condition in a flow"
        }
      },
      "required" : [ "Condition" ],
      "additionalProperties" : False
    },
    "FlowConnection" : {
      "type" : "object",
      "description" : "Flow connection",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/FlowConnectionType"
        },
        "Name" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z]([_]?[0-9a-zA-Z]){1,100}$",
          "description" : "Name of a connection in a flow"
        },
        "Source" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z]([_]?[0-9a-zA-Z]){1,50}$",
          "description" : "Name of a node in a flow"
        },
        "Target" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z]([_]?[0-9a-zA-Z]){1,50}$",
          "description" : "Name of a node in a flow"
        },
        "Configuration" : {
          "$ref" : "#/definitions/FlowConnectionConfiguration"
        }
      },
      "required" : [ "Name", "Source", "Target", "Type" ],
      "additionalProperties" : False
    },
    "FlowConnectionConfiguration" : {
      "description" : "Connection configuration",
      "oneOf" : [ {
        "type" : "object",
        "title" : "Data",
        "properties" : {
          "Data" : {
            "$ref" : "#/definitions/FlowDataConnectionConfiguration"
          }
        },
        "required" : [ "Data" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Conditional",
        "properties" : {
          "Conditional" : {
            "$ref" : "#/definitions/FlowConditionalConnectionConfiguration"
          }
        },
        "required" : [ "Conditional" ],
        "additionalProperties" : False
      } ]
    },
    "FlowConnectionType" : {
      "type" : "string",
      "description" : "Connection type",
      "enum" : [ "Data", "Conditional" ]
    },
    "FlowDataConnectionConfiguration" : {
      "type" : "object",
      "description" : "Data connection configuration",
      "properties" : {
        "SourceOutput" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z]([_]?[0-9a-zA-Z]){1,50}$",
          "description" : "Name of a node output in a flow"
        },
        "TargetInput" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z]([_]?[0-9a-zA-Z]){1,50}$",
          "description" : "Name of a node input in a flow"
        }
      },
      "required" : [ "SourceOutput", "TargetInput" ],
      "additionalProperties" : False
    },
    "FlowDefinition" : {
      "type" : "object",
      "description" : "Flow definition",
      "properties" : {
        "Nodes" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FlowNode"
          },
          "maxItems" : 40,
          "description" : "List of nodes in a flow",
          "insertionOrder" : True
        },
        "Connections" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FlowConnection"
          },
          "maxItems" : 100,
          "description" : "List of connections",
          "insertionOrder" : True
        }
      },
      "additionalProperties" : False
    },
    "FlowNode" : {
      "type" : "object",
      "description" : "Internal mixin for flow node",
      "properties" : {
        "Name" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z]([_]?[0-9a-zA-Z]){1,50}$",
          "description" : "Name of a node in a flow"
        },
        "Type" : {
          "$ref" : "#/definitions/FlowNodeType"
        },
        "Configuration" : {
          "$ref" : "#/definitions/FlowNodeConfiguration"
        },
        "Inputs" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FlowNodeInput"
          },
          "maxItems" : 5,
          "description" : "List of node inputs in a flow",
          "insertionOrder" : True
        },
        "Outputs" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FlowNodeOutput"
          },
          "maxItems" : 5,
          "description" : "List of node outputs in a flow",
          "insertionOrder" : True
        }
      },
      "required" : [ "Name", "Type" ],
      "additionalProperties" : False
    },
    "FlowNodeConfiguration" : {
      "description" : "Node configuration in a flow",
      "oneOf" : [ {
        "type" : "object",
        "title" : "Input",
        "properties" : {
          "Input" : {
            "$ref" : "#/definitions/InputFlowNodeConfiguration"
          }
        },
        "required" : [ "Input" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Output",
        "properties" : {
          "Output" : {
            "$ref" : "#/definitions/OutputFlowNodeConfiguration"
          }
        },
        "required" : [ "Output" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "KnowledgeBase",
        "properties" : {
          "KnowledgeBase" : {
            "$ref" : "#/definitions/KnowledgeBaseFlowNodeConfiguration"
          }
        },
        "required" : [ "KnowledgeBase" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Condition",
        "properties" : {
          "Condition" : {
            "$ref" : "#/definitions/ConditionFlowNodeConfiguration"
          }
        },
        "required" : [ "Condition" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Lex",
        "properties" : {
          "Lex" : {
            "$ref" : "#/definitions/LexFlowNodeConfiguration"
          }
        },
        "required" : [ "Lex" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Prompt",
        "properties" : {
          "Prompt" : {
            "$ref" : "#/definitions/PromptFlowNodeConfiguration"
          }
        },
        "required" : [ "Prompt" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "LambdaFunction",
        "properties" : {
          "LambdaFunction" : {
            "$ref" : "#/definitions/LambdaFunctionFlowNodeConfiguration"
          }
        },
        "required" : [ "LambdaFunction" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Agent",
        "properties" : {
          "Agent" : {
            "$ref" : "#/definitions/AgentFlowNodeConfiguration"
          }
        },
        "required" : [ "Agent" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Storage",
        "properties" : {
          "Storage" : {
            "$ref" : "#/definitions/StorageFlowNodeConfiguration"
          }
        },
        "required" : [ "Storage" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Retrieval",
        "properties" : {
          "Retrieval" : {
            "$ref" : "#/definitions/RetrievalFlowNodeConfiguration"
          }
        },
        "required" : [ "Retrieval" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Iterator",
        "properties" : {
          "Iterator" : {
            "$ref" : "#/definitions/IteratorFlowNodeConfiguration"
          }
        },
        "required" : [ "Iterator" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Collector",
        "properties" : {
          "Collector" : {
            "$ref" : "#/definitions/CollectorFlowNodeConfiguration"
          }
        },
        "required" : [ "Collector" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "InlineCode",
        "properties" : {
          "InlineCode" : {
            "$ref" : "#/definitions/InlineCodeFlowNodeConfiguration"
          }
        },
        "required" : [ "InlineCode" ],
        "additionalProperties" : False
      } ]
    },
    "LexFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Lex flow node configuration",
      "properties" : {
        "BotAliasArn" : {
          "type" : "string",
          "maxLength" : 78,
          "pattern" : "^arn:aws(|-us-gov):lex:[a-z]{2}(-gov)?-[a-z]+-\\d{1}:\\d{12}:bot-alias/[0-9a-zA-Z]+/[0-9a-zA-Z]+$",
          "description" : "ARN of a Lex bot alias"
        },
        "LocaleId" : {
          "type" : "string",
          "maxLength" : 10,
          "minLength" : 1,
          "description" : "Lex bot locale id"
        }
      },
      "required" : [ "BotAliasArn", "LocaleId" ],
      "additionalProperties" : False
    },
    "FlowNodeIODataType" : {
      "type" : "string",
      "description" : "Type of input/output for a node in a flow",
      "enum" : [ "String", "Number", "Boolean", "Object", "Array" ]
    },
    "FlowNodeInput" : {
      "type" : "object",
      "description" : "Input to a node in a flow",
      "properties" : {
        "Name" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z]([_]?[0-9a-zA-Z]){1,50}$",
          "description" : "Name of a node input in a flow"
        },
        "Type" : {
          "$ref" : "#/definitions/FlowNodeIODataType"
        },
        "Expression" : {
          "type" : "string",
          "maxLength" : 64,
          "minLength" : 1,
          "description" : "Expression for a node input in a flow"
        }
      },
      "required" : [ "Expression", "Name", "Type" ],
      "additionalProperties" : False
    },
    "FlowNodeOutput" : {
      "type" : "object",
      "description" : "Output of a node in a flow",
      "properties" : {
        "Name" : {
          "type" : "string",
          "pattern" : "^[a-zA-Z]([_]?[0-9a-zA-Z]){1,50}$",
          "description" : "Name of a node output in a flow"
        },
        "Type" : {
          "$ref" : "#/definitions/FlowNodeIODataType"
        }
      },
      "required" : [ "Name", "Type" ],
      "additionalProperties" : False
    },
    "FlowNodeType" : {
      "type" : "string",
      "description" : "Flow node types",
      "enum" : [ "Input", "Output", "KnowledgeBase", "Condition", "Lex", "Prompt", "LambdaFunction", "Agent", "Iterator", "Collector", "Storage", "Retrieval", "InlineCode" ]
    },
    "FlowStatus" : {
      "type" : "string",
      "description" : "Schema Type for Flow APIs",
      "enum" : [ "Failed", "Prepared", "Preparing", "NotPrepared" ]
    },
    "InputFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Input flow node configuration",
      "additionalProperties" : False
    },
    "AgentFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Agent flow node configuration",
      "properties" : {
        "AgentAliasArn" : {
          "type" : "string",
          "maxLength" : 2048,
          "pattern" : "^arn:aws(-[^:]+)?:bedrock:[a-z0-9-]{1,20}:[0-9]{12}:agent-alias/[0-9a-zA-Z]{10}/[0-9a-zA-Z]{10}$",
          "description" : "Arn representation of the Agent Alias."
        }
      },
      "required" : [ "AgentAliasArn" ],
      "additionalProperties" : False
    },
    "KnowledgeBaseFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Knowledge base flow node configuration",
      "properties" : {
        "KnowledgeBaseId" : {
          "type" : "string",
          "maxLength" : 10,
          "pattern" : "^[0-9a-zA-Z]+$",
          "description" : "Identifier of the KnowledgeBase"
        },
        "ModelId" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^(arn:aws(-[^:]{1,12})?:(bedrock|sagemaker):[a-z0-9-]{1,20}:([0-9]{12})?:([a-z-]+/)?)?([a-zA-Z0-9.-]{1,63}){0,2}(([:][a-z0-9-]{1,63}){0,2})?(/[a-z0-9]{1,12})?$",
          "description" : "ARN or Id of a Bedrock Foundational Model or Inference Profile, or the ARN of a imported model, or a provisioned throughput ARN for custom models."
        },
        "GuardrailConfiguration" : {
          "$ref" : "#/definitions/GuardrailConfiguration"
        }
      },
      "required" : [ "KnowledgeBaseId" ],
      "additionalProperties" : False
    },
    "LambdaFunctionFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Lambda function flow node configuration",
      "properties" : {
        "LambdaArn" : {
          "type" : "string",
          "maxLength" : 2048,
          "pattern" : "^arn:(aws[a-zA-Z-]*)?:lambda:[a-z]{2}(-gov)?-[a-z]+-\\d{1}:\\d{12}:function:[a-zA-Z0-9-_\\.]+(:(\\$LATEST|[a-zA-Z0-9-_]+))?$",
          "description" : "ARN of a Lambda."
        }
      },
      "required" : [ "LambdaArn" ],
      "additionalProperties" : False
    },
    "OutputFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Output flow node configuration",
      "additionalProperties" : False
    },
    "IteratorFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Iterator flow node configuration",
      "additionalProperties" : False
    },
    "CollectorFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Collector flow node configuration",
      "additionalProperties" : False
    },
    "PromptFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Prompt flow node configuration",
      "properties" : {
        "SourceConfiguration" : {
          "$ref" : "#/definitions/PromptFlowNodeSourceConfiguration"
        },
        "GuardrailConfiguration" : {
          "$ref" : "#/definitions/GuardrailConfiguration"
        }
      },
      "required" : [ "SourceConfiguration" ],
      "additionalProperties" : False
    },
    "StorageFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Storage flow node configuration",
      "properties" : {
        "ServiceConfiguration" : {
          "$ref" : "#/definitions/StorageFlowNodeServiceConfiguration"
        }
      },
      "required" : [ "ServiceConfiguration" ],
      "additionalProperties" : False
    },
    "RetrievalFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Retrieval flow node configuration",
      "properties" : {
        "ServiceConfiguration" : {
          "$ref" : "#/definitions/RetrievalFlowNodeServiceConfiguration"
        }
      },
      "required" : [ "ServiceConfiguration" ],
      "additionalProperties" : False
    },
    "InlineCodeFlowNodeConfiguration" : {
      "type" : "object",
      "description" : "Inline code config strucuture, contains code configs",
      "properties" : {
        "Code" : {
          "type" : "string",
          "maxLength" : 5000000,
          "description" : "The inline code entered by customers. max size is 5MB."
        },
        "Language" : {
          "$ref" : "#/definitions/SupportedLanguages"
        }
      },
      "required" : [ "Code", "Language" ],
      "additionalProperties" : False
    },
    "SupportedLanguages" : {
      "type" : "string",
      "description" : "Enum encodes the supported language type",
      "enum" : [ "Python_3" ]
    },
    "PromptFlowNodeInlineConfiguration" : {
      "type" : "object",
      "description" : "Inline prompt configuration for prompt node",
      "properties" : {
        "TemplateType" : {
          "$ref" : "#/definitions/PromptTemplateType"
        },
        "TemplateConfiguration" : {
          "$ref" : "#/definitions/PromptTemplateConfiguration"
        },
        "ModelId" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^(arn:aws(-[^:]{1,12})?:(bedrock|sagemaker):[a-z0-9-]{1,20}:([0-9]{12})?:([a-z-]+/)?)?([a-zA-Z0-9.-]{1,63}){0,2}(([:][a-z0-9-]{1,63}){0,2})?(/[a-z0-9]{1,12})?$",
          "description" : "ARN or Id of a Bedrock Foundational Model or Inference Profile, or the ARN of a imported model, or a provisioned throughput ARN for custom models."
        },
        "InferenceConfiguration" : {
          "$ref" : "#/definitions/PromptInferenceConfiguration"
        }
      },
      "required" : [ "ModelId", "TemplateConfiguration", "TemplateType" ],
      "additionalProperties" : False
    },
    "PromptFlowNodeResourceConfiguration" : {
      "type" : "object",
      "description" : "Resource prompt configuration for prompt node",
      "properties" : {
        "PromptArn" : {
          "type" : "string",
          "pattern" : "^(arn:aws(-[^:]+)?:bedrock:[a-z0-9-]{1,20}:[0-9]{12}:prompt/[0-9a-zA-Z]{10}(?::[0-9]{1,5})?)$",
          "description" : "ARN of a prompt resource possibly with a version"
        }
      },
      "required" : [ "PromptArn" ],
      "additionalProperties" : False
    },
    "PromptFlowNodeSourceConfiguration" : {
      "description" : "Prompt source configuration for prompt node",
      "oneOf" : [ {
        "type" : "object",
        "title" : "Resource",
        "properties" : {
          "Resource" : {
            "$ref" : "#/definitions/PromptFlowNodeResourceConfiguration"
          }
        },
        "required" : [ "Resource" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Inline",
        "properties" : {
          "Inline" : {
            "$ref" : "#/definitions/PromptFlowNodeInlineConfiguration"
          }
        },
        "required" : [ "Inline" ],
        "additionalProperties" : False
      } ]
    },
    "StorageFlowNodeServiceConfiguration" : {
      "description" : "storage service configuration for storage node",
      "oneOf" : [ {
        "type" : "object",
        "title" : "S3",
        "properties" : {
          "S3" : {
            "$ref" : "#/definitions/StorageFlowNodeS3Configuration"
          }
        },
        "additionalProperties" : False
      } ]
    },
    "StorageFlowNodeS3Configuration" : {
      "type" : "object",
      "description" : "s3 storage configuration for storage node",
      "properties" : {
        "BucketName" : {
          "type" : "string",
          "pattern" : "^[a-z0-9][\\.\\-a-z0-9]{1,61}[a-z0-9]$",
          "description" : "bucket name of an s3 that will be used for storage flow node configuration"
        }
      },
      "required" : [ "BucketName" ],
      "additionalProperties" : False
    },
    "RetrievalFlowNodeServiceConfiguration" : {
      "description" : "Retrieval service configuration for Retrieval node",
      "oneOf" : [ {
        "type" : "object",
        "title" : "S3",
        "properties" : {
          "S3" : {
            "$ref" : "#/definitions/RetrievalFlowNodeS3Configuration"
          }
        },
        "additionalProperties" : False
      } ]
    },
    "RetrievalFlowNodeS3Configuration" : {
      "type" : "object",
      "description" : "s3 Retrieval configuration for Retrieval node",
      "properties" : {
        "BucketName" : {
          "type" : "string",
          "pattern" : "^[a-z0-9][\\.\\-a-z0-9]{1,61}[a-z0-9]$",
          "description" : "bucket name of an s3 that will be used for Retrieval flow node configuration"
        }
      },
      "required" : [ "BucketName" ],
      "additionalProperties" : False
    },
    "PromptInferenceConfiguration" : {
      "description" : "Model inference configuration",
      "oneOf" : [ {
        "type" : "object",
        "title" : "Text",
        "properties" : {
          "Text" : {
            "$ref" : "#/definitions/PromptModelInferenceConfiguration"
          }
        },
        "required" : [ "Text" ],
        "additionalProperties" : False
      } ]
    },
    "PromptInputVariable" : {
      "type" : "object",
      "description" : "Input variable",
      "properties" : {
        "Name" : {
          "type" : "string",
          "pattern" : "^([0-9a-zA-Z][_-]?){1,100}$",
          "description" : "Name for an input variable"
        }
      },
      "additionalProperties" : False
    },
    "PromptModelInferenceConfiguration" : {
      "type" : "object",
      "description" : "Prompt model inference configuration",
      "properties" : {
        "Temperature" : {
          "type" : "number",
          "maximum" : 1,
          "minimum" : 0,
          "description" : "Controls randomness, higher values increase diversity"
        },
        "TopP" : {
          "type" : "number",
          "maximum" : 1,
          "minimum" : 0,
          "description" : "Cumulative probability cutoff for token selection"
        },
        "MaxTokens" : {
          "type" : "number",
          "maximum" : 4096,
          "minimum" : 0,
          "description" : "Maximum length of output"
        },
        "StopSequences" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          },
          "maxItems" : 4,
          "minItems" : 0,
          "description" : "List of stop sequences",
          "insertionOrder" : True
        }
      },
      "additionalProperties" : False
    },
    "PromptTemplateConfiguration" : {
      "description" : "Prompt template configuration",
      "oneOf" : [ {
        "type" : "object",
        "title" : "Text",
        "properties" : {
          "Text" : {
            "$ref" : "#/definitions/TextPromptTemplateConfiguration"
          }
        },
        "required" : [ "Text" ],
        "additionalProperties" : False
      } ]
    },
    "PromptTemplateType" : {
      "type" : "string",
      "description" : "Prompt template type",
      "enum" : [ "TEXT" ]
    },
    "TextPromptTemplateConfiguration" : {
      "type" : "object",
      "description" : "Configuration for text prompt template",
      "properties" : {
        "Text" : {
          "type" : "string",
          "maxLength" : 200000,
          "minLength" : 1,
          "description" : "Prompt content for String prompt template"
        },
        "InputVariables" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/PromptInputVariable"
          },
          "maxItems" : 20,
          "minItems" : 0,
          "description" : "List of input variables",
          "insertionOrder" : True
        }
      },
      "required" : [ "Text" ],
      "additionalProperties" : False
    },
    "GuardrailConfiguration" : {
      "type" : "object",
      "description" : "Configuration for a guardrail",
      "properties" : {
        "GuardrailIdentifier" : {
          "type" : "string",
          "maxLength" : 2048,
          "pattern" : "^(([a-z0-9]+)|(arn:aws(-[^:]+)?:bedrock:[a-z0-9-]{1,20}:[0-9]{12}:guardrail/[a-z0-9]+))$",
          "description" : "Identifier for the guardrail, could be the id or the arn"
        },
        "GuardrailVersion" : {
          "type" : "string",
          "pattern" : "^(([0-9]{1,8})|(DRAFT))$",
          "description" : "Version of the guardrail"
        }
      },
      "additionalProperties" : False
    }
  },
  "properties" : {
    "FlowArn" : {
      "type" : "string",
      "pattern" : "^arn:aws(-[^:]+)?:bedrock:[a-z0-9-]{1,20}:[0-9]{12}:flow/[0-9a-zA-Z]{10}$",
      "description" : "Arn representation of the Flow"
    },
    "CreatedAt" : {
      "type" : "string",
      "description" : "Time Stamp.",
      "format" : "date-time"
    },
    "Definition" : {
      "$ref" : "#/definitions/FlowDefinition"
    },
    "Description" : {
      "type" : "string",
      "maxLength" : 200,
      "minLength" : 1,
      "description" : "Description of the flow version"
    },
    "ExecutionRoleArn" : {
      "type" : "string",
      "maxLength" : 2048,
      "pattern" : "^arn:aws(-[^:]+)?:iam::([0-9]{12})?:role/(service-role/)?.+$",
      "description" : "ARN of a IAM role"
    },
    "FlowId" : {
      "type" : "string",
      "pattern" : "^[0-9a-zA-Z]{10}$",
      "description" : "Identifier for a Flow"
    },
    "Name" : {
      "type" : "string",
      "pattern" : "^([0-9a-zA-Z][_-]?){1,100}$",
      "description" : "Name for the flow"
    },
    "Status" : {
      "$ref" : "#/definitions/FlowStatus"
    },
    "Version" : {
      "type" : "string",
      "pattern" : "^[0-9]{1,5}$",
      "description" : "Numerical Version."
    },
    "CustomerEncryptionKeyArn" : {
      "type" : "string",
      "maxLength" : 2048,
      "minLength" : 1,
      "pattern" : "^arn:aws(|-cn|-us-gov):kms:[a-zA-Z0-9-]*:[0-9]{12}:key/[a-zA-Z0-9-]{36}$",
      "description" : "A KMS key ARN"
    }
  },
  "required" : [ "FlowArn" ],
  "readOnlyProperties" : [ "/properties/CreatedAt", "/properties/Definition", "/properties/ExecutionRoleArn", "/properties/FlowId", "/properties/Name", "/properties/Status", "/properties/Version", "/properties/CustomerEncryptionKeyArn" ],
  "createOnlyProperties" : [ "/properties/Description", "/properties/FlowArn" ],
  "primaryIdentifier" : [ "/properties/FlowArn", "/properties/Version" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "bedrock:CreateFlowVersion", "bedrock:GetFlowVersion", "kms:GenerateDataKey", "kms:Decrypt", "bedrock:CreateGuardrail", "bedrock:CreateGuardrailVersion", "bedrock:GetGuardrail" ]
    },
    "read" : {
      "permissions" : [ "bedrock:GetFlowVersion", "kms:Decrypt", "bedrock:GetGuardrail" ]
    },
    "delete" : {
      "permissions" : [ "bedrock:DeleteFlowVersion", "bedrock:GetFlowVersion", "bedrock:DeleteGuardrail", "bedrock:GetGuardrail" ]
    },
    "list" : {
      "permissions" : [ "bedrock:ListFlowVersions", "bedrock:ListGuardrails" ],
      "handlerSchema" : {
        "properties" : {
          "FlowArn" : {
            "$ref" : "resource-schema.json#/properties/FlowArn"
          }
        },
        "required" : [ "FlowArn" ]
      }
    },
    "update" : {
      "permissions" : [ "noservice:NoAction" ]
    }
  },
  "tagging" : {
    "taggable" : False
  },
  "additionalProperties" : False
}