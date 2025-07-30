SCHEMA = {
  "typeName" : "AWS::AppMesh::VirtualNode",
  "description" : "Resource Type definition for AWS::AppMesh::VirtualNode",
  "additionalProperties" : False,
  "properties" : {
    "Uid" : {
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
      "$ref" : "#/definitions/VirtualNodeSpec"
    },
    "VirtualNodeName" : {
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
    "AccessLog" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "File" : {
          "$ref" : "#/definitions/FileAccessLog"
        }
      }
    },
    "ListenerTimeout" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TCP" : {
          "$ref" : "#/definitions/TcpTimeout"
        },
        "HTTP" : {
          "$ref" : "#/definitions/HttpTimeout"
        },
        "HTTP2" : {
          "$ref" : "#/definitions/HttpTimeout"
        },
        "GRPC" : {
          "$ref" : "#/definitions/GrpcTimeout"
        }
      }
    },
    "TlsValidationContextAcmTrust" : {
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
    "ClientPolicy" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TLS" : {
          "$ref" : "#/definitions/ClientPolicyTls"
        }
      }
    },
    "FileAccessLog" : {
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
    "Listener" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ConnectionPool" : {
          "$ref" : "#/definitions/VirtualNodeConnectionPool"
        },
        "Timeout" : {
          "$ref" : "#/definitions/ListenerTimeout"
        },
        "HealthCheck" : {
          "$ref" : "#/definitions/HealthCheck"
        },
        "TLS" : {
          "$ref" : "#/definitions/ListenerTls"
        },
        "PortMapping" : {
          "$ref" : "#/definitions/PortMapping"
        },
        "OutlierDetection" : {
          "$ref" : "#/definitions/OutlierDetection"
        }
      },
      "required" : [ "PortMapping" ]
    },
    "TlsValidationContextTrust" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SDS" : {
          "$ref" : "#/definitions/TlsValidationContextSdsTrust"
        },
        "ACM" : {
          "$ref" : "#/definitions/TlsValidationContextAcmTrust"
        },
        "File" : {
          "$ref" : "#/definitions/TlsValidationContextFileTrust"
        }
      }
    },
    "HealthCheck" : {
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
    "GrpcTimeout" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PerRequest" : {
          "$ref" : "#/definitions/Duration"
        },
        "Idle" : {
          "$ref" : "#/definitions/Duration"
        }
      }
    },
    "VirtualNodeConnectionPool" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "TCP" : {
          "$ref" : "#/definitions/VirtualNodeTcpConnectionPool"
        },
        "HTTP" : {
          "$ref" : "#/definitions/VirtualNodeHttpConnectionPool"
        },
        "HTTP2" : {
          "$ref" : "#/definitions/VirtualNodeHttp2ConnectionPool"
        },
        "GRPC" : {
          "$ref" : "#/definitions/VirtualNodeGrpcConnectionPool"
        }
      }
    },
    "TlsValidationContextFileTrust" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CertificateChain" : {
          "type" : "string"
        }
      },
      "required" : [ "CertificateChain" ]
    },
    "ListenerTlsFileCertificate" : {
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
    "ListenerTlsValidationContextTrust" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "File" : {
          "$ref" : "#/definitions/TlsValidationContextFileTrust"
        },
        "SDS" : {
          "$ref" : "#/definitions/TlsValidationContextSdsTrust"
        }
      }
    },
    "ListenerTlsCertificate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SDS" : {
          "$ref" : "#/definitions/ListenerTlsSdsCertificate"
        },
        "ACM" : {
          "$ref" : "#/definitions/ListenerTlsAcmCertificate"
        },
        "File" : {
          "$ref" : "#/definitions/ListenerTlsFileCertificate"
        }
      }
    },
    "PortMapping" : {
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
    "TcpTimeout" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Idle" : {
          "$ref" : "#/definitions/Duration"
        }
      }
    },
    "ListenerTls" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Validation" : {
          "$ref" : "#/definitions/ListenerTlsValidationContext"
        },
        "Mode" : {
          "type" : "string"
        },
        "Certificate" : {
          "$ref" : "#/definitions/ListenerTlsCertificate"
        }
      },
      "required" : [ "Mode", "Certificate" ]
    },
    "HttpTimeout" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "PerRequest" : {
          "$ref" : "#/definitions/Duration"
        },
        "Idle" : {
          "$ref" : "#/definitions/Duration"
        }
      }
    },
    "VirtualNodeTcpConnectionPool" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxConnections" : {
          "type" : "integer"
        }
      },
      "required" : [ "MaxConnections" ]
    },
    "ServiceDiscovery" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "DNS" : {
          "$ref" : "#/definitions/DnsServiceDiscovery"
        },
        "AWSCloudMap" : {
          "$ref" : "#/definitions/AwsCloudMapServiceDiscovery"
        }
      }
    },
    "ListenerTlsAcmCertificate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "CertificateArn" : {
          "type" : "string"
        }
      },
      "required" : [ "CertificateArn" ]
    },
    "VirtualNodeSpec" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Logging" : {
          "$ref" : "#/definitions/Logging"
        },
        "Backends" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Backend"
          }
        },
        "Listeners" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/Listener"
          }
        },
        "BackendDefaults" : {
          "$ref" : "#/definitions/BackendDefaults"
        },
        "ServiceDiscovery" : {
          "$ref" : "#/definitions/ServiceDiscovery"
        }
      }
    },
    "Logging" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "AccessLog" : {
          "$ref" : "#/definitions/AccessLog"
        }
      }
    },
    "DnsServiceDiscovery" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Hostname" : {
          "type" : "string"
        },
        "IpPreference" : {
          "type" : "string"
        },
        "ResponseType" : {
          "type" : "string"
        }
      },
      "required" : [ "Hostname" ]
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
    "VirtualNodeHttp2ConnectionPool" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxRequests" : {
          "type" : "integer"
        }
      },
      "required" : [ "MaxRequests" ]
    },
    "ClientPolicyTls" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Validation" : {
          "$ref" : "#/definitions/TlsValidationContext"
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
          "$ref" : "#/definitions/ClientTlsCertificate"
        }
      },
      "required" : [ "Validation" ]
    },
    "VirtualServiceBackend" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VirtualServiceName" : {
          "type" : "string"
        },
        "ClientPolicy" : {
          "$ref" : "#/definitions/ClientPolicy"
        }
      },
      "required" : [ "VirtualServiceName" ]
    },
    "AwsCloudMapServiceDiscovery" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Attributes" : {
          "type" : "array",
          "uniqueItems" : False,
          "items" : {
            "$ref" : "#/definitions/AwsCloudMapInstanceAttribute"
          }
        },
        "NamespaceName" : {
          "type" : "string"
        },
        "ServiceName" : {
          "type" : "string"
        },
        "IpPreference" : {
          "type" : "string"
        }
      },
      "required" : [ "NamespaceName", "ServiceName" ]
    },
    "TlsValidationContext" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SubjectAlternativeNames" : {
          "$ref" : "#/definitions/SubjectAlternativeNames"
        },
        "Trust" : {
          "$ref" : "#/definitions/TlsValidationContextTrust"
        }
      },
      "required" : [ "Trust" ]
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
    "AwsCloudMapInstanceAttribute" : {
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
    "BackendDefaults" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "ClientPolicy" : {
          "$ref" : "#/definitions/ClientPolicy"
        }
      }
    },
    "Duration" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "Value" : {
          "type" : "integer"
        },
        "Unit" : {
          "type" : "string"
        }
      },
      "required" : [ "Value", "Unit" ]
    },
    "ListenerTlsSdsCertificate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecretName" : {
          "type" : "string"
        }
      },
      "required" : [ "SecretName" ]
    },
    "TlsValidationContextSdsTrust" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SecretName" : {
          "type" : "string"
        }
      },
      "required" : [ "SecretName" ]
    },
    "Backend" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "VirtualService" : {
          "$ref" : "#/definitions/VirtualServiceBackend"
        }
      }
    },
    "ListenerTlsValidationContext" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "SubjectAlternativeNames" : {
          "$ref" : "#/definitions/SubjectAlternativeNames"
        },
        "Trust" : {
          "$ref" : "#/definitions/ListenerTlsValidationContextTrust"
        }
      },
      "required" : [ "Trust" ]
    },
    "ClientTlsCertificate" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "File" : {
          "$ref" : "#/definitions/ListenerTlsFileCertificate"
        },
        "SDS" : {
          "$ref" : "#/definitions/ListenerTlsSdsCertificate"
        }
      }
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
    "OutlierDetection" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxEjectionPercent" : {
          "type" : "integer"
        },
        "BaseEjectionDuration" : {
          "$ref" : "#/definitions/Duration"
        },
        "MaxServerErrors" : {
          "type" : "integer"
        },
        "Interval" : {
          "$ref" : "#/definitions/Duration"
        }
      },
      "required" : [ "MaxEjectionPercent", "BaseEjectionDuration", "MaxServerErrors", "Interval" ]
    },
    "VirtualNodeGrpcConnectionPool" : {
      "type" : "object",
      "additionalProperties" : False,
      "properties" : {
        "MaxRequests" : {
          "type" : "integer"
        }
      },
      "required" : [ "MaxRequests" ]
    },
    "VirtualNodeHttpConnectionPool" : {
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
    }
  },
  "required" : [ "MeshName", "Spec" ],
  "createOnlyProperties" : [ "/properties/MeshName", "/properties/VirtualNodeName", "/properties/MeshOwner" ],
  "primaryIdentifier" : [ "/properties/Id" ],
  "readOnlyProperties" : [ "/properties/Id", "/properties/ResourceOwner", "/properties/Arn", "/properties/Uid" ]
}