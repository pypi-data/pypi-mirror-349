SCHEMA = {
  "typeName" : "AWS::ElasticLoadBalancingV2::ListenerCertificate",
  "description" : "Resource Type definition for AWS::ElasticLoadBalancingV2::ListenerCertificate",
  "additionalProperties" : False,
  "properties" : {
    "ListenerArn" : {
      "type" : "string"
    },
    "Certificates" : {
      "type" : "array",
      "uniqueItems" : True,
      "items" : {
        "$ref" : "#/definitions/Certificate"
      }
    },
    "Id" : {
      "type" : "string"
    }
  },
  "definitions" : {
    "Certificate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CertificateArn" : {
          "type" : "string"
        }
      }
    }
  },
  "required" : [ "ListenerArn", "Certificates" ],
  "createOnlyProperties" : [ "/properties/ListenerArn" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id" ]
}