SCHEMA = {
  "typeName" : "AWS::SageMaker::CodeRepository",
  "description" : "Resource Type definition for AWS::SageMaker::CodeRepository",
  "additionalProperties" : False,
  "properties" : {
    "GitConfig" : {
      "$ref" : "#/definitions/GitConfig"
    },
    "CodeRepositoryName" : {
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
    }
  },
  "definitions" : {
    "GitConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecretArn" : {
          "type" : "string"
        },
        "RepositoryUrl" : {
          "type" : "string"
        },
        "Branch" : {
          "type" : "string"
        }
      },
      "required" : [ "RepositoryUrl" ]
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
    }
  },
  "required" : [ "GitConfig" ],
  "createOnlyProperties" : [ "/properties/CodeRepositoryName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}