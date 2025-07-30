SCHEMA = {
  "typeName" : "AWS::Personalize::Solution",
  "description" : "Resource schema for AWS::Personalize::Solution.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-personalize",
  "definitions" : {
    "SolutionArn" : {
      "description" : "The ARN of the solution",
      "type" : "string",
      "maxLength" : 256,
      "pattern" : "arn:([a-z\\d-]+):personalize:.*:.*:.+"
    },
    "CategoricalHyperParameterRange" : {
      "description" : "Provides the name and values of a Categorical hyperparameter.",
      "type" : "object",
      "properties" : {
        "Name" : {
          "description" : "The name of the hyperparameter.",
          "type" : "string",
          "maxLength" : 256
        },
        "Values" : {
          "description" : "A list of the categories for the hyperparameter.",
          "type" : "array",
          "items" : {
            "type" : "string",
            "maxLength" : 1000
          },
          "maxItems" : 100,
          "insertionOrder" : True
        }
      },
      "additionalProperties" : False
    },
    "ContinuousHyperParameterRange" : {
      "description" : "Provides the name and range of a continuous hyperparameter.",
      "type" : "object",
      "properties" : {
        "Name" : {
          "description" : "The name of the hyperparameter.",
          "type" : "string",
          "maxLength" : 256
        },
        "MinValue" : {
          "description" : "The minimum allowable value for the hyperparameter.",
          "type" : "number",
          "minimum" : -1000000
        },
        "MaxValue" : {
          "description" : "The maximum allowable value for the hyperparameter.",
          "type" : "number",
          "minimum" : -1000000
        }
      },
      "additionalProperties" : False
    },
    "IntegerHyperParameterRange" : {
      "description" : "Provides the name and range of an integer-valued hyperparameter.",
      "type" : "object",
      "properties" : {
        "Name" : {
          "description" : "The name of the hyperparameter.",
          "type" : "string",
          "maxLength" : 256
        },
        "MinValue" : {
          "description" : "The minimum allowable value for the hyperparameter.",
          "type" : "integer",
          "minimum" : -1000000
        },
        "MaxValue" : {
          "description" : "The maximum allowable value for the hyperparameter.",
          "type" : "integer",
          "maximum" : 1000000
        }
      },
      "additionalProperties" : False
    },
    "SolutionConfig" : {
      "type" : "object",
      "description" : "The configuration to use with the solution. When performAutoML is set to True, Amazon Personalize only evaluates the autoMLConfig section of the solution configuration.",
      "properties" : {
        "AlgorithmHyperParameters" : {
          "description" : "Lists the hyperparameter names and ranges.",
          "type" : "object",
          "patternProperties" : {
            ".{1,}" : {
              "type" : "string"
            }
          },
          "maxProperties" : 100,
          "additionalProperties" : False
        },
        "AutoMLConfig" : {
          "description" : "The AutoMLConfig object containing a list of recipes to search when AutoML is performed.",
          "type" : "object",
          "properties" : {
            "MetricName" : {
              "description" : "The metric to optimize.",
              "type" : "string",
              "maxLength" : 256
            },
            "RecipeList" : {
              "description" : "The list of candidate recipes.",
              "type" : "array",
              "items" : {
                "type" : "string",
                "maxLength" : 256,
                "pattern" : "arn:([a-z\\d-]+):personalize:.*:.*:.+"
              },
              "insertionOrder" : True,
              "maxItems" : 100
            }
          },
          "additionalProperties" : False
        },
        "EventValueThreshold" : {
          "description" : "Only events with a value greater than or equal to this threshold are used for training a model.",
          "type" : "string",
          "maxLength" : 256
        },
        "FeatureTransformationParameters" : {
          "description" : "Lists the feature transformation parameters.",
          "type" : "object",
          "patternProperties" : {
            ".{1,}" : {
              "type" : "string"
            }
          },
          "maxProperties" : 100,
          "additionalProperties" : False
        },
        "HpoConfig" : {
          "description" : "Describes the properties for hyperparameter optimization (HPO)",
          "type" : "object",
          "properties" : {
            "AlgorithmHyperParameterRanges" : {
              "description" : "The hyperparameters and their allowable ranges",
              "type" : "object",
              "properties" : {
                "CategoricalHyperParameterRanges" : {
                  "description" : "The categorical hyperparameters and their ranges.",
                  "type" : "array",
                  "maxItems" : 100,
                  "items" : {
                    "$ref" : "#/definitions/CategoricalHyperParameterRange"
                  },
                  "insertionOrder" : True
                },
                "ContinuousHyperParameterRanges" : {
                  "description" : "The continuous hyperparameters and their ranges.",
                  "type" : "array",
                  "maxItems" : 100,
                  "items" : {
                    "$ref" : "#/definitions/ContinuousHyperParameterRange"
                  },
                  "insertionOrder" : True
                },
                "IntegerHyperParameterRanges" : {
                  "description" : "The integer hyperparameters and their ranges.",
                  "type" : "array",
                  "maxItems" : 100,
                  "items" : {
                    "$ref" : "#/definitions/IntegerHyperParameterRange"
                  },
                  "insertionOrder" : True
                }
              },
              "additionalProperties" : False
            },
            "HpoObjective" : {
              "description" : "The metric to optimize during HPO.",
              "type" : "object",
              "properties" : {
                "MetricName" : {
                  "description" : "The name of the metric",
                  "type" : "string",
                  "maxLength" : 256
                },
                "Type" : {
                  "description" : "The type of the metric. Valid values are Maximize and Minimize.",
                  "type" : "string",
                  "enum" : [ "Maximize", "Minimize" ]
                },
                "MetricRegex" : {
                  "description" : "A regular expression for finding the metric in the training job logs.",
                  "type" : "string",
                  "maxLength" : 256
                }
              },
              "additionalProperties" : False
            },
            "HpoResourceConfig" : {
              "description" : "Describes the resource configuration for hyperparameter optimization (HPO).",
              "type" : "object",
              "properties" : {
                "MaxNumberOfTrainingJobs" : {
                  "description" : "The maximum number of training jobs when you create a solution version. The maximum value for maxNumberOfTrainingJobs is 40.",
                  "type" : "string",
                  "maxLength" : 256
                },
                "MaxParallelTrainingJobs" : {
                  "description" : "The maximum number of parallel training jobs when you create a solution version. The maximum value for maxParallelTrainingJobs is 10.",
                  "type" : "string",
                  "maxLength" : 256
                }
              },
              "additionalProperties" : False
            }
          },
          "additionalProperties" : False
        }
      },
      "additionalProperties" : False
    }
  },
  "properties" : {
    "Name" : {
      "description" : "The name for the solution",
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 63,
      "pattern" : "^[a-zA-Z0-9][a-zA-Z0-9\\-_]*"
    },
    "SolutionArn" : {
      "$ref" : "#/definitions/SolutionArn"
    },
    "EventType" : {
      "description" : "When your have multiple event types (using an EVENT_TYPE schema field), this parameter specifies which event type (for example, 'click' or 'like') is used for training the model. If you do not provide an eventType, Amazon Personalize will use all interactions for training with equal weight regardless of type.",
      "type" : "string",
      "maxLength" : 256
    },
    "DatasetGroupArn" : {
      "description" : "The ARN of the dataset group that provides the training data.",
      "type" : "string",
      "maxLength" : 256,
      "pattern" : "arn:([a-z\\d-]+):personalize:.*:.*:.+"
    },
    "PerformAutoML" : {
      "description" : "Whether to perform automated machine learning (AutoML). The default is False. For this case, you must specify recipeArn.",
      "type" : "boolean"
    },
    "PerformHPO" : {
      "description" : "Whether to perform hyperparameter optimization (HPO) on the specified or selected recipe. The default is False. When performing AutoML, this parameter is always True and you should not set it to false.",
      "type" : "boolean"
    },
    "RecipeArn" : {
      "description" : "The ARN of the recipe to use for model training. Only specified when performAutoML is False.",
      "type" : "string",
      "maxLength" : 256,
      "pattern" : "arn:([a-z\\d-]+):personalize:.*:.*:.+"
    },
    "SolutionConfig" : {
      "$ref" : "#/definitions/SolutionConfig"
    }
  },
  "additionalProperties" : False,
  "required" : [ "Name", "DatasetGroupArn" ],
  "createOnlyProperties" : [ "/properties/Name", "/properties/EventType", "/properties/DatasetGroupArn", "/properties/PerformAutoML", "/properties/PerformHPO", "/properties/RecipeArn", "/properties/SolutionConfig" ],
  "taggable" : False,
  "readOnlyProperties" : [ "/properties/SolutionArn" ],
  "primaryIdentifier" : [ "/properties/SolutionArn" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "personalize:CreateSolution", "personalize:DescribeSolution" ]
    },
    "read" : {
      "permissions" : [ "personalize:DescribeSolution" ]
    },
    "delete" : {
      "permissions" : [ "personalize:DeleteSolution", "personalize:DescribeSolution" ]
    },
    "list" : {
      "permissions" : [ "personalize:ListSolutions" ]
    }
  }
}