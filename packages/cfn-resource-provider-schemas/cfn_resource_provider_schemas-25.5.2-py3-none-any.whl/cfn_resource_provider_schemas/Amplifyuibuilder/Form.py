SCHEMA = {
  "typeName" : "AWS::AmplifyUIBuilder::Form",
  "description" : "Definition of AWS::AmplifyUIBuilder::Form Resource Type",
  "definitions" : {
    "FieldConfig" : {
      "type" : "object",
      "properties" : {
        "Label" : {
          "type" : "string"
        },
        "Position" : {
          "$ref" : "#/definitions/FieldPosition"
        },
        "Excluded" : {
          "type" : "boolean"
        },
        "InputType" : {
          "$ref" : "#/definitions/FieldInputConfig"
        },
        "Validations" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FieldValidationConfiguration"
          }
        }
      },
      "additionalProperties" : False
    },
    "FieldInputConfig" : {
      "type" : "object",
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "Required" : {
          "type" : "boolean"
        },
        "ReadOnly" : {
          "type" : "boolean"
        },
        "Placeholder" : {
          "type" : "string"
        },
        "DefaultValue" : {
          "type" : "string"
        },
        "DescriptiveText" : {
          "type" : "string"
        },
        "DefaultChecked" : {
          "type" : "boolean"
        },
        "DefaultCountryCode" : {
          "type" : "string"
        },
        "ValueMappings" : {
          "$ref" : "#/definitions/ValueMappings"
        },
        "Name" : {
          "type" : "string"
        },
        "MinValue" : {
          "type" : "number"
        },
        "MaxValue" : {
          "type" : "number"
        },
        "Step" : {
          "type" : "number"
        },
        "Value" : {
          "type" : "string"
        },
        "IsArray" : {
          "type" : "boolean"
        },
        "FileUploaderConfig" : {
          "$ref" : "#/definitions/FileUploaderFieldConfig"
        }
      },
      "required" : [ "Type" ],
      "additionalProperties" : False
    },
    "FieldPosition" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "Fixed",
        "properties" : {
          "Fixed" : {
            "$ref" : "#/definitions/FixedPosition"
          }
        },
        "required" : [ "Fixed" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "RightOf",
        "properties" : {
          "RightOf" : {
            "type" : "string"
          }
        },
        "required" : [ "RightOf" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Below",
        "properties" : {
          "Below" : {
            "type" : "string"
          }
        },
        "required" : [ "Below" ],
        "additionalProperties" : False
      } ]
    },
    "FieldValidationConfiguration" : {
      "type" : "object",
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "StrValues" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "NumValues" : {
          "type" : "array",
          "items" : {
            "type" : "number"
          }
        },
        "ValidationMessage" : {
          "type" : "string"
        }
      },
      "required" : [ "Type" ],
      "additionalProperties" : False
    },
    "FieldsMap" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "$ref" : "#/definitions/FieldConfig"
        }
      },
      "additionalProperties" : False
    },
    "FileUploaderFieldConfig" : {
      "type" : "object",
      "properties" : {
        "AccessLevel" : {
          "$ref" : "#/definitions/StorageAccessLevel"
        },
        "AcceptedFileTypes" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "ShowThumbnails" : {
          "type" : "boolean"
        },
        "IsResumable" : {
          "type" : "boolean"
        },
        "MaxFileCount" : {
          "type" : "number"
        },
        "MaxSize" : {
          "type" : "number"
        }
      },
      "required" : [ "AcceptedFileTypes", "AccessLevel" ],
      "additionalProperties" : False
    },
    "FixedPosition" : {
      "type" : "string",
      "enum" : [ "first" ]
    },
    "FormActionType" : {
      "type" : "string",
      "enum" : [ "create", "update" ]
    },
    "FormButton" : {
      "type" : "object",
      "properties" : {
        "Excluded" : {
          "type" : "boolean"
        },
        "Children" : {
          "type" : "string"
        },
        "Position" : {
          "$ref" : "#/definitions/FieldPosition"
        }
      },
      "additionalProperties" : False
    },
    "FormButtonsPosition" : {
      "type" : "string",
      "enum" : [ "top", "bottom", "top_and_bottom" ]
    },
    "FormCTA" : {
      "type" : "object",
      "properties" : {
        "Position" : {
          "$ref" : "#/definitions/FormButtonsPosition"
        },
        "Clear" : {
          "$ref" : "#/definitions/FormButton"
        },
        "Cancel" : {
          "$ref" : "#/definitions/FormButton"
        },
        "Submit" : {
          "$ref" : "#/definitions/FormButton"
        }
      },
      "additionalProperties" : False
    },
    "FormDataSourceType" : {
      "type" : "string",
      "enum" : [ "DataStore", "Custom" ]
    },
    "FormDataTypeConfig" : {
      "type" : "object",
      "properties" : {
        "DataSourceType" : {
          "$ref" : "#/definitions/FormDataSourceType"
        },
        "DataTypeName" : {
          "type" : "string"
        }
      },
      "required" : [ "DataSourceType", "DataTypeName" ],
      "additionalProperties" : False
    },
    "FormInputBindingProperties" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "$ref" : "#/definitions/FormInputBindingPropertiesValue"
        }
      },
      "additionalProperties" : False
    },
    "FormInputBindingPropertiesValue" : {
      "type" : "object",
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "BindingProperties" : {
          "$ref" : "#/definitions/FormInputBindingPropertiesValueProperties"
        }
      },
      "additionalProperties" : False
    },
    "FormInputBindingPropertiesValueProperties" : {
      "type" : "object",
      "properties" : {
        "Model" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "FormInputValueProperty" : {
      "type" : "object",
      "properties" : {
        "Value" : {
          "type" : "string"
        },
        "BindingProperties" : {
          "$ref" : "#/definitions/FormInputValuePropertyBindingProperties"
        },
        "Concat" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/FormInputValueProperty"
          }
        }
      },
      "additionalProperties" : False
    },
    "FormInputValuePropertyBindingProperties" : {
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
    "FormStyle" : {
      "type" : "object",
      "properties" : {
        "HorizontalGap" : {
          "$ref" : "#/definitions/FormStyleConfig"
        },
        "VerticalGap" : {
          "$ref" : "#/definitions/FormStyleConfig"
        },
        "OuterPadding" : {
          "$ref" : "#/definitions/FormStyleConfig"
        }
      },
      "additionalProperties" : False
    },
    "FormStyleConfig" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "TokenReference",
        "properties" : {
          "TokenReference" : {
            "type" : "string"
          }
        },
        "required" : [ "TokenReference" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Value",
        "properties" : {
          "Value" : {
            "type" : "string"
          }
        },
        "required" : [ "Value" ],
        "additionalProperties" : False
      } ]
    },
    "LabelDecorator" : {
      "type" : "string",
      "enum" : [ "required", "optional", "none" ]
    },
    "SectionalElement" : {
      "type" : "object",
      "properties" : {
        "Type" : {
          "type" : "string"
        },
        "Position" : {
          "$ref" : "#/definitions/FieldPosition"
        },
        "Text" : {
          "type" : "string"
        },
        "Level" : {
          "type" : "number"
        },
        "Orientation" : {
          "type" : "string"
        },
        "Excluded" : {
          "type" : "boolean"
        }
      },
      "required" : [ "Type" ],
      "additionalProperties" : False
    },
    "SectionalElementMap" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "$ref" : "#/definitions/SectionalElement"
        }
      },
      "additionalProperties" : False
    },
    "StorageAccessLevel" : {
      "type" : "string",
      "enum" : [ "public", "protected", "private" ]
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
    },
    "ValueMapping" : {
      "type" : "object",
      "properties" : {
        "DisplayValue" : {
          "$ref" : "#/definitions/FormInputValueProperty"
        },
        "Value" : {
          "$ref" : "#/definitions/FormInputValueProperty"
        }
      },
      "required" : [ "Value" ],
      "additionalProperties" : False
    },
    "ValueMappings" : {
      "type" : "object",
      "properties" : {
        "Values" : {
          "type" : "array",
          "items" : {
            "$ref" : "#/definitions/ValueMapping"
          }
        },
        "BindingProperties" : {
          "$ref" : "#/definitions/FormInputBindingProperties"
        }
      },
      "required" : [ "Values" ],
      "additionalProperties" : False
    }
  },
  "properties" : {
    "AppId" : {
      "type" : "string"
    },
    "Cta" : {
      "$ref" : "#/definitions/FormCTA"
    },
    "DataType" : {
      "$ref" : "#/definitions/FormDataTypeConfig"
    },
    "EnvironmentName" : {
      "type" : "string"
    },
    "Fields" : {
      "$ref" : "#/definitions/FieldsMap"
    },
    "FormActionType" : {
      "$ref" : "#/definitions/FormActionType"
    },
    "Id" : {
      "type" : "string"
    },
    "LabelDecorator" : {
      "$ref" : "#/definitions/LabelDecorator"
    },
    "Name" : {
      "type" : "string",
      "maxLength" : 255,
      "minLength" : 1
    },
    "SchemaVersion" : {
      "type" : "string"
    },
    "SectionalElements" : {
      "$ref" : "#/definitions/SectionalElementMap"
    },
    "Style" : {
      "$ref" : "#/definitions/FormStyle"
    },
    "Tags" : {
      "$ref" : "#/definitions/Tags"
    }
  },
  "createOnlyProperties" : [ "/properties/AppId", "/properties/EnvironmentName" ],
  "readOnlyProperties" : [ "/properties/Id" ],
  "primaryIdentifier" : [ "/properties/AppId", "/properties/EnvironmentName", "/properties/Id" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "amplify:GetApp", "amplifyuibuilder:CreateForm", "amplifyuibuilder:GetForm", "amplifyuibuilder:TagResource" ]
    },
    "read" : {
      "permissions" : [ "amplify:GetApp", "amplifyuibuilder:GetForm" ]
    },
    "update" : {
      "permissions" : [ "amplify:GetApp", "amplifyuibuilder:GetForm", "amplifyuibuilder:TagResource", "amplifyuibuilder:UntagResource", "amplifyuibuilder:UpdateForm" ]
    },
    "delete" : {
      "permissions" : [ "amplify:GetApp", "amplifyuibuilder:DeleteForm", "amplifyuibuilder:UntagResource" ]
    },
    "list" : {
      "permissions" : [ "amplify:GetApp", "amplifyuibuilder:ListForms" ],
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