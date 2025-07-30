SCHEMA = {
  "typeName" : "AWS::AppStream::Stack",
  "description" : "Resource Type definition for AWS::AppStream::Stack",
  "additionalProperties" : False,
  "properties" : {
    "Description" : {
      "type" : "string"
    },
    "StorageConnectors" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/StorageConnector"
      }
    },
    "DeleteStorageConnectors" : {
      "type" : "boolean"
    },
    "EmbedHostDomains" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "UserSettings" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/UserSetting"
      }
    },
    "AttributesToDelete" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "RedirectURL" : {
      "type" : "string"
    },
    "StreamingExperienceSettings" : {
      "$ref" : "#/definitions/StreamingExperienceSettings"
    },
    "Name" : {
      "type" : "string"
    },
    "FeedbackURL" : {
      "type" : "string"
    },
    "ApplicationSettings" : {
      "$ref" : "#/definitions/ApplicationSettings"
    },
    "DisplayName" : {
      "type" : "string"
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
    },
    "AccessEndpoints" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/AccessEndpoint"
      }
    }
  },
  "definitions" : {
    "StorageConnector" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Domains" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        },
        "ResourceIdentifier" : {
          "type" : "string"
        },
        "ConnectorType" : {
          "type" : "string"
        }
      },
      "required" : [ "ConnectorType" ]
    },
    "ApplicationSettings" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SettingsGroup" : {
          "type" : "string"
        },
        "Enabled" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Enabled" ]
    },
    "StreamingExperienceSettings" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PreferredProtocol" : {
          "type" : "string"
        }
      }
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
    "AccessEndpoint" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "EndpointType" : {
          "type" : "string"
        },
        "VpceId" : {
          "type" : "string"
        }
      },
      "required" : [ "EndpointType", "VpceId" ]
    },
    "UserSetting" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Permission" : {
          "type" : "string"
        },
        "Action" : {
          "type" : "string"
        },
        "MaximumLength" : {
          "type" : "integer"
        }
      },
      "required" : [ "Action", "Permission" ]
    }
  },
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}