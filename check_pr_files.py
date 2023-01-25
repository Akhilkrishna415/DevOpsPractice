import requests
import json
import re

def get_files_in_branch(owner, repo, branch, token):
    headers = {"Authorization": f"Token {token}"}
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/file_pattern_test?ref={branch}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"An error occurred while fetching the files in the {branch} branch.")
        exit(1)
    files = json.loads(response.text)
    all_files = []
    for file in files:
        if file["type"] == "dir":
            # Recursively get files in subfolder
            all_files += get_files_in_subfolder(owner, repo, branch, file["path"], token)
        else:
            all_files.append(file)
    return all_files

def get_files_in_subfolder(owner, repo, branch, path, token):
    headers = {"Authorization": f"Token {token}"}
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"An error occurred while fetching the files in the {path} subfolder.")
        exit(1)
    files = json.loads(response.text)
    all_files = []
    for file in files:
        if file["type"] == "dir":
            # Recursively get files in subfolder
            all_files += get_files_in_subfolder(owner, repo, branch, file["path"], token)
        else:
            all_files.append(file)
    return all_files

def compare_branch_files(owner, repo, pr_number, token):
    # Get the files in Pull request
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("An error occurred while fetching the pull request data.")
        exit(1)
    pull_request_files = json.loads(response.text)

    main_branch_files = get_files_in_branch(owner, repo, "main", token)

    for file in pull_request_files:
        # Extract the unique number prefix from the file name
        pull_request_file_version = re.search(r'[vmu](\d+)__', file["filename"]).group(1)
        match_found = False

        # Compare the unique number prefix with the ones in the main branch
        for main_file in main_branch_files:
            main_file_version = re.search(r'[vmu](\d+)__', main_file["name"]).group(1)
            if main_file_version == pull_request_file_version:
                match_found = True
                break
        if match_found:
            print(f"WARNING: A file with the same version number prefix '{pull_request_file_version}' already exists in the main branch: {file['filename']}")

# Github token
token = "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"

# Repository owner and name
owner = "Akhilkrishna415"
repo = "DevOpsPractice"

pr_number = 4
compare_branch_files(owner, repo, pr_number, token)
