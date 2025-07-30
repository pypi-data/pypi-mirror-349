SCHEMA = {
  "typeName" : "AWS::Wisdom::KnowledgeBase",
  "description" : "Definition of AWS::Wisdom::KnowledgeBase Resource Type",
  "definitions" : {
    "AppIntegrationsConfiguration" : {
      "type" : "object",
      "properties" : {
        "ObjectFields" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "maxLength" : 4096,
            "minLength" : 1
          },
          "insertionOrder" : False,
          "maxItems" : 100,
          "minItems" : 1
        },
        "AppIntegrationArn" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^arn:[a-z-]+?:[a-z-]+?:[a-z0-9-]*?:([0-9]{12})?:[a-zA-Z0-9-:/]+$"
        }
      },
      "required" : [ "AppIntegrationArn" ],
      "additionalProperties" : False
    },
    "KnowledgeBaseType" : {
      "type" : "string",
      "enum" : [ "EXTERNAL", "CUSTOM", "MESSAGE_TEMPLATES", "MANAGED", "QUICK_RESPONSES" ]
    },
    "RenderingConfiguration" : {
      "type" : "object",
      "properties" : {
        "TemplateUri" : {
          "type" : "string",
          "maxLength" : 4096,
          "minLength" : 1
        }
      },
      "additionalProperties" : False
    },
    "ServerSideEncryptionConfiguration" : {
      "type" : "object",
      "properties" : {
        "KmsKeyId" : {
          "type" : "string",
          "maxLength" : 4096,
          "minLength" : 1
        }
      },
      "additionalProperties" : False
    },
    "SeedUrl" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Url" : {
          "type" : "string",
          "pattern" : "^https?://[A-Za-z0-9][^\\s]*$"
        }
      }
    },
    "UrlFilterPattern" : {
      "type" : "string",
      "maxLength" : 1000,
      "minLength" : 1
    },
    "UrlFilterList" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/UrlFilterPattern"
      },
      "maxItems" : 25,
      "minItems" : 1
    },
    "WebCrawlerConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "UrlConfiguration" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "SeedUrls" : {
              "type" : "array",
              "items" : {
                "$ref" : "#/definitions/SeedUrl"
              },
              "maxItems" : 100,
              "minItems" : 1
            }
          }
        },
        "CrawlerLimits" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "RateLimit" : {
              "type" : "number",
              "minimum" : 1,
              "maximum" : 3000
            }
          }
        },
        "InclusionFilters" : {
          "$ref" : "#/definitions/UrlFilterList"
        },
        "ExclusionFilters" : {
          "$ref" : "#/definitions/UrlFilterList"
        },
        "Scope" : {
          "type" : "string",
          "enum" : [ "HOST_ONLY", "SUBDOMAINS" ]
        }
      },
      "required" : [ "UrlConfiguration" ]
    },
    "ManagedSourceConfiguration" : {
      "oneOf" : [ {
        "type" : "object",
        "properties" : {
          "WebCrawlerConfiguration" : {
            "$ref" : "#/definitions/WebCrawlerConfiguration"
          }
        },
        "required" : [ "WebCrawlerConfiguration" ],
        "additionalProperties" : False
      } ]
    },
    "FixedSizeChunkingConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxTokens" : {
          "type" : "number",
          "minimum" : 1
        },
        "OverlapPercentage" : {
          "type" : "number",
          "minimum" : 1,
          "maximum" : 99
        }
      },
      "required" : [ "MaxTokens", "OverlapPercentage" ]
    },
    "HierarchicalChunkingLevelConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxTokens" : {
          "type" : "number",
          "minimum" : 1,
          "maximum" : 8192
        }
      },
      "required" : [ "MaxTokens" ]
    },
    "HierarchicalChunkingConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "LevelConfigurations" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/HierarchicalChunkingLevelConfiguration"
          },
          "maxItems" : 2,
          "minItems" : 2
        },
        "OverlapTokens" : {
          "type" : "number",
          "minimum" : 1
        }
      },
      "required" : [ "LevelConfigurations", "OverlapTokens" ]
    },
    "SemanticChunkingConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxTokens" : {
          "type" : "number",
          "minimum" : 1
        },
        "BufferSize" : {
          "type" : "number",
          "minimum" : 0,
          "maximum" : 1
        },
        "BreakpointPercentileThreshold" : {
          "type" : "number",
          "minimum" : 50,
          "maximum" : 99
        }
      },
      "required" : [ "MaxTokens", "BufferSize", "BreakpointPercentileThreshold" ]
    },
    "BedrockFoundationModelConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ModelArn" : {
          "type" : "string",
          "maxLength" : 2048,
          "minLength" : 1,
          "pattern" : "^arn:aws(-[^:]+)?:bedrock:[a-z0-9-]{1,20}::foundation-model\\/anthropic.claude-3-haiku-20240307-v1:0$"
        },
        "ParsingPrompt" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "ParsingPromptText" : {
              "type" : "string",
              "maxLength" : 10000,
              "minLength" : 1
            }
          },
          "required" : [ "ParsingPromptText" ]
        }
      },
      "required" : [ "ModelArn" ]
    },
    "VectorIngestionConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ChunkingConfiguration" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "ChunkingStrategy" : {
              "type" : "string",
              "enum" : [ "FIXED_SIZE", "NONE", "HIERARCHICAL", "SEMANTIC" ]
            },
            "FixedSizeChunkingConfiguration" : {
              "$ref" : "#/definitions/FixedSizeChunkingConfiguration"
            },
            "HierarchicalChunkingConfiguration" : {
              "$ref" : "#/definitions/HierarchicalChunkingConfiguration"
            },
            "SemanticChunkingConfiguration" : {
              "$ref" : "#/definitions/SemanticChunkingConfiguration"
            }
          },
          "required" : [ "ChunkingStrategy" ]
        },
        "ParsingConfiguration" : {
          "type" : "object",
          "additionalProperties" : False,
          "properties" : {
            "ParsingStrategy" : {
              "type" : "string",
              "enum" : [ "BEDROCK_FOUNDATION_MODEL" ]
            },
            "BedrockFoundationModelConfiguration" : {
              "$ref" : "#/definitions/BedrockFoundationModelConfiguration"
            }
          },
          "required" : [ "ParsingStrategy" ]
        }
      }
    },
    "SourceConfiguration" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "AppIntegrationsConfiguration",
        "properties" : {
          "AppIntegrations" : {
            "$ref" : "#/definitions/AppIntegrationsConfiguration"
          }
        },
        "required" : [ "AppIntegrations" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "ManagedSourceConfiguration",
        "properties" : {
          "ManagedSourceConfiguration" : {
            "$ref" : "#/definitions/ManagedSourceConfiguration"
          }
        },
        "required" : [ "ManagedSourceConfiguration" ],
        "additionalProperties" : False
      } ]
    },
    "Tag" : {
      "additionalProperties" : False,
      "properties" : {
        "Key" : {
          "maxLength" : 128,
          "minLength" : 1,
          "pattern" : "^(?!aws:)[a-zA-Z+-=._:/]+$",
          "type" : "string"
        },
        "Value" : {
          "maxLength" : 256,
          "minLength" : 1,
          "type" : "string"
        }
      },
      "required" : [ "Key", "Value" ],
      "type" : "object"
    }
  },
  "properties" : {
    "Description" : {
      "type" : "string",
      "maxLength" : 255,
      "minLength" : 1
    },
    "KnowledgeBaseArn" : {
      "type" : "string",
      "pattern" : "^arn:[a-z-]*?:wisdom:[a-z0-9-]*?:[0-9]{12}:[a-z-]*?/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}(?:/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})?$"
    },
    "KnowledgeBaseId" : {
      "type" : "string",
      "pattern" : "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    },
    "KnowledgeBaseType" : {
      "$ref" : "#/definitions/KnowledgeBaseType"
    },
    "Name" : {
      "type" : "string",
      "maxLength" : 255,
      "minLength" : 1
    },
    "RenderingConfiguration" : {
      "$ref" : "#/definitions/RenderingConfiguration"
    },
    "ServerSideEncryptionConfiguration" : {
      "$ref" : "#/definitions/ServerSideEncryptionConfiguration"
    },
    "SourceConfiguration" : {
      "$ref" : "#/definitions/SourceConfiguration"
    },
    "VectorIngestionConfiguration" : {
      "$ref" : "#/definitions/VectorIngestionConfiguration"
    },
    "Tags" : {
      "insertionOrder" : False,
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Tag"
      },
      "type" : "array"
    }
  },
  "required" : [ "KnowledgeBaseType", "Name" ],
  "readOnlyProperties" : [ "/properties/KnowledgeBaseId", "/properties/KnowledgeBaseArn" ],
  "createOnlyProperties" : [ "/properties/Description", "/properties/KnowledgeBaseType", "/properties/Name", "/properties/ServerSideEncryptionConfiguration", "/properties/SourceConfiguration", "/properties/Tags" ],
  "primaryIdentifier" : [ "/properties/KnowledgeBaseId" ],
  "additionalIdentifiers" : [ [ "/properties/KnowledgeBaseArn" ] ],
  "additionalProperties" : False,
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "wisdom:TagResource" ]
  },
  "replacementStrategy" : "delete_then_create",
  "handlers" : {
    "create" : {
      "permissions" : [ "appflow:CreateFlow", "appflow:DeleteFlow", "appflow:StartFlow", "appflow:TagResource", "appflow:UseConnectorProfile", "app-integrations:CreateDataIntegrationAssociation", "app-integrations:GetDataIntegration", "kms:DescribeKey", "kms:CreateGrant", "kms:ListGrants", "wisdom:CreateKnowledgeBase", "wisdom:TagResource" ]
    },
    "update" : {
      "permissions" : [ "wisdom:GetKnowledgeBase" ]
    },
    "delete" : {
      "permissions" : [ "appflow:DeleteFlow", "appflow:StopFlow", "app-integrations:DeleteDataIntegrationAssociation", "wisdom:DeleteKnowledgeBase" ]
    },
    "list" : {
      "permissions" : [ "wisdom:ListKnowledgeBases" ]
    },
    "read" : {
      "permissions" : [ "wisdom:GetKnowledgeBase" ]
    }
  }
}