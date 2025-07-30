SCHEMA = {
  "typeName" : "AWS::OpsWorks::ElasticLoadBalancerAttachment",
  "description" : "Resource Type definition for AWS::OpsWorks::ElasticLoadBalancerAttachment",
  "additionalProperties" : False,
  "properties" : {
    "Id" : {
      "type" : "string"
    },
    "ElasticLoadBalancerName" : {
      "type" : "string"
    },
    "LayerId" : {
      "type" : "string"
    }
  },
  "required" : [ "LayerId", "ElasticLoadBalancerName" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}