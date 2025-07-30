SCHEMA = {
  "typeName" : "AWS::Budgets::Budget",
  "description" : "Resource Type definition for AWS::Budgets::Budget",
  "additionalProperties" : False,
  "properties" : {
    "Budget" : {
      "$ref" : "#/definitions/BudgetData"
    },
    "Id" : {
      "type" : "string"
    },
    "NotificationsWithSubscribers" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/NotificationWithSubscribers"
      }
    },
    "ResourceTags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/ResourceTag"
      }
    }
  },
  "definitions" : {
    "HistoricalOptions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "BudgetAdjustmentPeriod" : {
          "type" : "integer"
        }
      },
      "required" : [ "BudgetAdjustmentPeriod" ]
    },
    "CostCategoryValues" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Values" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Key" : {
          "type" : "string"
        },
        "MatchOptions" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "BudgetData" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Metrics" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "BudgetLimit" : {
          "$ref" : "#/definitions/Spend"
        },
        "TimePeriod" : {
          "$ref" : "#/definitions/TimePeriod"
        },
        "AutoAdjustData" : {
          "$ref" : "#/definitions/AutoAdjustData"
        },
        "TimeUnit" : {
          "type" : "string"
        },
        "PlannedBudgetLimits" : {
          "type" : "object"
        },
        "CostFilters" : {
          "type" : "object"
        },
        "FilterExpression" : {
          "$ref" : "#/definitions/Expression"
        },
        "BudgetName" : {
          "type" : "string"
        },
        "CostTypes" : {
          "$ref" : "#/definitions/CostTypes"
        },
        "BudgetType" : {
          "type" : "string"
        }
      },
      "required" : [ "TimeUnit", "BudgetType" ]
    },
    "TimePeriod" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Start" : {
          "type" : "string"
        },
        "End" : {
          "type" : "string"
        }
      }
    },
    "NotificationWithSubscribers" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Subscribers" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Subscriber"
          }
        },
        "Notification" : {
          "$ref" : "#/definitions/Notification"
        }
      },
      "required" : [ "Subscribers", "Notification" ]
    },
    "Notification" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ComparisonOperator" : {
          "type" : "string"
        },
        "NotificationType" : {
          "type" : "string"
        },
        "Threshold" : {
          "type" : "number"
        },
        "ThresholdType" : {
          "type" : "string"
        }
      },
      "required" : [ "ComparisonOperator", "NotificationType", "Threshold" ]
    },
    "CostTypes" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IncludeSupport" : {
          "type" : "boolean"
        },
        "IncludeOtherSubscription" : {
          "type" : "boolean"
        },
        "IncludeTax" : {
          "type" : "boolean"
        },
        "IncludeSubscription" : {
          "type" : "boolean"
        },
        "UseBlended" : {
          "type" : "boolean"
        },
        "IncludeUpfront" : {
          "type" : "boolean"
        },
        "IncludeDiscount" : {
          "type" : "boolean"
        },
        "IncludeCredit" : {
          "type" : "boolean"
        },
        "IncludeRecurring" : {
          "type" : "boolean"
        },
        "UseAmortized" : {
          "type" : "boolean"
        },
        "IncludeRefund" : {
          "type" : "boolean"
        }
      }
    },
    "TagValues" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Values" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Key" : {
          "type" : "string"
        },
        "MatchOptions" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "ResourceTag" : {
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
      "required" : [ "Key" ]
    },
    "Subscriber" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Address" : {
          "type" : "string"
        },
        "SubscriptionType" : {
          "type" : "string"
        }
      },
      "required" : [ "SubscriptionType", "Address" ]
    },
    "Expression" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Not" : {
          "$ref" : "#/definitions/Expression"
        },
        "Or" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Expression"
          }
        },
        "And" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Expression"
          }
        },
        "Dimensions" : {
          "$ref" : "#/definitions/ExpressionDimensionValues"
        },
        "CostCategories" : {
          "$ref" : "#/definitions/CostCategoryValues"
        },
        "Tags" : {
          "$ref" : "#/definitions/TagValues"
        }
      }
    },
    "Spend" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Unit" : {
          "type" : "string"
        },
        "Amount" : {
          "type" : "number"
        }
      },
      "required" : [ "Amount", "Unit" ]
    },
    "AutoAdjustData" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AutoAdjustType" : {
          "type" : "string"
        },
        "HistoricalOptions" : {
          "$ref" : "#/definitions/HistoricalOptions"
        }
      },
      "required" : [ "AutoAdjustType" ]
    },
    "ExpressionDimensionValues" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Values" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "Key" : {
          "type" : "string"
        },
        "MatchOptions" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    }
  },
  "required" : [ "Budget" ],
  "createOnlyProperties" : [ "/properties/NotificationsWithSubscribers" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}