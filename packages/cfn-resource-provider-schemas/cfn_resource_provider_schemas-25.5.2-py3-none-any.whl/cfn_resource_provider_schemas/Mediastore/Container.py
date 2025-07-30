SCHEMA = {
  "typeName" : "AWS::MediaStore::Container",
  "description" : "Resource Type definition for AWS::MediaStore::Container",
  "additionalProperties" : False,
  "properties" : {
    "Policy" : {
      "type" : "string"
    },
    "MetricPolicy" : {
      "$ref" : "#/definitions/MetricPolicy"
    },
    "Endpoint" : {
      "type" : "string"
    },
    "ContainerName" : {
      "type" : "string"
    },
    "CorsPolicy" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/CorsRule"
      }
    },
    "LifecyclePolicy" : {
      "type" : "string"
    },
    "AccessLoggingEnabled" : {
      "type" : "boolean"
    },
    "Id" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Tag"
      }
    }
  },
  "definitions" : {
    "MetricPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ContainerLevelMetrics" : {
          "type" : "string"
        },
        "MetricPolicyRules" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/MetricPolicyRule"
          }
        }
      },
      "required" : [ "ContainerLevelMetrics" ]
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
    "MetricPolicyRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ObjectGroupName" : {
          "type" : "string"
        },
        "ObjectGroup" : {
          "type" : "string"
        }
      },
      "required" : [ "ObjectGroup", "ObjectGroupName" ]
    },
    "CorsRule" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AllowedMethods" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "AllowedOrigins" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "ExposeHeaders" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "MaxAgeSeconds" : {
          "type" : "integer"
        },
        "AllowedHeaders" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    }
  },
  "required" : [ "ContainerName" ],
  "createOnlyProperties" : [ "/properties/ContainerName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/Endpoint" ]
}