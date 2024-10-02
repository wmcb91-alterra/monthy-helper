# Monthly Report Helper

Simple helper script to make creating a monthly report easier. Opens Github repos
to closed PRs where you are the author and the PR was closed the previous month.

The default assumption is you are running this script to create a monthly report for the
previous month. So if you are running this on June 6th, it will help find relevant
information from May 1st to May 31st.

## Installation

```bash
git clone git@github.com:wmcb91-alterra/monthy-helper.git
cd monthy-helper
```

## Usage

Basic usage:

```bash
python3 monthly_helper.py
```

Additional options:

```md
python3 monthly_helper.py [-h] [-m {1,2,3,4,5,6,7,8,9,10,11,12}] [-b DAY_BUFFER] [-md] [--include-reviewed] [--skip-jira] [--skip-github]

options:
  -h, --help            show this help message and exit
  -m {1,2,3,4,5,6,7,8,9,10,11,12}, --month {1,2,3,4,5,6,7,8,9,10,11,12}
                        The month for the report.
  -b DAY_BUFFER, --day-buffer DAY_BUFFER
                        Number of days to look outside of prior month.
  -md, --use-merged-date
                        Use the merged date instead of the created date for PR filters.
  --include-reviewed    Also will open Github PRs filtered to show those you reviewed in the previous month.
  --skip-jira           Don't open the Jira issues page.
  --skip-github         Don't open the Github PR pages.
```

## Config

The first time you run the script, it will be prompted to configure the script.
The configuration will be stored in a file called `config.json` in the same
directory as the script. And can be manually edited if needed. The configuration
file should look like the following:

```json
{
  "github_username": "YOUR_USERNAME",
  "github_org": "YOUR_GH_ORG",
  "github_repos": [
    "REPO_NAME_1",
    "REPO_NAME_2",
  ],
  "jira_org": "YOUR_JIRA_ORG",
}
```

If you don't want to use the `--skip-jira` or `--skip-github` flags, you can set
"github_username", "github_org", or "jira_org" to an empty string in the
config and the script will skip opening those pages.
