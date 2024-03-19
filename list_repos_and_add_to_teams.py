import argparse
import requests
import os


def list_repos_and_add_to_github_teams(org_name: str, github_team_name: str, search_string: str, permission: str):
    """
    function to add specific repos matching a string in repo names to a github teams
    :return:
    """
    # GitHub endpoint for listing repos under an organization
    repo_url = f"https://api.github.com/orgs/{org_name}/repos"
    print(f"github api endpoint url {repo_url}")

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.getenv('GH_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Define pagination parameters
    per_page = 100  # Number of records per page
    page = 1        # Initial page number
    list_of_repo_names = []

    while True:
        # Add pagination parameters to the URL
        params = {'per_page': per_page, 'page': page}
        response = requests.get(repo_url, headers=headers, params=params)
        response_json = response.json() ## Github repo details

        # Checking the API status code
        if response.status_code == 200:
            print(f"API request successful on {repo_url}")
            # print(response_json)
        else:
            print(f"API request failed with status code {response.status_code}:")
            # print(response_json)
            break

        # Get the repo names from the list of dictionaries and add to another list
        for repo in response_json:
            list_of_repo_names.append(repo['full_name'])

        page += 1  # Move to the next page

        # Break the loop if no more pages
        if len(response_json) < per_page:
            break

    for repo in list_of_repo_names:
        print(f" repo name: {repo} ")

    print(f"Total Number of repos in {org_name} Org is {len(list_of_repo_names)}")

    # Finding repos starting with search string
    matching_repos = [repo for repo in list_of_repo_names if repo.startswith(f'{org_name}/{search_string}')]
    print(f"Matching repos {search_string} are: {matching_repos}")

    ### Adding repos to teams ###
    # GitHub endpoint for listing teamws under an organization
    team_url = f"https://api.github.com/orgs/{org_name}/teams?per_page={per_page}"
    print(f"github api endpoint url {team_url}")

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.getenv('GH_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    page = 1  # Initial page number
    while True:
        params = {'per_page': per_page, 'page': page}
        response = requests.get(team_url, headers=headers, params=params)
        response_json = response.json() ## Github team details
        print("wait")

        team_slug = ""  # defining empty team slug
        for team in response_json:
            if team['name'] == github_team_name:
                team_slug = team['slug']
        print(f"GitHub team slug is : {team_slug}")

        for repo in matching_repos:
            print(f"Adding {repo} to {github_team_name} team")

            # GitHub endpoint for adding repos to a team in an organization
            repo_addition_url = f"https://api.github.com/orgs/{org_name}/teams/{team_slug}/repos/{repo}"
            print(f"github api endpoint url {repo_addition_url}")

            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {os.getenv('GH_TOKEN')}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            data = {
                "permission": permission
            }

            response = requests.put(repo_addition_url, headers=headers, params=params, json=data)
            print(f"Repository {repo} successfully added to {github_team_name} with permission {permission}")
         # Increment page number
        page += 1
        # Break the loop if no more pages
        if len(response_json) < per_page:
            break


def main():
    """main function to test the code"""
    parser = argparse.ArgumentParser(description="Add specific repos matching a string in repo names to a github teams")
    parser.add_argument("--org_name",required=True, type=str, help="Github org name")
    parser.add_argument("--github_team_name",required=True, type=str, help="Your GitHub team name")
    parser.add_argument("--search_string", required=True, type=str, help="github repo name search string")
    parser.add_argument("--permission", required=True,choices=['admin', 'push', 'pull', 'triage', 'maintain'], help="Permissions for Github teams across repository" )
    args = parser.parse_args()
    os.environ["GH_TOKEN"] = "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"
    org_name = args.org_name
    github_team_name = args.github_team_name
    search_string = args.search_string
    permission = args.permission


    # function call
    list_repos_and_add_to_github_teams(org_name, github_team_name, search_string, permission)


if __name__ == "__main__":
    main()