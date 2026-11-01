#!/bin/sh
# upload.sh PROJECT_ID FILE METADATA_JSON : CurseForge Upload API, prints the response ({"id": ...})
SP=/tmp/claude-0/-home-user-Kasax-Challenge-Craft/2061deb3-7247-5b5c-aa62-6c43681c8da7/scratchpad
curl -sS -m 600 -w '\nHTTP %{http_code}\n' -H "X-Api-Token: $(cat $SP/.cf_token)" \
  -F "metadata=<$3;type=application/json" -F "file=@$2" \
  "https://minecraft.curseforge.com/api/projects/$1/upload-file"
