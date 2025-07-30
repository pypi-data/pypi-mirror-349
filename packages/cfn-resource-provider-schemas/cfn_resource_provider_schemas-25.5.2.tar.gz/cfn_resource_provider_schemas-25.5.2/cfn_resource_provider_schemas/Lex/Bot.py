SCHEMA = {
  "typeName" : "AWS::Lex::Bot",
  "description" : "Amazon Lex conversational bot performing automated tasks such as ordering a pizza, booking a hotel, and so on.",
  "sourceUrl" : "https://docs.aws.amazon.com/lexv2/latest/dg/build-create.html",
  "definitions" : {
    "ReplicaRegion" : {
      "description" : "The secondary region that will be used in the replication of the source bot.",
      "type" : "string",
      "minLength" : 2,
      "maxLength" : 25
    },
    "Replication" : {
      "type" : "object",
      "properties" : {
        "ReplicaRegions" : {
          "type" : "array",
          "uniqueItems" : True,
          "maxItems" : 1,
          "minItems" : 1,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/ReplicaRegion"
          }
        }
      },
      "required" : [ "ReplicaRegions" ],
      "additionalProperties" : False
    },
    "BotAliasLocaleSettingsList" : {
      "type" : "array",
      "uniqueItems" : True,
      "maxItems" : 50,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/BotAliasLocaleSettingsItem"
      }
    },
    "BotAliasLocaleSettingsItem" : {
      "type" : "object",
      "properties" : {
        "LocaleId" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128
        },
        "BotAliasLocaleSetting" : {
          "$ref" : "#/definitions/BotAliasLocaleSettings"
        }
      },
      "required" : [ "LocaleId", "BotAliasLocaleSetting" ],
      "additionalProperties" : False
    },
    "BotAliasLocaleSettings" : {
      "type" : "object",
      "properties" : {
        "CodeHookSpecification" : {
          "$ref" : "#/definitions/CodeHookSpecification"
        },
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ],
      "additionalProperties" : False
    },
    "CodeHookSpecification" : {
      "type" : "object",
      "properties" : {
        "LambdaCodeHook" : {
          "$ref" : "#/definitions/LambdaCodeHook"
        }
      },
      "required" : [ "LambdaCodeHook" ],
      "additionalProperties" : False
    },
    "LambdaCodeHook" : {
      "type" : "object",
      "properties" : {
        "CodeHookInterfaceVersion" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 5
        },
        "LambdaArn" : {
          "type" : "string",
          "minLength" : 20,
          "maxLength" : 2048
        }
      },
      "required" : [ "CodeHookInterfaceVersion", "LambdaArn" ],
      "additionalProperties" : False
    },
    "ConversationLogSettings" : {
      "type" : "object",
      "properties" : {
        "AudioLogSettings" : {
          "$ref" : "#/definitions/AudioLogSettings"
        },
        "TextLogSettings" : {
          "$ref" : "#/definitions/TextLogSettings"
        }
      },
      "additionalProperties" : False
    },
    "AudioLogSettings" : {
      "type" : "array",
      "maxItems" : 1,
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/AudioLogSetting"
      }
    },
    "TextLogSettings" : {
      "type" : "array",
      "maxItems" : 1,
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/TextLogSetting"
      }
    },
    "AudioLogSetting" : {
      "type" : "object",
      "properties" : {
        "Destination" : {
          "$ref" : "#/definitions/AudioLogDestination"
        },
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Destination", "Enabled" ],
      "additionalProperties" : False
    },
    "TextLogSetting" : {
      "type" : "object",
      "properties" : {
        "Destination" : {
          "$ref" : "#/definitions/TextLogDestination"
        },
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Destination", "Enabled" ],
      "additionalProperties" : False
    },
    "AudioLogDestination" : {
      "type" : "object",
      "properties" : {
        "S3Bucket" : {
          "$ref" : "#/definitions/S3BucketLogDestination"
        }
      },
      "required" : [ "S3Bucket" ],
      "additionalProperties" : False
    },
    "TextLogDestination" : {
      "type" : "object",
      "properties" : {
        "CloudWatch" : {
          "$ref" : "#/definitions/CloudWatchLogGroupLogDestination"
        }
      },
      "required" : [ "CloudWatch" ],
      "additionalProperties" : False
    },
    "CloudWatchLogGroupLogDestination" : {
      "type" : "object",
      "properties" : {
        "CloudWatchLogGroupArn" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 2048
        },
        "LogPrefix" : {
          "type" : "string",
          "minLength" : 0,
          "maxLength" : 1024
        }
      },
      "required" : [ "CloudWatchLogGroupArn", "LogPrefix" ],
      "additionalProperties" : False
    },
    "S3BucketLogDestination" : {
      "type" : "object",
      "properties" : {
        "S3BucketArn" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 2048,
          "pattern" : "^arn:[\\w\\-]+:s3:::[a-z0-9][\\.\\-a-z0-9]{1,61}[a-z0-9]$"
        },
        "LogPrefix" : {
          "type" : "string",
          "minLength" : 0,
          "maxLength" : 1024
        },
        "KmsKeyArn" : {
          "type" : "string",
          "minLength" : 20,
          "maxLength" : 2048,
          "pattern" : "^arn:[\\w\\-]+:kms:[\\w\\-]+:[\\d]{12}:(?:key\\/[\\w\\-]+|alias\\/[a-zA-Z0-9:\\/_\\-]{1,256})$"
        }
      },
      "required" : [ "LogPrefix", "S3BucketArn" ],
      "additionalProperties" : False
    },
    "TestBotAliasSettings" : {
      "type" : "object",
      "properties" : {
        "BotAliasLocaleSettings" : {
          "$ref" : "#/definitions/BotAliasLocaleSettingsList"
        },
        "ConversationLogSettings" : {
          "$ref" : "#/definitions/ConversationLogSettings"
        },
        "Description" : {
          "$ref" : "#/definitions/Description"
        },
        "SentimentAnalysisSettings" : {
          "type" : "object",
          "properties" : {
            "DetectSentiment" : {
              "type" : "boolean"
            }
          },
          "required" : [ "DetectSentiment" ],
          "additionalProperties" : False
        }
      },
      "additionalProperties" : False
    },
    "RoleArn" : {
      "type" : "string",
      "minLength" : 32,
      "maxLength" : 2048,
      "pattern" : "^arn:aws[a-zA-Z-]*:iam::[0-9]{12}:role/.*$"
    },
    "Id" : {
      "type" : "string",
      "minLength" : 10,
      "maxLength" : 10,
      "pattern" : "^[0-9a-zA-Z]+$"
    },
    "BotArn" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 1011,
      "pattern" : "^arn:aws[a-zA-Z-]*:lex:[a-z]+-[a-z]+-[0-9]:[0-9]{12}:bot/[0-9a-zA-Z]+$"
    },
    "Name" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 100,
      "pattern" : "^([0-9a-zA-Z][_-]?)+$"
    },
    "Description" : {
      "description" : "A description of the resource",
      "type" : "string",
      "maxLength" : 200
    },
    "DataPrivacy" : {
      "type" : "object",
      "properties" : {
        "ChildDirected" : {
          "type" : "boolean"
        }
      },
      "required" : [ "ChildDirected" ],
      "additionalProperties" : False
    },
    "IdleSessionTTLInSeconds" : {
      "type" : "integer",
      "minimum" : 60,
      "maximum" : 86400
    },
    "Utterance" : {
      "type" : "string"
    },
    "SampleUtterance" : {
      "type" : "object",
      "properties" : {
        "Utterance" : {
          "$ref" : "#/definitions/Utterance"
        }
      },
      "required" : [ "Utterance" ],
      "additionalProperties" : False
    },
    "SampleUtterancesList" : {
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/SampleUtterance"
      }
    },
    "Tag" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 128
        },
        "Value" : {
          "type" : "string",
          "minLength" : 0,
          "maxLength" : 256
        }
      },
      "required" : [ "Key", "Value" ],
      "additionalProperties" : False
    },
    "LocaleId" : {
      "type" : "string"
    },
    "VoiceSettings" : {
      "type" : "object",
      "properties" : {
        "VoiceId" : {
          "type" : "string"
        },
        "Engine" : {
          "type" : "string",
          "enum" : [ "standard", "neural", "long-form", "generative" ]
        }
      },
      "required" : [ "VoiceId" ],
      "additionalProperties" : False
    },
    "ConfidenceThreshold" : {
      "type" : "number",
      "minimum" : 0,
      "maximum" : 1
    },
    "ParentIntentSignature" : {
      "type" : "string"
    },
    "DialogCodeHookSetting" : {
      "type" : "object",
      "properties" : {
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ],
      "additionalProperties" : False
    },
    "FulfillmentStartResponseSpecification" : {
      "type" : "object",
      "properties" : {
        "MessageGroups" : {
          "$ref" : "#/definitions/MessageGroupsList"
        },
        "DelayInSeconds" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 900
        },
        "AllowInterrupt" : {
          "type" : "boolean"
        }
      },
      "required" : [ "DelayInSeconds", "MessageGroups" ],
      "additionalProperties" : False
    },
    "FulfillmentUpdateResponseSpecification" : {
      "type" : "object",
      "properties" : {
        "MessageGroups" : {
          "$ref" : "#/definitions/MessageGroupsList"
        },
        "FrequencyInSeconds" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 900
        },
        "AllowInterrupt" : {
          "type" : "boolean"
        }
      },
      "required" : [ "FrequencyInSeconds", "MessageGroups" ],
      "additionalProperties" : False
    },
    "FulfillmentUpdatesSpecification" : {
      "type" : "object",
      "properties" : {
        "StartResponse" : {
          "$ref" : "#/definitions/FulfillmentStartResponseSpecification"
        },
        "UpdateResponse" : {
          "$ref" : "#/definitions/FulfillmentUpdateResponseSpecification"
        },
        "TimeoutInSeconds" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 900
        },
        "Active" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Active" ],
      "additionalProperties" : False
    },
    "PostFulfillmentStatusSpecification" : {
      "type" : "object",
      "properties" : {
        "SuccessResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "SuccessNextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "SuccessConditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        },
        "FailureResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "FailureNextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "FailureConditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        },
        "TimeoutResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "TimeoutNextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "TimeoutConditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        }
      },
      "required" : [ ],
      "additionalProperties" : False
    },
    "FulfillmentCodeHookSetting" : {
      "type" : "object",
      "properties" : {
        "FulfillmentUpdatesSpecification" : {
          "$ref" : "#/definitions/FulfillmentUpdatesSpecification"
        },
        "PostFulfillmentStatusSpecification" : {
          "$ref" : "#/definitions/PostFulfillmentStatusSpecification"
        },
        "Enabled" : {
          "type" : "boolean"
        },
        "IsActive" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ],
      "additionalProperties" : False
    },
    "Button" : {
      "type" : "object",
      "properties" : {
        "Text" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 50
        },
        "Value" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 50
        }
      },
      "required" : [ "Text", "Value" ],
      "additionalProperties" : False
    },
    "AttachmentTitle" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 250
    },
    "AttachmentUrl" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 250
    },
    "ImageResponseCard" : {
      "type" : "object",
      "properties" : {
        "Title" : {
          "$ref" : "#/definitions/AttachmentTitle"
        },
        "Subtitle" : {
          "$ref" : "#/definitions/AttachmentTitle"
        },
        "ImageUrl" : {
          "$ref" : "#/definitions/AttachmentUrl"
        },
        "Buttons" : {
          "type" : "array",
          "maxItems" : 5,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Button"
          }
        }
      },
      "required" : [ "Title" ],
      "additionalProperties" : False
    },
    "PlainTextMessage" : {
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 1000
        }
      },
      "required" : [ "Value" ],
      "additionalProperties" : False
    },
    "CustomPayload" : {
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 1000
        }
      },
      "required" : [ "Value" ],
      "additionalProperties" : False
    },
    "SSMLMessage" : {
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 1000
        }
      },
      "required" : [ "Value" ],
      "additionalProperties" : False
    },
    "Message" : {
      "type" : "object",
      "properties" : {
        "PlainTextMessage" : {
          "$ref" : "#/definitions/PlainTextMessage"
        },
        "CustomPayload" : {
          "$ref" : "#/definitions/CustomPayload"
        },
        "SSMLMessage" : {
          "$ref" : "#/definitions/SSMLMessage"
        },
        "ImageResponseCard" : {
          "$ref" : "#/definitions/ImageResponseCard"
        }
      },
      "required" : [ ],
      "additionalProperties" : False
    },
    "MessageGroup" : {
      "type" : "object",
      "properties" : {
        "Message" : {
          "$ref" : "#/definitions/Message"
        },
        "Variations" : {
          "type" : "array",
          "maxItems" : 2,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Message"
          }
        }
      },
      "required" : [ "Message" ],
      "additionalProperties" : False
    },
    "MessageGroupsList" : {
      "type" : "array",
      "minItems" : 1,
      "maxItems" : 5,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/MessageGroup"
      }
    },
    "PromptMaxRetries" : {
      "type" : "integer",
      "minimum" : 0,
      "maximum" : 5
    },
    "MessageSelectionStrategy" : {
      "type" : "string",
      "enum" : [ "Random", "Ordered" ]
    },
    "AllowedInputTypes" : {
      "type" : "object",
      "properties" : {
        "AllowAudioInput" : {
          "type" : "boolean"
        },
        "AllowDTMFInput" : {
          "type" : "boolean"
        }
      },
      "required" : [ "AllowAudioInput", "AllowDTMFInput" ],
      "additionalProperties" : False
    },
    "DTMFSpecification" : {
      "type" : "object",
      "properties" : {
        "DeletionCharacter" : {
          "type" : "string",
          "pattern" : "^[A-D0-9#*]{1}$"
        },
        "EndCharacter" : {
          "type" : "string",
          "pattern" : "^[A-D0-9#*]{1}$"
        },
        "EndTimeoutMs" : {
          "type" : "integer",
          "minimum" : 1
        },
        "MaxLength" : {
          "type" : "integer",
          "minimum" : 1,
          "maximum" : 1024
        }
      },
      "required" : [ "DeletionCharacter", "EndCharacter", "EndTimeoutMs", "MaxLength" ],
      "additionalProperties" : False
    },
    "AudioSpecification" : {
      "type" : "object",
      "properties" : {
        "EndTimeoutMs" : {
          "type" : "integer",
          "minimum" : 1
        },
        "MaxLengthMs" : {
          "type" : "integer",
          "minimum" : 1
        }
      },
      "required" : [ "EndTimeoutMs", "MaxLengthMs" ],
      "additionalProperties" : False
    },
    "AudioAndDTMFInputSpecification" : {
      "type" : "object",
      "properties" : {
        "StartTimeoutMs" : {
          "type" : "integer",
          "minimum" : 1
        },
        "DTMFSpecification" : {
          "$ref" : "#/definitions/DTMFSpecification"
        },
        "AudioSpecification" : {
          "$ref" : "#/definitions/AudioSpecification"
        }
      },
      "required" : [ "StartTimeoutMs" ],
      "additionalProperties" : False
    },
    "TextInputSpecification" : {
      "type" : "object",
      "properties" : {
        "StartTimeoutMs" : {
          "type" : "integer",
          "minimum" : 1
        }
      },
      "required" : [ "StartTimeoutMs" ],
      "additionalProperties" : False
    },
    "PromptAttemptSpecification" : {
      "type" : "object",
      "properties" : {
        "AllowedInputTypes" : {
          "$ref" : "#/definitions/AllowedInputTypes"
        },
        "AllowInterrupt" : {
          "type" : "boolean"
        },
        "AudioAndDTMFInputSpecification" : {
          "$ref" : "#/definitions/AudioAndDTMFInputSpecification"
        },
        "TextInputSpecification" : {
          "$ref" : "#/definitions/TextInputSpecification"
        }
      },
      "required" : [ "AllowedInputTypes" ],
      "additionalProperties" : False
    },
    "PromptSpecification" : {
      "type" : "object",
      "properties" : {
        "MessageGroupsList" : {
          "$ref" : "#/definitions/MessageGroupsList"
        },
        "MaxRetries" : {
          "$ref" : "#/definitions/PromptMaxRetries"
        },
        "AllowInterrupt" : {
          "type" : "boolean"
        },
        "MessageSelectionStrategy" : {
          "$ref" : "#/definitions/MessageSelectionStrategy"
        },
        "PromptAttemptsSpecification" : {
          "type" : "object",
          "patternProperties" : {
            "^(Initial|Retry1|Retry2|Retry3|Retry4|Retry5)$" : {
              "$ref" : "#/definitions/PromptAttemptSpecification"
            }
          },
          "additionalProperties" : False
        }
      },
      "required" : [ "MessageGroupsList", "MaxRetries" ],
      "additionalProperties" : False
    },
    "ResponseSpecification" : {
      "type" : "object",
      "properties" : {
        "MessageGroupsList" : {
          "$ref" : "#/definitions/MessageGroupsList"
        },
        "AllowInterrupt" : {
          "type" : "boolean"
        }
      },
      "required" : [ "MessageGroupsList" ],
      "additionalProperties" : False
    },
    "StillWaitingResponseFrequency" : {
      "type" : "integer",
      "minimum" : 1,
      "maximum" : 300
    },
    "StillWaitingResponseTimeout" : {
      "type" : "integer",
      "minimum" : 1,
      "maximum" : 900
    },
    "StillWaitingResponseSpecification" : {
      "type" : "object",
      "properties" : {
        "MessageGroupsList" : {
          "$ref" : "#/definitions/MessageGroupsList"
        },
        "FrequencyInSeconds" : {
          "$ref" : "#/definitions/StillWaitingResponseFrequency"
        },
        "TimeoutInSeconds" : {
          "$ref" : "#/definitions/StillWaitingResponseTimeout"
        },
        "AllowInterrupt" : {
          "type" : "boolean"
        }
      },
      "required" : [ "MessageGroupsList", "FrequencyInSeconds", "TimeoutInSeconds" ],
      "additionalProperties" : False
    },
    "IntentConfirmationSetting" : {
      "type" : "object",
      "properties" : {
        "PromptSpecification" : {
          "$ref" : "#/definitions/PromptSpecification"
        },
        "IsActive" : {
          "type" : "boolean"
        },
        "ConfirmationResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "ConfirmationNextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "ConfirmationConditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        },
        "DeclinationResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "DeclinationNextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "DeclinationConditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        },
        "FailureResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "FailureNextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "FailureConditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        },
        "CodeHook" : {
          "$ref" : "#/definitions/DialogCodeHookInvocationSetting"
        },
        "ElicitationCodeHook" : {
          "$ref" : "#/definitions/ElicitationCodeHookInvocationSetting"
        }
      },
      "required" : [ "PromptSpecification" ],
      "additionalProperties" : False
    },
    "IntentClosingSetting" : {
      "type" : "object",
      "properties" : {
        "ClosingResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "IsActive" : {
          "type" : "boolean"
        },
        "Conditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        },
        "NextStep" : {
          "$ref" : "#/definitions/DialogState"
        }
      },
      "additionalProperties" : False
    },
    "InputContext" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "$ref" : "#/definitions/Name"
        }
      },
      "required" : [ "Name" ],
      "additionalProperties" : False
    },
    "InputContextsList" : {
      "type" : "array",
      "maxItems" : 5,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/InputContext"
      }
    },
    "ContextTimeToLiveInSeconds" : {
      "type" : "integer",
      "minimum" : 5,
      "maximum" : 86400
    },
    "ContextTurnsToLive" : {
      "type" : "integer",
      "minimum" : 1,
      "maximum" : 20
    },
    "OutputContext" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "$ref" : "#/definitions/Name"
        },
        "TimeToLiveInSeconds" : {
          "$ref" : "#/definitions/ContextTimeToLiveInSeconds"
        },
        "TurnsToLive" : {
          "$ref" : "#/definitions/ContextTurnsToLive"
        }
      },
      "required" : [ "Name", "TimeToLiveInSeconds", "TurnsToLive" ],
      "additionalProperties" : False
    },
    "OutputContextsList" : {
      "type" : "array",
      "maxItems" : 10,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/OutputContext"
      }
    },
    "KendraIndexArn" : {
      "type" : "string",
      "minLength" : 32,
      "maxLength" : 2048,
      "pattern" : "^arn:aws[a-zA-Z-]*:kendra:[a-z]+-[a-z]+-[0-9]:[0-9]{12}:index/[a-zA-Z0-9][a-zA-Z0-9_-]*$"
    },
    "QueryFilterString" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 5000
    },
    "BedrockModelSpecification" : {
      "type" : "object",
      "properties" : {
        "ModelArn" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 5000
        },
        "BedrockGuardrailConfiguration" : {
          "type" : "object",
          "properties" : {
            "BedrockGuardrailIdentifier" : {
              "type" : "string",
              "minLength" : 1,
              "maxLength" : 5000
            },
            "BedrockGuardrailVersion" : {
              "type" : "string",
              "minLength" : 1,
              "maxLength" : 5000
            }
          },
          "additionalProperties" : False
        },
        "BedrockTraceStatus" : {
          "type" : "string",
          "enum" : [ "ENABLED", "DISABLED" ]
        },
        "BedrockModelCustomPrompt" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 5000
        }
      },
      "required" : [ "ModelArn" ],
      "additionalProperties" : False
    },
    "KendraConfiguration" : {
      "type" : "object",
      "properties" : {
        "KendraIndex" : {
          "$ref" : "#/definitions/KendraIndexArn"
        },
        "QueryFilterStringEnabled" : {
          "type" : "boolean"
        },
        "QueryFilterString" : {
          "$ref" : "#/definitions/QueryFilterString"
        }
      },
      "required" : [ "KendraIndex" ],
      "additionalProperties" : False
    },
    "QnAIntentConfiguration" : {
      "type" : "object",
      "properties" : {
        "DataSourceConfiguration" : {
          "type" : "object",
          "properties" : {
            "OpensearchConfiguration" : {
              "type" : "object",
              "properties" : {
                "DomainEndpoint" : {
                  "type" : "string",
                  "minLength" : 1,
                  "maxLength" : 5000
                },
                "IndexName" : {
                  "type" : "string",
                  "minLength" : 1,
                  "maxLength" : 5000
                },
                "IncludeFields" : {
                  "type" : "array",
                  "insertionOrder" : False,
                  "items" : {
                    "type" : "string",
                    "minLength" : 1,
                    "maxLength" : 5000
                  }
                },
                "ExactResponse" : {
                  "type" : "boolean"
                },
                "ExactResponseFields" : {
                  "type" : "object",
                  "properties" : {
                    "QuestionField" : {
                      "type" : "string",
                      "minLength" : 1,
                      "maxLength" : 5000
                    },
                    "AnswerField" : {
                      "type" : "string",
                      "minLength" : 1,
                      "maxLength" : 5000
                    }
                  },
                  "additionalProperties" : False
                }
              },
              "additionalProperties" : False
            },
            "BedrockKnowledgeStoreConfiguration" : {
              "type" : "object",
              "properties" : {
                "BedrockKnowledgeBaseArn" : {
                  "type" : "string",
                  "minLength" : 1,
                  "maxLength" : 5000
                },
                "ExactResponse" : {
                  "type" : "boolean"
                },
                "BKBExactResponseFields" : {
                  "type" : "object",
                  "properties" : {
                    "AnswerField" : {
                      "type" : "string",
                      "minLength" : 1,
                      "maxLength" : 5000
                    }
                  },
                  "additionalProperties" : False
                }
              },
              "additionalProperties" : False
            },
            "KendraConfiguration" : {
              "$ref" : "#/definitions/QnAKendraConfiguration"
            }
          },
          "additionalProperties" : False
        },
        "BedrockModelConfiguration" : {
          "$ref" : "#/definitions/BedrockModelSpecification"
        }
      },
      "required" : [ "DataSourceConfiguration", "BedrockModelConfiguration" ],
      "additionalProperties" : False
    },
    "QInConnectIntentConfiguration" : {
      "type" : "object",
      "properties" : {
        "QInConnectAssistantConfiguration" : {
          "type" : "object",
          "properties" : {
            "AssistantArn" : {
              "type" : "string",
              "minLength" : 1,
              "maxLength" : 200,
              "pattern" : "^arn:[a-z-]*?:wisdom:[a-z0-9-]*?:[0-9]{12}:[a-z-]*?/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}(?:/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}){0,2}$"
            }
          },
          "required" : [ "AssistantArn" ],
          "additionalProperties" : False
        }
      },
      "additionalProperties" : False
    },
    "QnAKendraConfiguration" : {
      "type" : "object",
      "properties" : {
        "KendraIndex" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 5000
        },
        "QueryFilterString" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 5000
        },
        "QueryFilterStringEnabled" : {
          "type" : "boolean"
        },
        "ExactResponse" : {
          "type" : "boolean"
        }
      },
      "required" : [ "KendraIndex", "QueryFilterStringEnabled", "ExactResponse" ],
      "additionalProperties" : False
    },
    "BedrockAgentIntentConfiguration" : {
      "type" : "object",
      "properties" : {
        "BedrockAgentConfiguration" : {
          "type" : "object",
          "properties" : {
            "BedrockAgentId" : {
              "type" : "string",
              "minLength" : 1,
              "maxLength" : 5000
            },
            "BedrockAgentAliasId" : {
              "type" : "string",
              "minLength" : 1,
              "maxLength" : 5000
            }
          },
          "additionalProperties" : False
        },
        "BedrockAgentIntentKnowledgeBaseConfiguration" : {
          "type" : "object",
          "properties" : {
            "BedrockKnowledgeBaseArn" : {
              "type" : "string",
              "minLength" : 1,
              "maxLength" : 5000
            },
            "BedrockModelConfiguration" : {
              "$ref" : "#/definitions/BedrockModelSpecification"
            }
          },
          "required" : [ "BedrockKnowledgeBaseArn", "BedrockModelConfiguration" ],
          "additionalProperties" : False
        }
      },
      "additionalProperties" : False
    },
    "PriorityValue" : {
      "type" : "integer",
      "minimum" : 0,
      "maximum" : 100
    },
    "SlotPriority" : {
      "type" : "object",
      "properties" : {
        "Priority" : {
          "$ref" : "#/definitions/PriorityValue"
        },
        "SlotName" : {
          "$ref" : "#/definitions/Name"
        }
      },
      "required" : [ "SlotName", "Priority" ],
      "additionalProperties" : False
    },
    "SlotPrioritiesList" : {
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/SlotPriority"
      }
    },
    "Intent" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "$ref" : "#/definitions/Name"
        },
        "Description" : {
          "description" : "Description of thr intent.",
          "$ref" : "#/definitions/Description"
        },
        "ParentIntentSignature" : {
          "$ref" : "#/definitions/ParentIntentSignature"
        },
        "SampleUtterances" : {
          "$ref" : "#/definitions/SampleUtterancesList"
        },
        "DialogCodeHook" : {
          "$ref" : "#/definitions/DialogCodeHookSetting"
        },
        "FulfillmentCodeHook" : {
          "$ref" : "#/definitions/FulfillmentCodeHookSetting"
        },
        "IntentConfirmationSetting" : {
          "$ref" : "#/definitions/IntentConfirmationSetting"
        },
        "IntentClosingSetting" : {
          "$ref" : "#/definitions/IntentClosingSetting"
        },
        "InitialResponseSetting" : {
          "$ref" : "#/definitions/InitialResponseSetting"
        },
        "InputContexts" : {
          "$ref" : "#/definitions/InputContextsList"
        },
        "OutputContexts" : {
          "$ref" : "#/definitions/OutputContextsList"
        },
        "KendraConfiguration" : {
          "$ref" : "#/definitions/KendraConfiguration"
        },
        "QnAIntentConfiguration" : {
          "$ref" : "#/definitions/QnAIntentConfiguration"
        },
        "QInConnectIntentConfiguration" : {
          "$ref" : "#/definitions/QInConnectIntentConfiguration"
        },
        "BedrockAgentIntentConfiguration" : {
          "$ref" : "#/definitions/BedrockAgentIntentConfiguration"
        },
        "SlotPriorities" : {
          "$ref" : "#/definitions/SlotPrioritiesList"
        },
        "Slots" : {
          "type" : "array",
          "maxItems" : 100,
          "uniqueItems" : True,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Slot"
          }
        }
      },
      "required" : [ "Name" ],
      "additionalProperties" : False
    },
    "ParentSlotTypeSignature" : {
      "type" : "string"
    },
    "SlotTypeName" : {
      "type" : "string"
    },
    "SampleValue" : {
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 140
        }
      },
      "required" : [ "Value" ],
      "additionalProperties" : False
    },
    "SynonymList" : {
      "type" : "array",
      "maxItems" : 10000,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/SampleValue"
      }
    },
    "SlotTypeValue" : {
      "type" : "object",
      "properties" : {
        "SampleValue" : {
          "$ref" : "#/definitions/SampleValue"
        },
        "Synonyms" : {
          "$ref" : "#/definitions/SynonymList"
        }
      },
      "required" : [ "SampleValue" ],
      "additionalProperties" : False
    },
    "SlotTypeValues" : {
      "type" : "array",
      "maxItems" : 10000,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/SlotTypeValue"
      }
    },
    "SlotValueResolutionStrategy" : {
      "type" : "string",
      "enum" : [ "ORIGINAL_VALUE", "TOP_RESOLUTION", "CONCATENATION" ]
    },
    "SlotValueRegexFilter" : {
      "type" : "object",
      "properties" : {
        "Pattern" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 300
        }
      },
      "required" : [ "Pattern" ],
      "additionalProperties" : False
    },
    "AudioRecognitionStrategy" : {
      "type" : "string",
      "enum" : [ "UseSlotValuesAsCustomVocabulary" ]
    },
    "AdvancedRecognitionSetting" : {
      "type" : "object",
      "properties" : {
        "AudioRecognitionStrategy" : {
          "$ref" : "#/definitions/AudioRecognitionStrategy"
        }
      },
      "additionalProperties" : False
    },
    "SlotValueSelectionSetting" : {
      "type" : "object",
      "properties" : {
        "ResolutionStrategy" : {
          "$ref" : "#/definitions/SlotValueResolutionStrategy"
        },
        "RegexFilter" : {
          "$ref" : "#/definitions/SlotValueRegexFilter"
        },
        "AdvancedRecognitionSetting" : {
          "$ref" : "#/definitions/AdvancedRecognitionSetting"
        }
      },
      "required" : [ "ResolutionStrategy" ],
      "additionalProperties" : False
    },
    "S3BucketName" : {
      "type" : "string",
      "minLength" : 3,
      "maxLength" : 63,
      "pattern" : "^[a-z0-9][\\.\\-a-z0-9]{1,61}[a-z0-9]$"
    },
    "S3ObjectKey" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 1024,
      "pattern" : "[\\.\\-\\!\\*\\_\\'\\(\\)a-zA-Z0-9][\\.\\-\\!\\*\\_\\'\\(\\)\\/a-zA-Z0-9]*$"
    },
    "GrammarSlotTypeSource" : {
      "type" : "object",
      "properties" : {
        "S3BucketName" : {
          "$ref" : "#/definitions/S3BucketName"
        },
        "S3ObjectKey" : {
          "$ref" : "#/definitions/S3ObjectKey"
        },
        "KmsKeyArn" : {
          "type" : "string",
          "minLength" : 20,
          "maxLength" : 2048,
          "pattern" : "^arn:[\\w\\-]+:kms:[\\w\\-]+:[\\d]{12}:(?:key\\/[\\w\\-]+|alias\\/[a-zA-Z0-9:\\/_\\-]{1,256})$"
        }
      },
      "required" : [ "S3BucketName", "S3ObjectKey" ],
      "additionalProperties" : False
    },
    "GrammarSlotTypeSetting" : {
      "type" : "object",
      "properties" : {
        "Source" : {
          "$ref" : "#/definitions/GrammarSlotTypeSource"
        }
      },
      "additionalProperties" : False
    },
    "ExternalSourceSetting" : {
      "type" : "object",
      "properties" : {
        "GrammarSlotTypeSetting" : {
          "$ref" : "#/definitions/GrammarSlotTypeSetting"
        }
      },
      "additionalProperties" : False
    },
    "CompositeSlotTypeSetting" : {
      "type" : "object",
      "properties" : {
        "SubSlots" : {
          "type" : "array",
          "minItems" : 1,
          "maxItems" : 6,
          "uniqueItems" : True,
          "insertionOrder" : True,
          "items" : {
            "$ref" : "#/definitions/SubSlotTypeComposition"
          }
        }
      },
      "additionalProperties" : False
    },
    "SubSlotTypeComposition" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 100,
          "pattern" : "^([0-9a-zA-Z][_-]?){1,100}$"
        },
        "SlotTypeId" : {
          "$ref" : "#/definitions/SlotTypeId"
        }
      },
      "required" : [ "Name", "SlotTypeId" ],
      "additionalProperties" : False
    },
    "SubSlotSetting" : {
      "type" : "object",
      "properties" : {
        "Expression" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 1000,
          "pattern" : "[0-9A-Za-z_\\-\\s\\(\\)]+"
        },
        "SlotSpecifications" : {
          "type" : "object",
          "minProperties" : 0,
          "maxProperties" : 6,
          "patternProperties" : {
            "^([0-9a-zA-Z][_-]?){1,100}$" : {
              "$ref" : "#/definitions/Specifications"
            }
          },
          "additionalProperties" : False
        }
      },
      "additionalProperties" : False
    },
    "Specifications" : {
      "type" : "object",
      "properties" : {
        "SlotTypeId" : {
          "$ref" : "#/definitions/SlotTypeId"
        },
        "ValueElicitationSetting" : {
          "$ref" : "#/definitions/SubSlotValueElicitationSetting"
        }
      },
      "required" : [ "SlotTypeId", "ValueElicitationSetting" ],
      "additionalProperties" : False
    },
    "SlotTypeId" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 25,
      "pattern" : "^((AMAZON\\.)[a-zA-Z_]+?|[0-9a-zA-Z]+)$"
    },
    "SubSlotValueElicitationSetting" : {
      "type" : "object",
      "properties" : {
        "PromptSpecification" : {
          "$ref" : "#/definitions/PromptSpecification"
        },
        "DefaultValueSpecification" : {
          "$ref" : "#/definitions/SlotDefaultValueSpecification"
        },
        "SampleUtterances" : {
          "$ref" : "#/definitions/SampleUtterancesList"
        },
        "WaitAndContinueSpecification" : {
          "$ref" : "#/definitions/WaitAndContinueSpecification"
        }
      },
      "additionalProperties" : False
    },
    "SlotType" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "$ref" : "#/definitions/Name"
        },
        "Description" : {
          "$ref" : "#/definitions/Description"
        },
        "ParentSlotTypeSignature" : {
          "$ref" : "#/definitions/ParentSlotTypeSignature"
        },
        "SlotTypeValues" : {
          "$ref" : "#/definitions/SlotTypeValues"
        },
        "ValueSelectionSetting" : {
          "$ref" : "#/definitions/SlotValueSelectionSetting"
        },
        "ExternalSourceSetting" : {
          "$ref" : "#/definitions/ExternalSourceSetting"
        },
        "CompositeSlotTypeSetting" : {
          "$ref" : "#/definitions/CompositeSlotTypeSetting"
        }
      },
      "required" : [ "Name" ],
      "additionalProperties" : False
    },
    "CustomVocabularyItem" : {
      "type" : "object",
      "properties" : {
        "Phrase" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 100
        },
        "Weight" : {
          "type" : "integer",
          "minimum" : 0,
          "maximum" : 3
        },
        "DisplayAs" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 100
        }
      },
      "required" : [ "Phrase" ],
      "additionalProperties" : False
    },
    "CustomVocabularyItems" : {
      "type" : "array",
      "maxItems" : 500,
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/CustomVocabularyItem"
      }
    },
    "CustomVocabulary" : {
      "type" : "object",
      "properties" : {
        "CustomVocabularyItems" : {
          "$ref" : "#/definitions/CustomVocabularyItems"
        }
      },
      "required" : [ "CustomVocabularyItems" ],
      "additionalProperties" : False
    },
    "SlotDefaultValue" : {
      "type" : "object",
      "properties" : {
        "DefaultValue" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 202
        }
      },
      "required" : [ "DefaultValue" ],
      "additionalProperties" : False
    },
    "SlotDefaultValueSpecification" : {
      "type" : "object",
      "properties" : {
        "DefaultValueList" : {
          "type" : "array",
          "maxItems" : 10,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/SlotDefaultValue"
          }
        }
      },
      "required" : [ "DefaultValueList" ],
      "additionalProperties" : False
    },
    "SlotConstraint" : {
      "type" : "string",
      "enum" : [ "Required", "Optional" ]
    },
    "WaitAndContinueSpecification" : {
      "type" : "object",
      "properties" : {
        "WaitingResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "ContinueResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "StillWaitingResponse" : {
          "$ref" : "#/definitions/StillWaitingResponseSpecification"
        },
        "IsActive" : {
          "type" : "boolean"
        }
      },
      "required" : [ "WaitingResponse", "ContinueResponse" ],
      "additionalProperties" : False
    },
    "SlotValueElicitationSetting" : {
      "type" : "object",
      "properties" : {
        "DefaultValueSpecification" : {
          "$ref" : "#/definitions/SlotDefaultValueSpecification"
        },
        "SlotConstraint" : {
          "$ref" : "#/definitions/SlotConstraint"
        },
        "PromptSpecification" : {
          "$ref" : "#/definitions/PromptSpecification"
        },
        "SampleUtterances" : {
          "$ref" : "#/definitions/SampleUtterancesList"
        },
        "WaitAndContinueSpecification" : {
          "$ref" : "#/definitions/WaitAndContinueSpecification"
        },
        "SlotCaptureSetting" : {
          "$ref" : "#/definitions/SlotCaptureSetting"
        }
      },
      "required" : [ "SlotConstraint" ],
      "additionalProperties" : False
    },
    "ObfuscationSetting" : {
      "type" : "object",
      "properties" : {
        "ObfuscationSettingType" : {
          "type" : "string",
          "enum" : [ "None", "DefaultObfuscation" ]
        }
      },
      "required" : [ "ObfuscationSettingType" ],
      "additionalProperties" : False
    },
    "MultipleValuesSetting" : {
      "type" : "object",
      "properties" : {
        "AllowMultipleValues" : {
          "type" : "boolean"
        }
      },
      "required" : [ ],
      "additionalProperties" : False
    },
    "Slot" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "$ref" : "#/definitions/Name"
        },
        "Description" : {
          "$ref" : "#/definitions/Description"
        },
        "SlotTypeName" : {
          "$ref" : "#/definitions/SlotTypeName"
        },
        "ValueElicitationSetting" : {
          "$ref" : "#/definitions/SlotValueElicitationSetting"
        },
        "ObfuscationSetting" : {
          "$ref" : "#/definitions/ObfuscationSetting"
        },
        "MultipleValuesSetting" : {
          "$ref" : "#/definitions/MultipleValuesSetting"
        },
        "SubSlotSetting" : {
          "$ref" : "#/definitions/SubSlotSetting"
        }
      },
      "required" : [ "Name", "SlotTypeName", "ValueElicitationSetting" ],
      "additionalProperties" : False
    },
    "BotLocale" : {
      "type" : "object",
      "properties" : {
        "LocaleId" : {
          "$ref" : "#/definitions/LocaleId"
        },
        "Description" : {
          "$ref" : "#/definitions/Description"
        },
        "VoiceSettings" : {
          "$ref" : "#/definitions/VoiceSettings"
        },
        "NluConfidenceThreshold" : {
          "$ref" : "#/definitions/ConfidenceThreshold"
        },
        "Intents" : {
          "type" : "array",
          "maxItems" : 1000,
          "uniqueItems" : True,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/Intent"
          }
        },
        "SlotTypes" : {
          "type" : "array",
          "maxItems" : 250,
          "uniqueItems" : True,
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/SlotType"
          }
        },
        "CustomVocabulary" : {
          "$ref" : "#/definitions/CustomVocabulary"
        }
      },
      "required" : [ "LocaleId", "NluConfidenceThreshold" ],
      "additionalProperties" : False
    },
    "S3Location" : {
      "type" : "object",
      "properties" : {
        "S3Bucket" : {
          "$ref" : "#/definitions/S3BucketName"
        },
        "S3ObjectKey" : {
          "$ref" : "#/definitions/S3ObjectKey"
        },
        "S3ObjectVersion" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 1024
        }
      },
      "required" : [ "S3Bucket", "S3ObjectKey" ],
      "additionalProperties" : False
    },
    "Condition" : {
      "type" : "object",
      "properties" : {
        "ExpressionString" : {
          "$ref" : "#/definitions/ConditionExpression"
        }
      },
      "required" : [ "ExpressionString" ],
      "additionalProperties" : False
    },
    "Conditional" : {
      "type" : "object",
      "properties" : {
        "IsActive" : {
          "type" : "boolean"
        },
        "ConditionalBranches" : {
          "$ref" : "#/definitions/ConditionalBranches"
        }
      },
      "required" : [ "IsActive", "ConditionalBranches" ],
      "additionalProperties" : False
    },
    "ConditionalSpecification" : {
      "type" : "object",
      "properties" : {
        "IsActive" : {
          "type" : "boolean"
        },
        "ConditionalBranches" : {
          "$ref" : "#/definitions/ConditionalBranches"
        },
        "DefaultBranch" : {
          "$ref" : "#/definitions/DefaultConditionalBranch"
        }
      },
      "required" : [ "IsActive", "ConditionalBranches", "DefaultBranch" ],
      "additionalProperties" : False
    },
    "DefaultConditionalBranch" : {
      "type" : "object",
      "properties" : {
        "NextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "Response" : {
          "$ref" : "#/definitions/ResponseSpecification"
        }
      },
      "additionalProperties" : False
    },
    "ConditionalBranch" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "$ref" : "#/definitions/Name"
        },
        "Condition" : {
          "$ref" : "#/definitions/Condition"
        },
        "NextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "Response" : {
          "$ref" : "#/definitions/ResponseSpecification"
        }
      },
      "required" : [ "Name", "Condition", "NextStep" ],
      "additionalProperties" : False
    },
    "ConditionalBranches" : {
      "type" : "array",
      "minItems" : 1,
      "maxItems" : 4,
      "insertionOrder" : True,
      "items" : {
        "$ref" : "#/definitions/ConditionalBranch"
      }
    },
    "InitialResponseSetting" : {
      "type" : "object",
      "properties" : {
        "InitialResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "NextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "Conditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        },
        "CodeHook" : {
          "$ref" : "#/definitions/DialogCodeHookInvocationSetting"
        }
      },
      "additionalProperties" : False
    },
    "ConditionExpression" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 1024
    },
    "DialogCodeHookInvocationSetting" : {
      "type" : "object",
      "properties" : {
        "EnableCodeHookInvocation" : {
          "type" : "boolean"
        },
        "IsActive" : {
          "type" : "boolean"
        },
        "InvocationLabel" : {
          "$ref" : "#/definitions/Name"
        },
        "PostCodeHookSpecification" : {
          "$ref" : "#/definitions/PostDialogCodeHookInvocationSpecification"
        }
      },
      "required" : [ "IsActive", "EnableCodeHookInvocation", "PostCodeHookSpecification" ],
      "additionalProperties" : False
    },
    "ElicitationCodeHookInvocationSetting" : {
      "type" : "object",
      "properties" : {
        "EnableCodeHookInvocation" : {
          "type" : "boolean"
        },
        "InvocationLabel" : {
          "$ref" : "#/definitions/Name"
        }
      },
      "required" : [ "EnableCodeHookInvocation" ],
      "additionalProperties" : False
    },
    "PostDialogCodeHookInvocationSpecification" : {
      "type" : "object",
      "properties" : {
        "SuccessResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "SuccessNextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "SuccessConditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        },
        "FailureResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "FailureNextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "FailureConditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        },
        "TimeoutResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "TimeoutNextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "TimeoutConditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        }
      },
      "additionalProperties" : False
    },
    "DialogState" : {
      "type" : "object",
      "properties" : {
        "DialogAction" : {
          "$ref" : "#/definitions/DialogAction"
        },
        "Intent" : {
          "$ref" : "#/definitions/IntentOverride"
        },
        "SessionAttributes" : {
          "type" : "array",
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/SessionAttribute"
          }
        }
      },
      "additionalProperties" : False
    },
    "DialogAction" : {
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/DialogActionType"
        },
        "SlotToElicit" : {
          "$ref" : "#/definitions/Name"
        },
        "SuppressNextMessage" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Type" ],
      "additionalProperties" : False
    },
    "DialogActionType" : {
      "type" : "string",
      "enum" : [ "CloseIntent", "ConfirmIntent", "ElicitIntent", "ElicitSlot", "StartIntent", "FulfillIntent", "EndConversation", "EvaluateConditional", "InvokeDialogCodeHook" ]
    },
    "SessionAttribute" : {
      "type" : "object",
      "properties" : {
        "Key" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 1024
        },
        "Value" : {
          "type" : "string",
          "minLength" : 0,
          "maxLength" : 1024
        }
      },
      "required" : [ "Key" ],
      "additionalProperties" : False
    },
    "IntentOverride" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "$ref" : "#/definitions/Name"
        },
        "Slots" : {
          "type" : "array",
          "insertionOrder" : False,
          "items" : {
            "$ref" : "#/definitions/SlotValueOverrideMap"
          }
        }
      },
      "additionalProperties" : False
    },
    "SlotValueOverrideMap" : {
      "type" : "object",
      "properties" : {
        "SlotName" : {
          "$ref" : "#/definitions/Name"
        },
        "SlotValueOverride" : {
          "$ref" : "#/definitions/SlotValueOverride"
        }
      },
      "additionalProperties" : False
    },
    "SlotValueOverride" : {
      "type" : "object",
      "properties" : {
        "Shape" : {
          "$ref" : "#/definitions/SlotShape"
        },
        "Value" : {
          "$ref" : "#/definitions/SlotValue"
        },
        "Values" : {
          "$ref" : "#/definitions/SlotValues"
        }
      },
      "additionalProperties" : False
    },
    "SlotValue" : {
      "type" : "object",
      "properties" : {
        "InterpretedValue" : {
          "type" : "string",
          "minLength" : 1,
          "maxLength" : 202
        }
      },
      "additionalProperties" : False
    },
    "SlotValues" : {
      "type" : "array",
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/SlotValueOverride"
      }
    },
    "SlotShape" : {
      "type" : "string",
      "enum" : [ "Scalar", "List" ]
    },
    "SlotCaptureSetting" : {
      "type" : "object",
      "properties" : {
        "CaptureResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "CaptureNextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "CaptureConditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        },
        "FailureResponse" : {
          "$ref" : "#/definitions/ResponseSpecification"
        },
        "FailureNextStep" : {
          "$ref" : "#/definitions/DialogState"
        },
        "FailureConditional" : {
          "$ref" : "#/definitions/ConditionalSpecification"
        },
        "CodeHook" : {
          "$ref" : "#/definitions/DialogCodeHookInvocationSetting"
        },
        "ElicitationCodeHook" : {
          "$ref" : "#/definitions/ElicitationCodeHookInvocationSetting"
        }
      },
      "additionalProperties" : False
    }
  },
  "properties" : {
    "Id" : {
      "$ref" : "#/definitions/Id"
    },
    "Arn" : {
      "$ref" : "#/definitions/BotArn"
    },
    "Name" : {
      "$ref" : "#/definitions/Name"
    },
    "Description" : {
      "$ref" : "#/definitions/Description"
    },
    "RoleArn" : {
      "$ref" : "#/definitions/RoleArn"
    },
    "DataPrivacy" : {
      "type" : "object",
      "properties" : {
        "ChildDirected" : {
          "type" : "boolean"
        }
      },
      "required" : [ "ChildDirected" ],
      "additionalProperties" : False
    },
    "IdleSessionTTLInSeconds" : {
      "type" : "integer",
      "minimum" : 60,
      "maximum" : 86400
    },
    "BotLocales" : {
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/BotLocale"
      }
    },
    "BotFileS3Location" : {
      "$ref" : "#/definitions/S3Location"
    },
    "BotTags" : {
      "type" : "array",
      "uniqueItems" : True,
      "maxItems" : 200,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "TestBotAliasTags" : {
      "type" : "array",
      "uniqueItems" : True,
      "maxItems" : 200,
      "insertionOrder" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    },
    "AutoBuildBotLocales" : {
      "type" : "boolean"
    },
    "TestBotAliasSettings" : {
      "$ref" : "#/definitions/TestBotAliasSettings"
    },
    "Replication" : {
      "$ref" : "#/definitions/Replication"
    }
  },
  "taggable" : True,
  "additionalProperties" : False,
  "required" : [ "Name", "RoleArn", "DataPrivacy", "IdleSessionTTLInSeconds" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Arn" ],
  "writeOnlyProperties" : [ "/properties/BotLocales", "/properties/BotFileS3Location", "/properties/AutoBuildBotLocales", "/properties/BotTags", "/properties/TestBotAliasTags", "/properties/Replication" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iam:PassRole", "lex:DescribeBot", "lex:CreateUploadUrl", "lex:StartImport", "lex:DescribeImport", "lex:ListTagsForResource", "lex:TagResource", "lex:CreateBot", "lex:CreateBotLocale", "lex:CreateIntent", "lex:CreateSlot", "lex:CreateSlotType", "lex:UpdateBot", "lex:UpdateBotLocale", "lex:UpdateIntent", "lex:UpdateSlot", "lex:UpdateSlotType", "lex:DeleteBotLocale", "lex:DeleteIntent", "lex:DeleteSlot", "lex:DeleteSlotType", "lex:DescribeBotLocale", "lex:BuildBotLocale", "lex:ListBots", "lex:ListBotLocales", "lex:CreateCustomVocabulary", "lex:UpdateCustomVocabulary", "lex:DeleteCustomVocabulary", "s3:GetObject", "lex:UpdateBotAlias", "iam:CreateServiceLinkedRole", "iam:GetRole", "lex:CreateBotReplica", "lex:DescribeBotReplica", "lex:DeleteBotReplica" ]
    },
    "read" : {
      "permissions" : [ "lex:DescribeBot", "lex:ListTagsForResource", "lex:DescribeBotReplica" ]
    },
    "update" : {
      "permissions" : [ "iam:PassRole", "lex:DescribeBot", "lex:CreateUploadUrl", "lex:StartImport", "lex:DescribeImport", "lex:ListTagsForResource", "lex:TagResource", "lex:UntagResource", "lex:CreateBot", "lex:CreateBotLocale", "lex:CreateIntent", "lex:CreateSlot", "lex:CreateSlotType", "lex:UpdateBot", "lex:UpdateBotLocale", "lex:UpdateIntent", "lex:UpdateSlot", "lex:UpdateSlotType", "lex:DeleteBotLocale", "lex:DeleteIntent", "lex:DeleteSlot", "lex:DeleteSlotType", "lex:DescribeBotLocale", "lex:BuildBotLocale", "lex:ListBots", "lex:ListBotLocales", "lex:CreateCustomVocabulary", "lex:UpdateCustomVocabulary", "lex:DeleteCustomVocabulary", "s3:GetObject", "lex:UpdateBotAlias", "lex:CreateBotReplica", "lex:DescribeBotReplica", "lex:DeleteBotReplica" ]
    },
    "delete" : {
      "permissions" : [ "lex:DeleteBot", "lex:DescribeBot", "lex:DeleteBotLocale", "lex:DeleteIntent", "lex:DeleteSlotType", "lex:DeleteSlot", "lex:DeleteBotVersion", "lex:DeleteBotChannel", "lex:DeleteBotAlias", "lex:DeleteCustomVocabulary", "lex:DeleteBotReplica" ]
    },
    "list" : {
      "permissions" : [ "lex:ListBots", "lex:ListBotReplicas" ]
    }
  }
}