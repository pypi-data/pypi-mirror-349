SCHEMA = {
  "typeName" : "AWS::Greengrass::FunctionDefinitionVersion",
  "description" : "Resource Type definition for AWS::Greengrass::FunctionDefinitionVersion",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "DefaultConfig" : {
      "$ref" : "#/definitions/DefaultConfig"
    },
    "Functions" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "$ref" : "#/definitions/Function"
      }
    },
    "FunctionDefinitionId" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "DefaultConfig" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Execution" : {
          "$ref" : "#/definitions/Execution"
        }
      },
      "required" : [ "Execution" ]
    },
    "Function" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "FunctionArn" : {
          "type" : "string"
        },
        "FunctionConfiguration" : {
          "$ref" : "#/definitions/FunctionConfiguration"
        },
        "Id" : {
          "type" : "string"
        }
      },
      "required" : [ "FunctionArn", "FunctionConfiguration", "Id" ]
    },
    "Execution" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "IsolationMode" : {
          "type" : "string"
        },
        "RunAs" : {
          "$ref" : "#/definitions/RunAs"
        }
      }
    },
    "FunctionConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MemorySize" : {
          "type" : "integer"
        },
        "Pinned" : {
          "type" : "boolean"
        },
        "ExecArgs" : {
          "type" : "string"
        },
        "Timeout" : {
          "type" : "integer"
        },
        "EncodingType" : {
          "type" : "string"
        },
        "Environment" : {
          "$ref" : "#/definitions/Environment"
        },
        "Executable" : {
          "type" : "string"
        }
      }
    },
    "RunAs" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Uid" : {
          "type" : "integer"
        },
        "Gid" : {
          "type" : "integer"
        }
      }
    },
    "Environment" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Variables" : {
          "type" : "object"
        },
        "Execution" : {
          "$ref" : "#/definitions/Execution"
        },
        "ResourceAccessPolicies" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/ResourceAccessPolicy"
          }
        },
        "AccessSysfs" : {
          "type" : "boolean"
        }
      }
    },
    "ResourceAccessPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ResourceId" : {
          "type" : "string"
        },
        "Permission" : {
          "type" : "string"
        }
      },
      "required" : [ "ResourceId" ]
    }
  },
  "required" : [ "FunctionDefinitionId", "Functions" ],
  "createOnlyProperties" : [ "/properties/Functions", "/properties/FunctionDefinitionId", "/properties/DefaultConfig" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}