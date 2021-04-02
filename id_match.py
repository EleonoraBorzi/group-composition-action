import os
import sys

def extract_candidates(file_changes, base_folder):
    ret = [] 
    for i in file_changes:
        folders = i.split("/")
        is_candidate = True
        for j, name in enumerate(base_folder):
            if(name != folders[j]):
                is_candidate = False
                break
        if is_candidate:
            ret.append(folders)
    return ret

def extract_readme(candidates):
    return [e for e in candidates if e [-1].lower() == "readme.md"]

def extract_and_sort_names(folder_name : str) -> "list of str":
    l = folder_name.split("-")
    l.sort()
    return l

def check_readme(list_id, path_readme):
    file_content = []
    with open(path_readme, 'r') as f:
        file_content = f.read()
    is_ok = True
    for id in list_id:
        if id + "@kth.se" not in file_content:
            is_ok = False
            break
    return is_ok
#check_readme(["acti"], "README.md")   


if __name__ == "__main__":
    file_changes = sys.argv[1][1:-1].split(",")
    base_folder = sys.argv[2]
    base_folder = base_folder.split("/")[:-1]
    candidates = extract_candidates(file_changes, base_folder)
    list_readme = extract_readme(candidates)
    if len(list_readme)!=1:
        report = "Invalid, is this a TA?"
        print("::set-output name=report::" + report)
        print("::set-output name=idsMatch::" + "false")
    else:
        list_id = extract_and_sort_names(list_readme[0][-2])
        is_valid = check_readme(list_id, "/".join(list_readme[0]))
        if is_valid == True:
            report = "The name in the folder matched with the email addresses in the README file"
            print("::set-output name=report::" + report)
            print("::set-output name=folderName::" + list_readme[0][-2])
            print("::set-output name=idsMatch::" + "true")
        else: 
            report = "The name in the folder did not match with the email addresses in the README file, please revise the pull request" 
            print("::set-output name=report::" + report)
            print("::set-output name=folderName::" + list_readme[0][-2])
            print("::set-output name=idsMatch::" + "false")
