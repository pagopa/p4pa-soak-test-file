#!/bin/bash

BASE_URL="$1"
ORG_IPA_CODE="$2"
CLIENT_SECRET_PU="$3"
FILE_TYPE="$4"
FILE_VERSION="$5"
N_ROWS="$6"
DP_TYPE_ORG_CODE="$7"

function print_help() {
   echo "To run the script you have to provide the following parameters:"
   echo "1. BASE_URL"
   echo "2. ORG_IPA_CODE"
   echo "3. CLIENT_SECRET_PU"
   echo "4. FILE_TYPE"
   echo "5. FILE_VERSION"
   echo "6. N_ROWS"
   echo "7. DP_TYPE_ORG_CODE"
   echo ""
}

function checkEnv() {
    if [ -z "$(printenv "$1")" ]
    then
      print_help
      echo "An error occurred: $1 is not set"
      exit 1
    fi
}

checkEnv BASE_URL
checkEnv ORG_IPA_CODE
checkEnv CLIENT_SECRET_PU
checkEnv FILE_TYPE
checkEnv FILE_VERSION
checkEnv N_ROWS

AUTH_RESPONSE=$(curl -s --location --request POST \
               "$BASE_URL/pu/auth/oauth/token?client_id=piattaforma-unitaria_$ORG_IPA_CODE&grant_type=client_credentials&scope=openid&client_secret=$CLIENT_SECRET_PU" \
               -d "")
ACCESS_TOKEN=$(echo "$AUTH_RESPONSE" | jq -r .access_token)
if [ "$ACCESS_TOKEN" == "null" ]; then
  echo "Cannot obtain an access token!"
  exit 1
fi

USERINFO_RESPONSE=$(curl -s --location --request GET \
                  "$BASE_URL/pu/auth/oauth/userinfo" \
                  --header "Authorization: Bearer $ACCESS_TOKEN")
ORGANIZATION_ID=$(echo "$USERINFO_RESPONSE" | jq '.organizations [0].organizationId')
if [[ -z "${ORGANIZATION_ID}" ]]; then
  echo "Cannot obtain organizationId!"
  echo "$USERINFO_RESPONSE"
  exit 1
fi
echo "Obtained accessToken for organization: $ORGANIZATION_ID"

PY_SCRIPT="./src/generateImportFile_$FILE_TYPE.py"
chmod +x "$PY_SCRIPT"
FILE_TO_UPLOAD=$(python3 -m pipenv run python "$PY_SCRIPT" "$FILE_VERSION" "$N_ROWS" "$DP_TYPE_ORG_CODE")
if [[ -z "${FILE_TO_UPLOAD}" ]]; then
  echo "Cannot generate file to upload!"
  exit 1
fi
echo "Generated file to upload: $FILE_TO_UPLOAD"

IMPORT_RESPONSE=$(curl -s --location --globoff "$BASE_URL/pu/fileshare/organization/$ORGANIZATION_ID/ingestionflowfiles?ingestionFlowFileType=$FILE_TYPE&fileOrigin=SIL" \
                --header "Authorization: Bearer $ACCESS_TOKEN" \
                --form "ingestionFlowFile=@\"./$FILE_TO_UPLOAD\"")
if [[ -z "${IMPORT_RESPONSE}" ]]; then
  echo "No body returned from upload invoke!"
  exit 1
else
  echo "Import response: $IMPORT_RESPONSE"
fi

INGESTION_FLOW_FILE_ID=$(echo "$IMPORT_RESPONSE" | jq .ingestionFlowFileId)
if [[ -z "${INGESTION_FLOW_FILE_ID}" ]]; then
  echo "Cannot read ingestionFlowFileId from response!"
  exit 1
fi

echo "Imported $FILE_TYPE with ingestionFlowFileId $INGESTION_FLOW_FILE_ID"