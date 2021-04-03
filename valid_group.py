import json
import os
import sys

# Given a string "name1-name2-...", returns a list of all strings that are seperated by a hyphen.
# The strings are also sorted so that e.g. "name1-name2" and "name2-name1" are considered equal.
def extract_and_sort_names(folder_name : str) -> "list of str":
    l = folder_name.split("-")
    l.sort()
    return l

# Returns the possible sorted subgroups, including the empty group as the first entry. Thus [1:] will return groups of at least one element.
# Member inclusions can be set as list of ints. This will make it so that the index of the member inclusions list will indicate whether to include 
# a particular member when creating subgroups or not. An int of at least 1 is required to include the member.
def subgroups_recursion(group_members: "list of str", index : int, member_inclusions=None) -> "list of lists of str":
    if index >= len(group_members):
        return [[]]
    subgroups = subgroups_recursion(group_members, index + 1, member_inclusions=member_inclusions)
    additions = []
    if member_inclusions == None or member_inclusions[len(group_members) - 1 - index] > 0:
        for l in subgroups:
            new_entry = l.copy()
            new_entry.append(group_members[len(group_members) - 1 - index])
            additions.append(new_entry)
    return subgroups + additions

# Returns a list of tuples with the number of collaborations among the subgroups of the group members, along with which group members are part of this.
# The subgroups considered are at least of size 2.
# The special case of a group with a single members does not count as a subset to anything else but itself.
def most_collaborations(base_folder : str, group_members : "list of str") -> "list of pairs (int, list of str)":
    # https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory 
    folder_lists = [x[1] for x in os.walk(base_folder) if x[1] != []]
    folders = [item for sublist in folder_lists for item in sublist]
    
    subgroupsR = subgroups_recursion(group_members, 0)
    subgroups = [sub for sub in subgroupsR if len(sub) > 1]

    subgroups_map = {}
    for sub in subgroups:
        subgroups_map["-".join(sub)] = 0

    if len(group_members) == 1:
        counter = 0
        for f in folders:
            if f == group_members[0]:
                counter += 1
        return [(counter, [group_members[0]])]

    for f in folders:
        name_inclusions = [0 for _ in group_members]
        names = extract_and_sort_names(f)
        for n1 in names:
            for i, n2 in enumerate(group_members):
                if n1 == n2:
                    name_inclusions[i] += 1
        keysR = subgroups_recursion(group_members, 0, member_inclusions=name_inclusions)
        keys = ["-".join(key) for key in keysR if len(key) > 1]
        for key in keys:
            subgroups_map[key] += 1
        
    ret_list = []
    for sub in subgroups:
        ret_list.append((subgroups_map["-".join(sub)], sub))
    return ret_list

# Expects four command line arguments in the following order: 
# - a string with the path to the base folder, 
# - a string with the group folder name,
# - an int with the maximum group size,
# - and an int with the maximum number of times the same group is allowed to work together (this includes groups of only a single person).
def main() -> "no return":
    report = ""
    valid_group = True
    verdict = ""

    group_members = extract_and_sort_names(sys.argv[2])
    collaborations = most_collaborations(sys.argv[1], group_members)
    allowed_group_size = int(sys.argv[3])
    allowed_collaboration_times = int(sys.argv[4])

    for num, members in collaborations:
        if num >= allowed_collaboration_times:
            verdict += "The group consisting of " 
            for g in members:
                verdict += g + ", "
            verdict += "appears to have worked together " + str(num) + " times, while the maximum allowed is " + str(allowed_collaboration_times) + ". "
            verdict += "Consequently they may not work together here.\n"
            valid_group = False

        report += "The group consisting of " 
        for g in members:
            report += g + ", "
        report += "appears to have worked together "  + str(num) + " times.\n"
    report += "Maximum group size allowed: " + str(allowed_group_size) + ".\n"
    report += "Maximum number of collaborations allowed: " + str(allowed_collaboration_times) + ".\n"

    
    if len(group_members) > allowed_group_size:
        verdict += "The group size is " + str(len(group_members))
        verdict += ", but the maximum allowed group size is " + str(allowed_group_size) + ". This group is thus not allowed.\n"
        valid_group = False
    
    if len(verdict) == 0:
        verdict += "The group composition is allowed.\n"
    #print("::set-output name=groupValidityReport::" + report + verdict)
    #print("::set-output name=groupValidity::" + ("true" if valid_group else "false"))
    print(json.dumps({"report":report+verdict, "validity":("true" if valid_group else "false")}))

if __name__ == "__main__":
    main()
