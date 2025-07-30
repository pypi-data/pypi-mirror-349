SCHEMA = {
  "typeName" : "AWS::AmplifyUIBuilder::Component",
  "description" : "Definition of AWS::AmplifyUIBuilder::Component Resource Type",
  "definitions" : {
    "ActionParameters" : {
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/ComponentProperty"
        },
        "Url" : {
          "$ref" : "#/definitions/ComponentProperty"
        },
        "Anchor" : {
          "$ref" : "#/definitions/ComponentProperty"
        },
        "Target" : {
          "$ref" : "#/definitions/ComponentProperty"
        },
        "Global" : {
          "$ref" : "#/definitions/ComponentProperty"
        },
        "Model" : {
          "type" : "string"
        },
        "Id" : {
          "$ref" : "#/definitions/ComponentProperty"
        },
        "Fields" : {
          "$ref" : "#/definitions/ComponentProperties"
        },
        "State" : {
          "$ref" : "#/definitions/MutationActionSetStateParameter"
        }
      },
      "additionalProperties" : False
    },
    "ComponentBindingProperties" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "$ref" : "#/definitions/ComponentBindingPropertiesValue"
        }
      },
      "additionalProperties" : False
    },
    "ComponentBindingPropertiesValue" : {
      "type" : "object",
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "BindingProperties" : {
          "$ref" : "#/definitions/ComponentBindingPropertiesValueProperties"
        },
        "DefaultValue" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "ComponentBindingPropertiesValueProperties" : {
      "type" : "object",
      "properties" : {
        "Model" : {
          "type" : "string"
        },
        "Field" : {
          "type" : "string"
        },
        "Predicates" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Predicate"
          }
        },
        "UserAttribute" : {
          "type" : "string"
        },
        "Bucket" : {
          "type" : "string"
        },
        "Key" : {
          "type" : "string"
        },
        "DefaultValue" : {
          "type" : "string"
        },
        "SlotName" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "ComponentChild" : {
      "type" : "object",
      "properties" : {
        "ComponentType" : {
          "type" : "string"
        },
        "Name" : {
          "type" : "string"
        },
        "Properties" : {
          "$ref" : "#/definitions/ComponentProperties"
        },
        "Children" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ComponentChild"
          }
        },
        "Events" : {
          "$ref" : "#/definitions/ComponentEvents"
        },
        "SourceId" : {
          "type" : "string"
        }
      },
      "required" : [ "ComponentType", "Name", "Properties" ],
      "additionalProperties" : False
    },
    "ComponentCollectionProperties" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "$ref" : "#/definitions/ComponentDataConfiguration"
        }
      },
      "additionalProperties" : False
    },
    "ComponentConditionProperty" : {
      "type" : "object",
      "properties" : {
        "Property" : {
          "type" : "string"
        },
        "Field" : {
          "type" : "string"
        },
        "Operator" : {
          "type" : "string"
        },
        "Operand" : {
          "type" : "string"
        },
        "Then" : {
          "$ref" : "#/definitions/ComponentProperty"
        },
        "Else" : {
          "$ref" : "#/definitions/ComponentProperty"
        },
        "OperandType" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "ComponentDataConfiguration" : {
      "type" : "object",
      "properties" : {
        "Model" : {
          "type" : "string"
        },
        "Sort" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/SortProperty"
          }
        },
        "Predicate" : {
          "$ref" : "#/definitions/Predicate"
        },
        "Identifiers" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "Model" ],
      "additionalProperties" : False
    },
    "ComponentEvent" : {
      "type" : "object",
      "properties" : {
        "Action" : {
          "type" : "string"
        },
        "Parameters" : {
          "$ref" : "#/definitions/ActionParameters"
        },
        "BindingEvent" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "ComponentEvents" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "$ref" : "#/definitions/ComponentEvent"
        }
      },
      "additionalProperties" : False
    },
    "ComponentOverrides" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "$ref" : "#/definitions/ComponentOverridesValue"
        }
      },
      "additionalProperties" : False
    },
    "ComponentOverridesValue" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "ComponentProperties" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "$ref" : "#/definitions/ComponentProperty"
        }
      },
      "additionalProperties" : False
    },
    "ComponentProperty" : {
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "BindingProperties" : {
          "$ref" : "#/definitions/ComponentPropertyBindingProperties"
        },
        "CollectionBindingProperties" : {
          "$ref" : "#/definitions/ComponentPropertyBindingProperties"
        },
        "DefaultValue" : {
          "type" : "string"
        },
        "Model" : {
          "type" : "string"
        },
        "Bindings" : {
          "$ref" : "#/definitions/FormBindings"
        },
        "Event" : {
          "type" : "string"
        },
        "UserAttribute" : {
          "type" : "string"
        },
        "Concat" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ComponentProperty"
          }
        },
        "Condition" : {
          "$ref" : "#/definitions/ComponentConditionProperty"
        },
        "Configured" : {
          "type" : "boolean"
        },
        "Type" : {
          "type" : "string"
        },
        "ImportedValue" : {
          "type" : "string"
        },
        "ComponentName" : {
          "type" : "string"
        },
        "Property" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "ComponentPropertyBindingProperties" : {
      "type" : "object",
      "properties" : {
        "Property" : {
          "type" : "string"
        },
        "Field" : {
          "type" : "string"
        }
      },
      "required" : [ "Property" ],
      "additionalProperties" : False
    },
    "ComponentVariant" : {
      "type" : "object",
      "properties" : {
        "VariantValues" : {
          "$ref" : "#/definitions/ComponentVariantValues"
        },
        "Overrides" : {
          "$ref" : "#/definitions/ComponentOverrides"
        }
      },
      "additionalProperties" : False
    },
    "ComponentVariantValues" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "FormBindingElement" : {
      "type" : "object",
      "properties" : {
        "Element" : {
          "type" : "string"
        },
        "Property" : {
          "type" : "string"
        }
      },
      "required" : [ "Element", "Property" ],
      "additionalProperties" : False
    },
    "FormBindings" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "$ref" : "#/definitions/FormBindingElement"
        }
      },
      "additionalProperties" : False
    },
    "MutationActionSetStateParameter" : {
      "type" : "object",
      "properties" : {
        "ComponentName" : {
          "type" : "string"
        },
        "Property" : {
          "type" : "string"
        },
        "Set" : {
          "$ref" : "#/definitions/ComponentProperty"
        }
      },
      "required" : [ "ComponentName", "Property", "Set" ],
      "additionalProperties" : False
    },
    "Predicate" : {
      "type" : "object",
      "properties" : {
        "Or" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Predicate"
          }
        },
        "And" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/Predicate"
          }
        },
        "Field" : {
          "type" : "string"
        },
        "Operator" : {
          "type" : "string"
        },
        "Operand" : {
          "type" : "string"
        },
        "OperandType" : {
          "type" : "string",
          "pattern" : "^boolean|string|number$"
        }
      },
      "additionalProperties" : False
    },
    "SortDirection" : {
      "type" : "string",
      "enum" : [ "ASC", "DESC" ]
    },
    "SortProperty" : {
      "type" : "object",
      "properties" : {
        "Field" : {
          "type" : "string"
        },
        "Direction" : {
          "$ref" : "#/definitions/SortDirection"
        }
      },
      "required" : [ "Direction", "Field" ],
      "additionalProperties" : False
    },
    "Tags" : {
      "type" : "object",
      "patternProperties" : {
        "^(?!aws:)[a-zA-Z+-=._:/]+$" : {
          "type" : "string",
          "maxLength" : 256,
          "minLength" : 1
        }
      },
      "additionalProperties" : False
    }
  },
  "properties" : {
    "AppId" : {
      "type" : "string"
    },
    "BindingProperties" : {
      "$ref" : "#/definitions/ComponentBindingProperties"
    },
    "Children" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/ComponentChild"
      }
    },
    "CollectionProperties" : {
      "$ref" : "#/definitions/ComponentCollectionProperties"
    },
    "ComponentType" : {
      "type" : "string",
      "maxLength" : 255,
      "minLength" : 1
    },
    "CreatedAt" : {
      "type" : "string",
      "format" : "date-time"
    },
    "EnvironmentName" : {
      "type" : "string"
    },
    "Events" : {
      "$ref" : "#/definitions/ComponentEvents"
    },
    "Id" : {
      "type" : "string"
    },
    "ModifiedAt" : {
      "type" : "string",
      "format" : "date-time"
    },
    "Name" : {
      "type" : "string",
      "maxLength" : 255,
      "minLength" : 1
    },
    "Overrides" : {
      "$ref" : "#/definitions/ComponentOverrides"
    },
    "Properties" : {
      "$ref" : "#/definitions/ComponentProperties"
    },
    "SchemaVersion" : {
      "type" : "string"
    },
    "SourceId" : {
      "type" : "string"
    },
    "Tags" : {
      "$ref" : "#/definitions/Tags"
    },
    "Variants" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/ComponentVariant"
      }
    }
  },
  "createOnlyProperties" : [ "/properties/AppId", "/properties/EnvironmentName" ],
  "readOnlyProperties" : [ "/properties/CreatedAt", "/properties/Id", "/properties/ModifiedAt" ],
  "primaryIdentifier" : [ "/properties/AppId", "/properties/EnvironmentName", "/properties/Id" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "amplify:GetApp", "amplifyuibuilder:CreateComponent", "amplifyuibuilder:GetComponent", "amplifyuibuilder:TagResource" ]
    },
    "read" : {
      "permissions" : [ "amplify:GetApp", "amplifyuibuilder:GetComponent" ]
    },
    "update" : {
      "permissions" : [ "amplify:GetApp", "amplifyuibuilder:GetComponent", "amplifyuibuilder:TagResource", "amplifyuibuilder:UntagResource", "amplifyuibuilder:UpdateComponent" ]
    },
    "delete" : {
      "permissions" : [ "amplify:GetApp", "amplifyuibuilder:DeleteComponent", "amplifyuibuilder:GetComponent", "amplifyuibuilder:UntagResource" ]
    },
    "list" : {
      "permissions" : [ "amplify:GetApp", "amplifyuibuilder:ListComponents" ],
      "handlerSchema" : {
        "properties" : {
          "AppId" : {
            "$ref" : "resource-schema.json#/properties/AppId"
          },
          "EnvironmentName" : {
            "$ref" : "resource-schema.json#/properties/EnvironmentName"
          }
        },
        "required" : [ "AppId", "EnvironmentName" ]
      }
    }
  },
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : True,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "amplifyuibuilder:TagResource", "amplifyuibuilder:UntagResource" ]
  },
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-amplifyuibuilder",
  "additionalProperties" : False
}