SCHEMA = {
  "typeName" : "AWS::SageMaker::NotebookInstanceLifecycleConfig",
  "description" : "Resource Type definition for AWS::SageMaker::NotebookInstanceLifecycleConfig",
  "additionalProperties" : False,
  "properties" : {
    "OnStart" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/NotebookInstanceLifecycleHook"
      }
    },
    "Id" : {
      "type" : "string"
    },
    "NotebookInstanceLifecycleConfigName" : {
      "type" : "string"
    },
    "OnCreate" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/NotebookInstanceLifecycleHook"
      }
    }
  },
  "definitions" : {
    "NotebookInstanceLifecycleHook" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Content" : {
          "type" : "string"
        }
      }
    }
  },
  "createOnlyProperties" : [ "/properties/NotebookInstanceLifecycleConfigName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}