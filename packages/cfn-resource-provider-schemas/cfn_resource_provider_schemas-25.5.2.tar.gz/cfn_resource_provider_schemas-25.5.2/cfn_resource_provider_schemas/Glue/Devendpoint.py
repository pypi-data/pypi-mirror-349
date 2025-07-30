SCHEMA = {
  "typeName" : "AWS::Glue::DevEndpoint",
  "description" : "Resource Type definition for AWS::Glue::DevEndpoint",
  "additionalProperties" : False,
  "properties" : {
    "ExtraJarsS3Path" : {
      "type" : "string"
    },
    "PublicKey" : {
      "type" : "string"
    },
    "NumberOfNodes" : {
      "type" : "integer"
    },
    "Arguments" : {
      "type" : "object"
    },
    "SubnetId" : {
      "type" : "string"
    },
    "PublicKeys" : {
      "type" : "array",
      "uniqueItems" : False,
      "items" : {
        "type" : "string"
      }
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
    "WorkerType" : {
      "type" : "string"
    },
    "EndpointName" : {
      "type" : "string"
    },
    "GlueVersion" : {
      "type" : "string"
    },
    "ExtraPythonLibsS3Path" : {
      "type" : "string"
    },
    "SecurityConfiguration" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "NumberOfWorkers" : {
      "type" : "integer"
    },
    "Tags" : {
      "type" : "object"
    }
  },
  "required" : [ "RoleArn" ],
  "createOnlyProperties" : [ "/properties/EndpointName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}