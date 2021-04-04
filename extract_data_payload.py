import os
import sys
import json
  
     
def get_values_json(payload):
    payloads = json.dumps(payload)
    quotes_payload = json.loads(payload)
    #Extract branch of main repo
    main_branch = quotes_payload['pull_request']
    main_branch = main_branch['base']
    main_branch = main_branch['ref']
    #Extract branch of forked repo
    head_branch = quotes_payload['pull_request']
    head_branch = head_branch['head']
    head_branch = head_branch['ref']
    #Extract name of main repo
    main_repo = quotes_payload['pull_request']
    main_repo = main_repo['base']
    main_repo = main_repo['repo']
    main_repo = main_repo['full_name']
    #Extract name of forked repo
    head_repo = quotes_payload['pull_request']
    head_repo = head_repo['head']
    head_repo = head_repo['repo']
    head_repo = head_repo['full_name']
    #Extract pull request number 
    pull_number = quotes_payload['number']
    

    print("::set-output name=baseRef::" + main_branch)
    print("::set-output name=headRef::" + head_branch)
    print("::set-output name=baseRepo::" + main_repo)
    print("::set-output name=headRepo::" + head_repo)
    print("::set-output name=pullNumber::" + str(pull_number)) 

    
if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, 'r') as myfile:
      data=myfile.read()
    try:
      get_values_json(data)
    except: 
      print("::set-output name=isPullReq::" + "false")
