#!/bin/bash

set -e

curl -LO https://schema.cloudformation.eu-central-1.amazonaws.com/CloudformationSchema.zip
unzip -d CloudformationSchema CloudformationSchema.zip
rm -f cfn_resource_provider_schemas/**/*.py
find cfn_resource_provider_schemas -type d -empty -delete

for file in CloudformationSchema/*.json; do
    filename="${file##*/}"
    filename="${filename%%.*}"
    IFS="-" read -r service schema <<<"${filename//aws-/}"
    service="${service^}"
    service="${service//-/}"
    schema="${schema^}"
    schema="${schema//-/}"
    mkdir -p "cfn_resource_provider_schemas/${service}"
    touch "cfn_resource_provider_schemas/${service}/__init__.py"
    sed \
        -e 's,^{,SCHEMA = {,' \
        -e 's,true,True,' \
        -e 's,false,False,' \
        -e 's,null,None,' \
        "${file}" >"cfn_resource_provider_schemas/${service}/${schema}.py"
    if ! grep -q "import cfn_resource_provider_schemas.${service} as ${service}" "cfn_resource_provider_schemas/__init__.py"; then
        echo "import cfn_resource_provider_schemas.${service} as ${service}" >>"cfn_resource_provider_schemas/__init__.py"
    fi
    if ! grep -q "from cfn_resource_provider_schemas.${service}.${schema} import SCHEMA as ${schema}" "cfn_resource_provider_schemas/${service}/__init__.py"; then
        echo "from cfn_resource_provider_schemas.${service}.${schema} import SCHEMA as ${schema}" >>"cfn_resource_provider_schemas/${service}/__init__.py"
    fi
done

uv build
