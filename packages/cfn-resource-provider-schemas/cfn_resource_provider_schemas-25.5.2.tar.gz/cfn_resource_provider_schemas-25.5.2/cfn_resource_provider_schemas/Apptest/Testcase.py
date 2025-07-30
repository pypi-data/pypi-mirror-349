SCHEMA = {
  "typeName" : "AWS::AppTest::TestCase",
  "description" : "Represents a Test Case that can be captured and executed",
  "definitions" : {
    "Batch" : {
      "type" : "object",
      "properties" : {
        "BatchJobName" : {
          "type" : "string",
          "pattern" : "^\\S{1,1000}$"
        },
        "BatchJobParameters" : {
          "$ref" : "#/definitions/BatchJobParameters"
        },
        "ExportDataSetNames" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "pattern" : "^\\S{1,100}$"
          }
        }
      },
      "required" : [ "BatchJobName" ],
      "additionalProperties" : False
    },
    "BatchJobParameters" : {
      "type" : "object",
      "patternProperties" : {
        ".+" : {
          "type" : "string"
        }
      },
      "additionalProperties" : False
    },
    "CaptureTool" : {
      "type" : "string",
      "enum" : [ "Precisely", "AWS DMS" ]
    },
    "CloudFormationAction" : {
      "type" : "object",
      "properties" : {
        "Resource" : {
          "type" : "string",
          "pattern" : "^\\S{1,1000}$"
        },
        "ActionType" : {
          "$ref" : "#/definitions/CloudFormationActionType"
        }
      },
      "required" : [ "Resource" ],
      "additionalProperties" : False
    },
    "CloudFormationActionType" : {
      "type" : "string",
      "enum" : [ "Create", "Delete" ]
    },
    "CompareAction" : {
      "type" : "object",
      "properties" : {
        "Input" : {
          "$ref" : "#/definitions/Input"
        },
        "Output" : {
          "$ref" : "#/definitions/Output"
        }
      },
      "required" : [ "Input" ],
      "additionalProperties" : False
    },
    "DataSet" : {
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/DataSetType"
        },
        "Name" : {
          "type" : "string",
          "pattern" : "^\\S{1,100}$"
        },
        "Ccsid" : {
          "type" : "string",
          "pattern" : "^\\S{1,50}$"
        },
        "Format" : {
          "$ref" : "#/definitions/Format"
        },
        "Length" : {
          "type" : "number"
        }
      },
      "required" : [ "Ccsid", "Format", "Length", "Name", "Type" ],
      "additionalProperties" : False
    },
    "DataSetType" : {
      "type" : "string",
      "enum" : [ "PS" ]
    },
    "DatabaseCDC" : {
      "type" : "object",
      "properties" : {
        "SourceMetadata" : {
          "$ref" : "#/definitions/SourceDatabaseMetadata"
        },
        "TargetMetadata" : {
          "$ref" : "#/definitions/TargetDatabaseMetadata"
        }
      },
      "required" : [ "SourceMetadata", "TargetMetadata" ],
      "additionalProperties" : False
    },
    "FileMetadata" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "DataSets",
        "properties" : {
          "DataSets" : {
            "type" : "array",
            "items" : {
              "$ref" : "#/definitions/DataSet"
            }
          }
        },
        "required" : [ "DataSets" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "DatabaseCDC",
        "properties" : {
          "DatabaseCDC" : {
            "$ref" : "#/definitions/DatabaseCDC"
          }
        },
        "required" : [ "DatabaseCDC" ],
        "additionalProperties" : False
      } ]
    },
    "Format" : {
      "type" : "string",
      "enum" : [ "FIXED", "VARIABLE", "LINE_SEQUENTIAL" ]
    },
    "Input" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "File",
        "properties" : {
          "File" : {
            "$ref" : "#/definitions/InputFile"
          }
        },
        "required" : [ "File" ],
        "additionalProperties" : False
      } ]
    },
    "InputFile" : {
      "type" : "object",
      "properties" : {
        "SourceLocation" : {
          "type" : "string",
          "pattern" : "^\\S{1,1000}$"
        },
        "TargetLocation" : {
          "type" : "string",
          "pattern" : "^\\S{1,1000}$"
        },
        "FileMetadata" : {
          "$ref" : "#/definitions/FileMetadata"
        }
      },
      "required" : [ "FileMetadata", "SourceLocation", "TargetLocation" ],
      "additionalProperties" : False
    },
    "M2ManagedActionProperties" : {
      "type" : "object",
      "properties" : {
        "ForceStop" : {
          "type" : "boolean"
        },
        "ImportDataSetLocation" : {
          "type" : "string",
          "pattern" : "^\\S{1,1000}$"
        }
      },
      "additionalProperties" : False
    },
    "M2ManagedActionType" : {
      "type" : "string",
      "enum" : [ "Configure", "Deconfigure" ]
    },
    "M2ManagedApplicationAction" : {
      "type" : "object",
      "properties" : {
        "Resource" : {
          "type" : "string",
          "pattern" : "^\\S{1,1000}$"
        },
        "ActionType" : {
          "$ref" : "#/definitions/M2ManagedActionType"
        },
        "Properties" : {
          "$ref" : "#/definitions/M2ManagedActionProperties"
        }
      },
      "required" : [ "ActionType", "Resource" ],
      "additionalProperties" : False
    },
    "M2NonManagedActionType" : {
      "type" : "string",
      "enum" : [ "Configure", "Deconfigure" ]
    },
    "M2NonManagedApplicationAction" : {
      "type" : "object",
      "properties" : {
        "Resource" : {
          "type" : "string",
          "pattern" : "^\\S{1,1000}$"
        },
        "ActionType" : {
          "$ref" : "#/definitions/M2NonManagedActionType"
        }
      },
      "required" : [ "ActionType", "Resource" ],
      "additionalProperties" : False
    },
    "MainframeAction" : {
      "type" : "object",
      "properties" : {
        "Resource" : {
          "type" : "string",
          "pattern" : "^\\S{1,1000}$"
        },
        "ActionType" : {
          "$ref" : "#/definitions/MainframeActionType"
        },
        "Properties" : {
          "$ref" : "#/definitions/MainframeActionProperties"
        }
      },
      "required" : [ "ActionType", "Resource" ],
      "additionalProperties" : False
    },
    "MainframeActionProperties" : {
      "type" : "object",
      "properties" : {
        "DmsTaskArn" : {
          "type" : "string",
          "pattern" : "^\\S{1,1000}$"
        }
      },
      "additionalProperties" : False
    },
    "MainframeActionType" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "Batch",
        "properties" : {
          "Batch" : {
            "$ref" : "#/definitions/Batch"
          }
        },
        "required" : [ "Batch" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "Tn3270",
        "properties" : {
          "Tn3270" : {
            "$ref" : "#/definitions/TN3270"
          }
        },
        "required" : [ "Tn3270" ],
        "additionalProperties" : False
      } ]
    },
    "Output" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "File",
        "properties" : {
          "File" : {
            "$ref" : "#/definitions/OutputFile"
          }
        },
        "required" : [ "File" ],
        "additionalProperties" : False
      } ]
    },
    "OutputFile" : {
      "type" : "object",
      "properties" : {
        "FileLocation" : {
          "type" : "string",
          "maxLength" : 1024,
          "minLength" : 0
        }
      },
      "additionalProperties" : False
    },
    "ResourceAction" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "M2ManagedApplicationAction",
        "properties" : {
          "M2ManagedApplicationAction" : {
            "$ref" : "#/definitions/M2ManagedApplicationAction"
          }
        },
        "required" : [ "M2ManagedApplicationAction" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "M2NonManagedApplicationAction",
        "properties" : {
          "M2NonManagedApplicationAction" : {
            "$ref" : "#/definitions/M2NonManagedApplicationAction"
          }
        },
        "required" : [ "M2NonManagedApplicationAction" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "CloudFormationAction",
        "properties" : {
          "CloudFormationAction" : {
            "$ref" : "#/definitions/CloudFormationAction"
          }
        },
        "required" : [ "CloudFormationAction" ],
        "additionalProperties" : False
      } ]
    },
    "Script" : {
      "type" : "object",
      "properties" : {
        "ScriptLocation" : {
          "type" : "string",
          "maxLength" : 1024,
          "minLength" : 0
        },
        "Type" : {
          "$ref" : "#/definitions/ScriptType"
        }
      },
      "required" : [ "ScriptLocation", "Type" ],
      "additionalProperties" : False
    },
    "ScriptType" : {
      "type" : "string",
      "enum" : [ "Selenium" ]
    },
    "SourceDatabase" : {
      "type" : "string",
      "enum" : [ "z/OS-DB2" ]
    },
    "SourceDatabaseMetadata" : {
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/SourceDatabase"
        },
        "CaptureTool" : {
          "$ref" : "#/definitions/CaptureTool"
        }
      },
      "required" : [ "CaptureTool", "Type" ],
      "additionalProperties" : False
    },
    "Step" : {
      "type" : "object",
      "properties" : {
        "Name" : {
          "type" : "string",
          "pattern" : "^[A-Za-z][A-Za-z0-9_\\-]{1,59}$"
        },
        "Description" : {
          "type" : "string",
          "maxLength" : 1000,
          "minLength" : 0
        },
        "Action" : {
          "$ref" : "#/definitions/StepAction"
        }
      },
      "required" : [ "Action", "Name" ],
      "additionalProperties" : False
    },
    "StepAction" : {
      "oneOf" : [ {
        "type" : "object",
        "title" : "ResourceAction",
        "properties" : {
          "ResourceAction" : {
            "$ref" : "#/definitions/ResourceAction"
          }
        },
        "required" : [ "ResourceAction" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "MainframeAction",
        "properties" : {
          "MainframeAction" : {
            "$ref" : "#/definitions/MainframeAction"
          }
        },
        "required" : [ "MainframeAction" ],
        "additionalProperties" : False
      }, {
        "type" : "object",
        "title" : "CompareAction",
        "properties" : {
          "CompareAction" : {
            "$ref" : "#/definitions/CompareAction"
          }
        },
        "required" : [ "CompareAction" ],
        "additionalProperties" : False
      } ]
    },
    "TN3270" : {
      "type" : "object",
      "properties" : {
        "Script" : {
          "$ref" : "#/definitions/Script"
        },
        "ExportDataSetNames" : {
          "type" : "array",
          "items" : {
            "type" : "string",
            "pattern" : "^\\S{1,100}$"
          }
        }
      },
      "required" : [ "Script" ],
      "additionalProperties" : False
    },
    "TagMap" : {
      "type" : "object",
      "maxProperties" : 200,
      "minProperties" : 0,
      "patternProperties" : {
        "^(?!aws:).+$" : {
          "type" : "string",
          "maxLength" : 256,
          "minLength" : 0
        }
      },
      "additionalProperties" : False
    },
    "TargetDatabase" : {
      "type" : "string",
      "enum" : [ "PostgreSQL" ]
    },
    "TargetDatabaseMetadata" : {
      "type" : "object",
      "properties" : {
        "Type" : {
          "$ref" : "#/definitions/TargetDatabase"
        },
        "CaptureTool" : {
          "$ref" : "#/definitions/CaptureTool"
        }
      },
      "required" : [ "CaptureTool", "Type" ],
      "additionalProperties" : False
    },
    "TestCaseLatestVersion" : {
      "type" : "object",
      "properties" : {
        "Version" : {
          "type" : "number"
        },
        "Status" : {
          "$ref" : "#/definitions/TestCaseLifecycle"
        }
      },
      "required" : [ "Status", "Version" ],
      "additionalProperties" : False
    },
    "TestCaseLifecycle" : {
      "type" : "string",
      "enum" : [ "Active", "Deleting" ]
    }
  },
  "properties" : {
    "CreationTime" : {
      "type" : "string",
      "format" : "date-time"
    },
    "Description" : {
      "type" : "string",
      "maxLength" : 1000,
      "minLength" : 0
    },
    "LastUpdateTime" : {
      "type" : "string",
      "format" : "date-time"
    },
    "LatestVersion" : {
      "$ref" : "#/definitions/TestCaseLatestVersion"
    },
    "Name" : {
      "type" : "string",
      "pattern" : "^[A-Za-z][A-Za-z0-9_\\-]{1,59}$"
    },
    "Status" : {
      "$ref" : "#/definitions/TestCaseLifecycle"
    },
    "Steps" : {
      "type" : "array",
      "items" : {
        "$ref" : "#/definitions/Step"
      },
      "maxItems" : 20,
      "minItems" : 1
    },
    "Tags" : {
      "$ref" : "#/definitions/TagMap"
    },
    "TestCaseArn" : {
      "type" : "string",
      "pattern" : "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]{1}|aws-us-gov):[A-Za-z0-9][A-Za-z0-9_/.-]{0,62}:([a-z]{2}-((iso[a-z]{0,1}-)|(gov-)){0,1}[a-z]+-[0-9]):[0-9]{12}:[A-Za-z0-9/][A-Za-z0-9:_/+=,@.-]{0,1023}$"
    },
    "TestCaseId" : {
      "type" : "string",
      "pattern" : "^[A-Za-z0-9:/\\-]{1,100}$"
    },
    "TestCaseVersion" : {
      "type" : "number"
    }
  },
  "required" : [ "Name", "Steps" ],
  "readOnlyProperties" : [ "/properties/CreationTime", "/properties/LastUpdateTime", "/properties/LatestVersion", "/properties/Status", "/properties/TestCaseArn", "/properties/TestCaseId", "/properties/TestCaseVersion" ],
  "createOnlyProperties" : [ "/properties/Name" ],
  "primaryIdentifier" : [ "/properties/TestCaseId" ],
  "tagging" : {
    "taggable" : True,
    "tagOnCreate" : True,
    "tagUpdatable" : True,
    "cloudFormationSystemTags" : False,
    "tagProperty" : "/properties/Tags",
    "permissions" : [ "apptest:TagResource", "apptest:UntagResource", "apptest:ListTagsForResource" ]
  },
  "handlers" : {
    "create" : {
      "permissions" : [ "apptest:CreateTestCase", "apptest:GetTestCase", "apptest:ListTagsForResource" ]
    },
    "read" : {
      "permissions" : [ "apptest:GetTestCase", "apptest:ListTagsForResource" ]
    },
    "update" : {
      "permissions" : [ "apptest:UpdateTestCase", "apptest:GetTestCase", "apptest:TagResource", "apptest:UnTagResource", "apptest:ListTagsForResource" ]
    },
    "delete" : {
      "permissions" : [ "apptest:GetTestCase", "apptest:ListTagsForResource", "apptest:DeleteTestCase" ]
    },
    "list" : {
      "permissions" : [ "apptest:ListTestCases" ]
    }
  },
  "additionalProperties" : False
}