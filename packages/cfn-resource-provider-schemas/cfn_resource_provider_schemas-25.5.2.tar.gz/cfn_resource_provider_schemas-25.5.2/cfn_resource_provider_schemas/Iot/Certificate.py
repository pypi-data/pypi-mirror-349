SCHEMA = {
  "typeName" : "AWS::IoT::Certificate",
  "description" : "Use the AWS::IoT::Certificate resource to declare an AWS IoT X.509 certificate.",
  "sourceUrl" : "https://github.com/aws-cloudformation/aws-cloudformation-rpdk.git",
  "definitions" : { },
  "properties" : {
    "CACertificatePem" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 65536
    },
    "CertificatePem" : {
      "type" : "string",
      "minLength" : 1,
      "maxLength" : 65536
    },
    "CertificateSigningRequest" : {
      "type" : "string"
    },
    "CertificateMode" : {
      "type" : "string",
      "enum" : [ "DEFAULT", "SNI_ONLY" ]
    },
    "Status" : {
      "type" : "string",
      "enum" : [ "ACTIVE", "INACTIVE", "REVOKED", "PENDING_TRANSFER", "PENDING_ACTIVATION" ]
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    }
  },
  "tagging" : {
    "taggable" : False,
    "tagOnCreate" : False,
    "tagUpdatable" : False,
    "cloudFormationSystemTags" : False
  },
  "additionalProperties" : False,
  "required" : [ "Status" ],
  "createOnlyProperties" : [ "/properties/CertificateSigningRequest", "/properties/CACertificatePem", "/properties/CertificatePem", "/properties/CertificateMode" ],
  "writeOnlyProperties" : [ "/properties/CertificateSigningRequest", "/properties/CACertificatePem" ],
  "readOnlyProperties" : [ "/properties/Arn", "/properties/Id" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "iot:CreateCertificateFromCsr", "iot:RegisterCertificate", "iot:RegisterCertificateWithoutCA", "iot:DescribeCertificate" ]
    },
    "read" : {
      "permissions" : [ "iot:DescribeCertificate" ]
    },
    "update" : {
      "permissions" : [ "iot:UpdateCertificate", "iot:DescribeCertificate" ]
    },
    "delete" : {
      "permissions" : [ "iot:DeleteCertificate", "iot:UpdateCertificate", "iot:DescribeCertificate" ]
    },
    "list" : {
      "permissions" : [ "iot:ListCertificates" ]
    }
  }
}