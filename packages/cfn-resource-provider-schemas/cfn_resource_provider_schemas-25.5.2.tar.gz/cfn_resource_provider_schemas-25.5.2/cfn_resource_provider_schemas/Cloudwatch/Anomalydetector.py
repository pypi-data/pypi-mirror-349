SCHEMA = {
  "typeName" : "AWS::CloudWatch::AnomalyDetector",
  "description" : "Resource Type definition for AWS::CloudWatch::AnomalyDetector",
  "additionalProperties" : False,
  "properties" : {
    "MetricCharacteristics" : {
      "$ref" : "#/definitions/MetricCharacteristics"
    },
    "MetricName" : {
      "type" : "string"
    },
    "Stat" : {
      "type" : "string"
    },
    "Configuration" : {
      "$ref" : "#/definitions/Configuration"
    },
    "MetricMathAnomalyDetector" : {
      "$ref" : "#/definitions/MetricMathAnomalyDetector"
    },
    "Dimensions" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Dimension"
      }
    },
    "Id" : {
      "type" : "string"
    },
    "Namespace" : {
      "type" : "string"
    },
    "SingleMetricAnomalyDetector" : {
      "$ref" : "#/definitions/SingleMetricAnomalyDetector"
    }
  },
  "definitions" : {
    "MetricCharacteristics" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PeriodicSpikes" : {
          "type" : "boolean"
        }
      }
    },
    "MetricMathAnomalyDetector" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MetricDataQueries" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/MetricDataQuery"
          }
        }
      }
    },
    "Configuration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MetricTimeZone" : {
          "type" : "string"
        },
        "ExcludedTimeRanges" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Range"
          }
        }
      }
    },
    "MetricStat" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Period" : {
          "type" : "integer"
        },
        "Metric" : {
          "$ref" : "#/definitions/Metric"
        },
        "Stat" : {
          "type" : "string"
        },
        "Unit" : {
          "type" : "string"
        }
      },
      "required" : [ "Stat", "Period", "Metric" ]
    },
    "Metric" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MetricName" : {
          "type" : "string"
        },
        "Dimensions" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Dimension"
          }
        },
        "Namespace" : {
          "type" : "string"
        }
      },
      "required" : [ "MetricName", "Namespace" ]
    },
    "Dimension" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Name" ]
    },
    "MetricDataQuery" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AccountId" : {
          "type" : "string"
        },
        "ReturnData" : {
          "type" : "boolean"
        },
        "Expression" : {
          "type" : "string"
        },
        "MetricStat" : {
          "$ref" : "#/definitions/MetricStat"
        },
        "Label" : {
          "type" : "string"
        },
        "Period" : {
          "type" : "integer"
        },
        "Id" : {
          "type" : "string"
        }
      },
      "required" : [ "Id" ]
    },
    "Range" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "EndTime" : {
          "type" : "string"
        },
        "StartTime" : {
          "type" : "string"
        }
      },
      "required" : [ "EndTime", "StartTime" ]
    },
    "SingleMetricAnomalyDetector" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MetricName" : {
          "type" : "string"
        },
        "Dimensions" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Dimension"
          }
        },
        "AccountId" : {
          "type" : "string"
        },
        "Stat" : {
          "type" : "string"
        },
        "Namespace" : {
          "type" : "string"
        }
      }
    }
  },
  "createOnlyProperties" : [ "/properties/Dimensions", "/properties/MetricCharacteristics", "/properties/MetricName", "/properties/Namespace", "/properties/SingleMetricAnomalyDetector", "/properties/MetricMathAnomalyDetector", "/properties/Stat" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}