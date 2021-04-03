import sys

def repair_file_path(file_path : str) -> str:
    ret = file_path
    # Remove unwanted prefix
    if len(ret) >= 1 and ret[0] == "/":
        ret = ret[1:]
    if len(ret) == 1 and ret[0] == ".":
        ret = ret[1:]
    if len(ret) >= 2 and ret[0] == "." and ret[1] == "/":
        ret = ret[2:]
    # This one is probably redundant.
    if len(ret) >= 1 and ret[0] == "/":
        ret = ret[1:]
    return ret

def repair_folder_path(folder_path: str) -> str:
    ret = repair_file_path(folder_path)
    # Add desired postfix
    if len(ret) >= 1 and ret[-1] != "/":
        ret += "/" 
    return ret

# Returns all file additions that were made within the base folder. 
# The added files are returned as lists of the folders (and file name) constituting their paths.
# E.g. a file "fol1/fol2/fol3/file1.txt" is represented as ["fol1", "fol2", "fol3", "file1.txt"]
def extract_candidates(file_additions : "list of str", base_folder_segments : "list of str") -> "list of lists of str":
    ret = [] 
    for file_path in file_additions:
        path_segments = file_path.split("/")
        is_candidate = True
        for j, base_segment in enumerate(base_folder_segments):
            if(base_segment != path_segments[j]):
                is_candidate = False
                break
        if is_candidate:
            ret.append(path_segments)
    return ret

# Returns the files which are named "README.md" (capitalization doesn't matter)
def extract_readme(candidates : "list of lists of str") -> "list of lists of str":
    return [e for e in candidates if e[-1].lower() == "readme.md"]

# Given a string "name1-name2-...", returns a list of all strings that are seperated by a hyphen. 
# The strings are also sorted so that e.g. "name1-name2" and "name2-name1" are considered equal. 
def extract_and_sort_names(folder_name : str) -> "list of str":
    l = folder_name.split("-")
    l.sort()
    return l

# Returns true if the readme contains KTH mail addresses corresponding to the ID:s extracted from its parent folder name.
def readme_is_valid(id_list : "list of str", readme_path : str) -> bool:
    file_content = []
    with open(readme_path, 'r') as f:
        file_content = f.read()
    is_valid = True
    for kth_id in id_list:
        if kth_id + "@kth.se" not in file_content:
            is_valid = False
            break
    return is_valid

# Expects two commandline arguments:
# - paths of files that have been added on the form [file1_path,file2_path,...] or ["file1_path","file2_path","..."] . 
# - the path to the base folder which is the folder that is to be considered root when running this script. 
# For all paths specified, they should not begin with a "./" but every other folder in the path should be followed by "/" . 
# E.g. "fol/base_folder/" . 
# Pointing to current directory would be just the empty string "".
# However, even if the input deviates from this it's attempted to repair it.
if __name__ == "__main__":
    file_additions = sys.argv[1][1:-1].split(",")
    for i, f in enumerate(file_additions):
        file_additions[i] = repair_file_path(f)
    base_folder = sys.argv[2]
    base_folder = repair_folder_path(base_folder)
    base_folder_segments = base_folder.split("/")[:-1]
    candidates = extract_candidates(file_additions, base_folder_segments)
    readme_list = extract_readme(candidates)

    report = ""

    if len(readme_list) != 1:
        report += "There wasn't exactly one readme added under \"" + base_folder + "\" . If this is a student submission, it's invalid.\n"
        valid_readme = False
    else:
        print("::set-output name=folderName::" + readme_list[0][-2])
        id_list = extract_and_sort_names(readme_list[0][-2]) # There is only one readme, and the ID:s should be in the immediate parent folder name.
        is_valid = readme_is_valid(id_list, "/".join(readme_list[0]))   
        if is_valid:
            report +=  "The ID:s constituting the folder name matched with the email addresses in the README file.\n"
            valid_readme = True
        else:
            report += "The ID:s constituting the folder name did not match with the email addresses in the README file. "
            report += "If this is a student submission, please revise the pull request.\n" 
            valid_readme = False

    print("::set-output name=report::" + report)
    print("::set-output name=idsMatch::" + ("true" if valid_readme else "false"))

