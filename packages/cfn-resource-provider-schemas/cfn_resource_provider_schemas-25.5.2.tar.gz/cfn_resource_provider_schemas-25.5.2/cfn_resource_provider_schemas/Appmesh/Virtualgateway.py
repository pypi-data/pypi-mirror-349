SCHEMA = {
  "typeName" : "AWS::AppMesh::VirtualGateway",
  "description" : "Resource Type definition for AWS::AppMesh::VirtualGateway",
  "additionalProperties" : False,
  "properties" : {
    "Uid" : {
      "type" : "string"
    },
    "VirtualGatewayName" : {
      "type" : "string"
    },
    "MeshName" : {
      "type" : "string"
    },
    "MeshOwner" : {
      "type" : "string"
    },
    "ResourceOwner" : {
      "type" : "string"
    },
    "Id" : {
      "type" : "string"
    },
    "Arn" : {
      "type" : "string"
    },
    "Spec" : {
      "$ref" : "#/definitions/VirtualGatewaySpec"
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
    "VirtualGatewayListener" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ConnectionPool" : {
          "$ref" : "#/definitions/VirtualGatewayConnectionPool"
        },
        "HealthCheck" : {
          "$ref" : "#/definitions/VirtualGatewayHealthCheckPolicy"
        },
        "TLS" : {
          "$ref" : "#/definitions/VirtualGatewayListenerTls"
        },
        "PortMapping" : {
          "$ref" : "#/definitions/VirtualGatewayPortMapping"
        }
      },
      "required" : [ "PortMapping" ]
    },
    "VirtualGatewayListenerTlsValidationContextTrust" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "File" : {
          "$ref" : "#/definitions/VirtualGatewayTlsValidationContextFileTrust"
        },
        "SDS" : {
          "$ref" : "#/definitions/VirtualGatewayTlsValidationContextSdsTrust"
        }
      }
    },
    "VirtualGatewayAccessLog" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "File" : {
          "$ref" : "#/definitions/VirtualGatewayFileAccessLog"
        }
      }
    },
    "VirtualGatewaySpec" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Logging" : {
          "$ref" : "#/definitions/VirtualGatewayLogging"
        },
        "Listeners" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/VirtualGatewayListener"
          }
        },
        "BackendDefaults" : {
          "$ref" : "#/definitions/VirtualGatewayBackendDefaults"
        }
      },
      "required" : [ "Listeners" ]
    },
    "VirtualGatewayClientPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TLS" : {
          "$ref" : "#/definitions/VirtualGatewayClientPolicyTls"
        }
      }
    },
    "VirtualGatewayHttpConnectionPool" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxConnections" : {
          "type" : "integer"
        },
        "MaxPendingRequests" : {
          "type" : "integer"
        }
      },
      "required" : [ "MaxConnections" ]
    },
    "VirtualGatewayClientPolicyTls" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Validation" : {
          "$ref" : "#/definitions/VirtualGatewayTlsValidationContext"
        },
        "Ports" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "integer"
          }
        },
        "Enforce" : {
          "type" : "boolean"
        },
        "Certificate" : {
          "$ref" : "#/definitions/VirtualGatewayClientTlsCertificate"
        }
      },
      "required" : [ "Validation" ]
    },
    "VirtualGatewayListenerTlsCertificate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SDS" : {
          "$ref" : "#/definitions/VirtualGatewayListenerTlsSdsCertificate"
        },
        "ACM" : {
          "$ref" : "#/definitions/VirtualGatewayListenerTlsAcmCertificate"
        },
        "File" : {
          "$ref" : "#/definitions/VirtualGatewayListenerTlsFileCertificate"
        }
      }
    },
    "VirtualGatewayTlsValidationContextSdsTrust" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecretName" : {
          "type" : "string"
        }
      },
      "required" : [ "SecretName" ]
    },
    "VirtualGatewayFileAccessLog" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Path" : {
          "type" : "string"
        },
        "Format" : {
          "$ref" : "#/definitions/LoggingFormat"
        }
      },
      "required" : [ "Path" ]
    },
    "LoggingFormat" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Text" : {
          "type" : "string"
        },
        "Json" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/JsonFormatRef"
          }
        }
      }
    },
    "VirtualGatewayTlsValidationContext" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SubjectAlternativeNames" : {
          "$ref" : "#/definitions/SubjectAlternativeNames"
        },
        "Trust" : {
          "$ref" : "#/definitions/VirtualGatewayTlsValidationContextTrust"
        }
      },
      "required" : [ "Trust" ]
    },
    "VirtualGatewayListenerTlsValidationContext" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SubjectAlternativeNames" : {
          "$ref" : "#/definitions/SubjectAlternativeNames"
        },
        "Trust" : {
          "$ref" : "#/definitions/VirtualGatewayListenerTlsValidationContextTrust"
        }
      },
      "required" : [ "Trust" ]
    },
    "VirtualGatewayTlsValidationContextFileTrust" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CertificateChain" : {
          "type" : "string"
        }
      },
      "required" : [ "CertificateChain" ]
    },
    "JsonFormatRef" : {
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
    },
    "VirtualGatewayHealthCheckPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Path" : {
          "type" : "string"
        },
        "UnhealthyThreshold" : {
          "type" : "integer"
        },
        "Port" : {
          "type" : "integer"
        },
        "HealthyThreshold" : {
          "type" : "integer"
        },
        "TimeoutMillis" : {
          "type" : "integer"
        },
        "Protocol" : {
          "type" : "string"
        },
        "IntervalMillis" : {
          "type" : "integer"
        }
      },
      "required" : [ "UnhealthyThreshold", "HealthyThreshold", "TimeoutMillis", "Protocol", "IntervalMillis" ]
    },
    "SubjectAlternativeNameMatchers" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Exact" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      }
    },
    "VirtualGatewayTlsValidationContextTrust" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SDS" : {
          "$ref" : "#/definitions/VirtualGatewayTlsValidationContextSdsTrust"
        },
        "ACM" : {
          "$ref" : "#/definitions/VirtualGatewayTlsValidationContextAcmTrust"
        },
        "File" : {
          "$ref" : "#/definitions/VirtualGatewayTlsValidationContextFileTrust"
        }
      }
    },
    "VirtualGatewayListenerTlsAcmCertificate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CertificateArn" : {
          "type" : "string"
        }
      },
      "required" : [ "CertificateArn" ]
    },
    "VirtualGatewayConnectionPool" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "HTTP" : {
          "$ref" : "#/definitions/VirtualGatewayHttpConnectionPool"
        },
        "HTTP2" : {
          "$ref" : "#/definitions/VirtualGatewayHttp2ConnectionPool"
        },
        "GRPC" : {
          "$ref" : "#/definitions/VirtualGatewayGrpcConnectionPool"
        }
      }
    },
    "SubjectAlternativeNames" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Match" : {
          "$ref" : "#/definitions/SubjectAlternativeNameMatchers"
        }
      },
      "required" : [ "Match" ]
    },
    "VirtualGatewayClientTlsCertificate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "File" : {
          "$ref" : "#/definitions/VirtualGatewayListenerTlsFileCertificate"
        },
        "SDS" : {
          "$ref" : "#/definitions/VirtualGatewayListenerTlsSdsCertificate"
        }
      }
    },
    "VirtualGatewayBackendDefaults" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ClientPolicy" : {
          "$ref" : "#/definitions/VirtualGatewayClientPolicy"
        }
      }
    },
    "VirtualGatewayLogging" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AccessLog" : {
          "$ref" : "#/definitions/VirtualGatewayAccessLog"
        }
      }
    },
    "VirtualGatewayGrpcConnectionPool" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxRequests" : {
          "type" : "integer"
        }
      },
      "required" : [ "MaxRequests" ]
    },
    "VirtualGatewayListenerTlsSdsCertificate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecretName" : {
          "type" : "string"
        }
      },
      "required" : [ "SecretName" ]
    },
    "VirtualGatewayListenerTlsFileCertificate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CertificateChain" : {
          "type" : "string"
        },
        "PrivateKey" : {
          "type" : "string"
        }
      },
      "required" : [ "PrivateKey", "CertificateChain" ]
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
    },
    "VirtualGatewayPortMapping" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Protocol" : {
          "type" : "string"
        },
        "Port" : {
          "type" : "integer"
        }
      },
      "required" : [ "Port", "Protocol" ]
    },
    "VirtualGatewayHttp2ConnectionPool" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxRequests" : {
          "type" : "integer"
        }
      },
      "required" : [ "MaxRequests" ]
    },
    "VirtualGatewayTlsValidationContextAcmTrust" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CertificateAuthorityArns" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "type" : "string"
          }
        }
      },
      "required" : [ "CertificateAuthorityArns" ]
    },
    "VirtualGatewayListenerTls" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Validation" : {
          "$ref" : "#/definitions/VirtualGatewayListenerTlsValidationContext"
        },
        "Mode" : {
          "type" : "string"
        },
        "Certificate" : {
          "$ref" : "#/definitions/VirtualGatewayListenerTlsCertificate"
        }
      },
      "required" : [ "Mode", "Certificate" ]
    }
  },
  "required" : [ "MeshName", "Spec" ],
  "createOnlyProperties" : [ "/properties/MeshName", "/properties/VirtualGatewayName", "/properties/MeshOwner" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/ResourceOwner", "/properties/Arn", "/properties/Uid" ]
}