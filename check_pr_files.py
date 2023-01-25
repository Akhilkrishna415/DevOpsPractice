import requests
import json
import re

# Github token
token = "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"

# Repository owner and name
owner = "Akhilkrishna415"
repo = "DevOpsPractice"

pr_number = 2
# Main branch name
# main_branch = "main"

headers = {"Authorization": f"Token {token}"}

# Get the files in Pull request
url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("An error occurred while fetching the pull request data.")
    exit(1)

pull_request_files = json.loads(response.text)


# Get the files in main branch
url = f"https://api.github.com/repos/{owner}/{repo}/contents/file_pattern_test?ref=main"
response = requests.get(url, headers=headers)


if response.status_code != 200:
    print("An error occurred while fetching the files in the main branch.")
    exit(1)

main_branch_files = json.loads(response.text)

for file in pull_request_files:
    # Only consider files in the migrations folder
    if "file_pattern_test" in file["filename"]:
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

        # if match_found is False:
        #     print("something is wrong")
