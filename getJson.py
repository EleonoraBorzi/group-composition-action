import os
import sys
import json
  
     
def get_values_json(payload):
   # payloads = json.dumps(payload)
    quotes_payload = json.loads(payload)
    main_branch = quotes_payload['pull_request']['base']['ref']
    head_branch = quotes_payload['pull_request']['head']['ref']
    main_repo = quotes_payload['pull_request']['base']['repo']['full_name']
    head_repo = quotes_payload['pull_request']['head']['repo']['full_name']
     
    print("::set-output name=baseBr::" + main_branch)
    print("::set-output name=headBr::" + head_branch)
    print("::set-output name=baseNm::" + main_repo)
    print("::set-output name=headNm::" + head_repo)
    
if __name__ == "__main__":
    get_values_json(sys.argv)
