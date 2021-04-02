import os
import sys
import json
  
     
def get_values_json(payload):
    payloads = json.dumps(payload)
    quotes_payload = json.loads(payload)
    print("aight")
    main_branch = quotes_payload['after']
    #main_branch = quotes_payload['pull_request']['base']['ref']
    print("Ok")
    print(main_branch)
    head_branch = quotes_payload['pull_request']['head']['ref']
    main_repo = quotes_payload['pull_request']['base']['repo']['full_name']
    head_repo = quotes_payload['pull_request']['head']['repo']['full_name']
     
    print("::set-output name=baseBr::" + main_branch)
    print("::set-output name=headBr::" + head_branch)
    print("::set-output name=baseNm::" + main_repo)
    print("::set-output name=headNm::" + head_repo)
    
if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, 'r') as myfile:
      data=myfile.read()
    print(data)
    get_values_json(data)
