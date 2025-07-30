SCHEMA = {
  "typeName" : "AWS::EMR::SecurityConfiguration",
  "description" : "Use a SecurityConfiguration resource to configure data encryption, Kerberos authentication, and Amazon S3 authorization for EMRFS.",
  "tagging" : {
    "taggable" : False
  },
  "properties" : {
    "Name" : {
      "description" : "The name of the security configuration.",
      "type" : "string"
    },
    "SecurityConfiguration" : {
      "description" : "The security configuration details in JSON format.",
      "type" : [ "object", "string" ]
    }
  },
  "additionalProperties" : False,
  "required" : [ "SecurityConfiguration" ],
  "createOnlyProperties" : [ "/properties/Name", "/properties/SecurityConfiguration" ],
  "primaryIdentifier" : [ "/properties/Name" ],
  "handlers" : {
    "create" : {
      "permissions" : [ "elasticmapreduce:CreateSecurityConfiguration", "elasticmapreduce:DescribeSecurityConfiguration" ]
    },
    "read" : {
      "permissions" : [ "elasticmapreduce:DescribeSecurityConfiguration" ]
    },
    "delete" : {
      "permissions" : [ "elasticmapreduce:DeleteSecurityConfiguration" ]
    },
    "list" : {
      "permissions" : [ "elasticmapreduce:ListSecurityConfigurations" ]
    }
  }
}