import os
import sys
import json
  
     
def get_values_json(payload):
    payloads = json.dumps(payload)
    quotes_payload = json.loads(payload)
    main_branch = quotes_payload['pull_request']
    main_branch = main_branch['base']
    main_branch = main_branch['ref']
    head_branch = quotes_payload['pull_request']
    head_branch = head_branch['head']
    head_branch = head_branch['ref']
    main_repo = quotes_payload['pull_request']
    main_repo = main_repo['base']
    main_repo = main_repo['repo']
    main_repo = main_repo['full_name']
    head_repo = quotes_payload['pull_request']
    head_repo = head_repo['head']
    head_repo = head_repo['repo']
    head_repo = head_repo['full_name']
    pull_number = quotes_payload['number']
    

     
    print("::set-output name=baseBr::" + main_branch)
    print("::set-output name=headBr::" + head_branch)
    print("::set-output name=baseNm::" + main_repo)
    print("::set-output name=headNm::" + head_repo)
    print("::set-output name=pullNm::" + pull_number)
    
if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, 'r') as myfile:
      data=myfile.read()
    print(data)
    get_values_json(data)
