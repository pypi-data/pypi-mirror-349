SCHEMA = {
  "typeName" : "AWS::SageMaker::NotebookInstance",
  "description" : "Resource Type definition for AWS::SageMaker::NotebookInstance",
  "additionalProperties" : False,
  "properties" : {
    "KmsKeyId" : {
      "type" : "string"
    },
    "VolumeSizeInGB" : {
      "type" : "integer"
    },
    "AdditionalCodeRepositories" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "DefaultCodeRepository" : {
      "type" : "string"
    },
    "DirectInternetAccess" : {
      "type" : "string"
    },
    "PlatformIdentifier" : {
      "type" : "string"
    },
    "AcceleratorTypes" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "SubnetId" : {
      "type" : "string"
    },
    "SecurityGroupIds" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
    },
    "RoleArn" : {
      "type" : "string"
    },
    "InstanceMetadataServiceConfiguration" : {
      "$ref" : "#/definitions/InstanceMetadataServiceConfiguration"
    },
    "RootAccess" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "NotebookInstanceName" : {
      "type" : "string"
    },
    "InstanceType" : {
      "type" : "string"
    },
    "LifecycleConfigName" : {
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
    "InstanceMetadataServiceConfiguration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MinimumInstanceMetadataServiceVersion" : {
          "type" : "string"
        }
      },
      "required" : [ "MinimumInstanceMetadataServiceVersion" ]
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
  "required" : [ "InstanceType", "RoleArn" ],
  "createOnlyProperties" : [ "/properties/KmsKeyId", "/properties/NotebookInstanceName", "/properties/SecurityGroupIds", "/properties/SubnetId", "/properties/DirectInternetAccess", "/properties/PlatformIdentifier" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}