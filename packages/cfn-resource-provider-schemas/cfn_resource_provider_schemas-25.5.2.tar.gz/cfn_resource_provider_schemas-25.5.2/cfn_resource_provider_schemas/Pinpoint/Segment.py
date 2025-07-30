SCHEMA = {
  "typeName" : "AWS::Pinpoint::Segment",
  "description" : "Resource Type definition for AWS::Pinpoint::Segment",
  "additionalProperties" : False,
  "properties" : {
    "SegmentId" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "SegmentGroups" : {
      "$ref" : "#/definitions/SegmentGroups"
    },
    "Dimensions" : {
      "$ref" : "#/definitions/SegmentDimensions"
    },
    "ApplicationId" : {
      "type" : "string"
    },
    "Tags" : {
      "type" : "object"
    },
    "Name" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "SegmentDimensions" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Demographic" : {
          "$ref" : "#/definitions/Demographic"
        },
        "Metrics" : {
          "type" : "object"
        },
        "Attributes" : {
          "type" : "object"
        },
        "Behavior" : {
          "$ref" : "#/definitions/Behavior"
        },
        "UserAttributes" : {
          "type" : "object"
        },
        "Location" : {
          "$ref" : "#/definitions/Location"
        }
      }
    },
    "SegmentGroups" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Groups" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Groups"
          }
        },
        "Include" : {
          "type" : "string"
        }
      }
    },
    "Demographic" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AppVersion" : {
          "$ref" : "#/definitions/SetDimension"
        },
        "DeviceType" : {
          "$ref" : "#/definitions/SetDimension"
        },
        "Platform" : {
          "$ref" : "#/definitions/SetDimension"
        },
        "Channel" : {
          "$ref" : "#/definitions/SetDimension"
        },
        "Model" : {
          "$ref" : "#/definitions/SetDimension"
        },
        "Make" : {
          "$ref" : "#/definitions/SetDimension"
        }
      }
    },
    "Groups" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "SourceType" : {
          "type" : "string"
        },
        "Dimensions" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/SegmentDimensions"
          }
        },
        "SourceSegments" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/SourceSegments"
          }
        }
      }
    },
    "Location" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "GPSPoint" : {
          "$ref" : "#/definitions/GPSPoint"
        },
        "Country" : {
          "$ref" : "#/definitions/SetDimension"
        }
      }
    },
    "Behavior" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Recency" : {
          "$ref" : "#/definitions/Recency"
        }
      }
    },
    "SetDimension" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DimensionType" : {
          "type" : "string"
        },
        "Values" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "SourceSegments" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Version" : {
          "type" : "integer"
        },
        "Id" : {
          "type" : "string"
        }
      },
      "required" : [ "Id" ]
    },
    "GPSPoint" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "RangeInKilometers" : {
          "type" : "number"
        },
        "Coordinates" : {
          "$ref" : "#/definitions/Coordinates"
        }
      },
      "required" : [ "RangeInKilometers", "Coordinates" ]
    },
    "Recency" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Duration" : {
          "type" : "string"
        },
        "RecencyType" : {
          "type" : "string"
        }
      },
      "required" : [ "Duration", "RecencyType" ]
    },
    "Coordinates" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Latitude" : {
          "type" : "number"
        },
        "Longitude" : {
          "type" : "number"
        }
      },
      "required" : [ "Longitude", "Latitude" ]
    }
  },
  "required" : [ "ApplicationId", "Name" ],
  "readOnlyProperties" : [ "/properties/SegmentId", "/properties/Arn" ],
  "createOnlyProperties" : [ "/properties/ApplicationId" ],
  "primaryIdentifier" : [ "/properties/SegmentId" ]
}