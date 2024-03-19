# list-repos-in-organization-based-on-name-and-add-to-github-teams
list-repos-in-organization-based-on-name-and-add-to-github-teams

# JIRA LINK
This is associated with the JIRA story [DEVOPS-39](https://devwithkrishna.atlassian.net/browse/DEVOPS-39)

#  DESCRIPTION 

This Python program uses the GitHub API to list repositories under a specified organization, filter repositories based on a search string in their names, and add the matching repositories to a specified GitHub team with a specified permission level.

## Here's a high-level overview of the program:

## Function Definitions:

list_repos_and_add_to_github_teams: This function takes the organization name (org_name), GitHub team name (github_team_name), search string (search_string), and permission level (permission) as input. It lists all repositories under the organization, filters them based on the search string, and adds the matching repositories to the specified GitHub team with the specified permission level.

### Main Function:

The main function parses command-line arguments (org_name, github_team_name, search_string, permission) using the argparse module.
It then calls the list_repos_and_add_to_github_teams function with the parsed arguments.

### GitHub API Calls:

The program makes several API calls to the GitHub API using the requests module to list repositories, list teams, and add repositories to teams.
It uses the Authorization header with a GitHub token (os.getenv('GH_TOKEN')) for authentication.

### Pagination:

The program handles pagination for listing repositories and teams by incrementing the page parameter in the API request until all repositories or teams are listed.

### Error Handling:

The program checks the status code of the API response and prints an error message if the request fails.
Overall, this program provides a convenient way to automate the process of adding specific repositories to GitHub teams based on a search string in their names, with customizable permission levels.

# Program Inputs

The program requires 4 Inputs which are passed as inputs on GitHub workflow

* org_name --> GitHub Organization name
* github_team_name --> GithHub team name
* search_string --> GitHub repo name search string
* permission --> Permissions for Github teams across repository `admin`,`push`,`pull`,`maintain`,`triage`

```
    pipenv run python3 list_repos_and_add_to_teams.py --org_name ${{ inputs.org_name }} \
          --github_team_name ${{ inputs.github_team_name }} --search_string ${{ inputs.search_string }} \
          --permission ${{ inputs.permission }}
```

>[!NOTE]
> This Program uses Personal Access token for Github authentication and passed as a environment variable in
> GitHub Workflow from GitHub Secrets.