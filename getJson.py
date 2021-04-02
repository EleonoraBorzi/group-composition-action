import os
import sys
import json

payloadex = {
    "action": "synchronize",
    "after": "7488e4807c9b905c19e1c217b3e847c227d95ec9",
    "before": "d2e162d6e82630c86724d19187ae739716e6680a",
    "number": 7,
    "pull_request": {
      "base": {
          "ref": "main"
          }
    }}
          
     

def get_values_json(payload):
    payloads = json.dumps(payload)
    quotes_payload = json.loads(payloads)
    main_branch = quotes_payload["pull_request"]["base"]["ref"]
    head_branch = quotes_payload["pull_request"]["head"]["ref"]
    main_repo = quotes_payload["pull_request"]["base"]["full_name"]
    head_repo = quotes_payload["pull_request"]["head"]["full_name"]
     
    print("::set-output name=baseBr::" + main_branch)
    print("::set-output name=headBr::" + head_branch)
    print("::set-output name=baseNm::" + main_repo)
    print("::set-output name=headNm::" + head_repo)

