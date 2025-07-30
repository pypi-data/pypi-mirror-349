SCHEMA = {
  "typeName" : "AWS::Lightsail::LoadBalancerTlsCertificate",
  "description" : "Resource Type definition for AWS::Lightsail::LoadBalancerTlsCertificate",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-lightsail.git",
  "properties" : {
    "LoadBalancerName" : {
      "description" : "The name of your load balancer.",
      "type" : "string",
      "pattern" : "\\w[\\w\\-]*\\w"
    },
    "CertificateName" : {
      "description" : "The SSL/TLS certificate name.",
      "type" : "string"
    },
    "CertificateDomainName" : {
      "description" : "The domain name (e.g., example.com ) for your SSL/TLS certificate.",
      "type" : "string"
    },
    "CertificateAlternativeNames" : {
      "description" : "An array of strings listing alternative domains and subdomains for your SSL/TLS certificate.",
      "type" : "array",
      "uniqueItems" : True,
      "insertionOrder" : False,
      "items" : {
        "type" : "string"
      }
    },
    "LoadBalancerTlsCertificateArn" : {
      "type" : "string"
    },
    "IsAttached" : {
      "description" : "When True, the SSL/TLS certificate is attached to the Lightsail load balancer.",
      "type" : "boolean"
    },
    "HttpsRedirectionEnabled" : {
      "description" : "A Boolean value that indicates whether HTTPS redirection is enabled for the load balancer.",
      "type" : "boolean"
    },
    "Status" : {
      "description" : "The validation status of the SSL/TLS certificate.",
      "type" : "string"
    }
  },
  "additionalProperties" : False,
  "required" : [ "LoadBalancerName", "CertificateName", "CertificateDomainName" ],
  "readOnlyProperties" : [ "/properties/LoadBalancerTlsCertificateArn", "/properties/Status" ],
  "taggable" : True,
  "primaryIdentifier" : [ "/properties/CertificateName", "/properties/LoadBalancerName" ],
  "createOnlyProperties" : [ "/properties/LoadBalancerName", "/properties/CertificateName", "/properties/CertificateDomainName", "/properties/CertificateAlternativeNames" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "lightsail:CreateLoadBalancerTlsCertificate", "lightsail:GetLoadBalancerTlsCertificates", "lightsail:GetLoadBalancer", "lightsail:AttachLoadBalancerTlsCertificate", "lightsail:UpdateLoadBalancerAttribute" ]
    },
    "read" : {
      "permissions" : [ "lightsail:GetLoadBalancerTlsCertificates", "lightsail:GetLoadBalancer" ]
    },
    "update" : {
      "permissions" : [ "lightsail:AttachLoadBalancerTlsCertificate", "lightsail:GetLoadBalancerTlsCertificates", "lightsail:GetLoadBalancer", "lightsail:UpdateLoadBalancerAttribute" ]
    },
    "delete" : {
      "permissions" : [ "lightsail:DeleteLoadBalancerTlsCertificate", "lightsail:GetLoadBalancerTlsCertificates", "lightsail:GetLoadBalancer" ]
    },
    "list" : {
      "permissions" : [ "lightsail:GetLoadBalancerTlsCertificates", "lightsail:GetLoadBalancer" ]
    }
  }
}