from datetime import datetime, timedelta
import argparse
import os
import json
import re
import urllib.parse

github_username = ""
github_org = ""
github_repos = []
jira_org = ""

has_config = False
try:
    with open("config.json") as f:
        config = json.load(f)
        github_username = config["github_username"]
        github_org = config["github_org"]
        github_repos = config["github_repos"]
        jira_org = config["jira_org"]

except FileNotFoundError:
    # First time running the script, create a config file from user input
    print("No config file found. Let's create one.")
    print('NOTE: You can always update the "config.json" file manually later.')

except KeyError:
    print('Invalid config file. Please re-enter the data or edit "config.json".')
    raise

except Exception as e:
    print(f"Unexpected error reading config file: {e}.")

else:
    # Runs if no exceptions were raised in try block.
    has_config = True

finally:
    if not has_config:
        print("")
        jira_org = input(
            "Enter your Jira organization (subdomain of Atlassian.net): "
        ).strip()
        github_org = input("Enter your Github organization: ").strip()
        github_username = input("Enter your Github username: ").strip()

        # Get a list of repos to track as a comma-separated list
        print("Enter the list of Github repos you want to track.")
        repo_str = input().strip()
        github_repos = [repo.strip() for repo in repo_str.split(",")]

        with open("config.json", "w") as f:
            json.dump(
                {
                    "github_username": github_username,
                    "github_org": github_org,
                    "github_repos": github_repos,
                    "jira_org": jira_org,
                },
                f,
                indent=2,
            )


jira_filter_jql_template = """
project = "RDC"
AND 
(
    ("developer[user picker (single user)]" = currentUser() OR assignee = currentUser())
    AND "start date[date]" >= "{}"
    AND "start date[date]" <= "{}"
)
OR
(
    reporter IN (currentUser())
    AND created >= "{}" AND created <= "{}"
)
ORDER BY key DESC
"""

# Clean up the JQL query template whitespace for building the URL
jira_filter_jql_template = re.sub(r"\s+", " ", jira_filter_jql_template).strip()


def open_github_pr_pages(
    start_date, end_date, use_merged_date=False, include_reviewed=False
):
    """
    Open Github PR pages for all the repos in the list that were closed in the
    previous month.

    Args:
    - start_date: The first day of the month
    - end_date: The last day of the month

    """
    if len(github_repos) > 0:
        print("Opening PRs for")
        print("\n".join(github_repos))

    date_filter = "created"
    author_filter = "author"

    if use_merged_date:
        date_filter = "merged"

    for repo in github_repos:
        repo_url = f"https://github.com/{github_org}/{repo}/pulls"
        query = f"is:pr {date_filter}:{start_date}..{end_date} {author_filter}:{github_username}"

        os.system(f"open '{repo_url}?q={query}'")

        if include_reviewed:
            query = query.replace(author_filter, "reviewed-by")
            os.system(f"open '{repo_url}?q={query}'")


def open_jira_filter(start_date, end_date):
    """
    Open Jira issue summary with advanced JQL filter that lists:
    - Issues where you are the developer assignee or reporter
    - AND were started (as a dev) or created (as reporter) in the previous month

    Args:
    - start_date: The first day of the month
    - end_date: The last day of the month

    """
    jira_filter_jql = jira_filter_jql_template.format(
        start_date, end_date, start_date, end_date
    )
    jira_filer_url = f"https://{jira_org}.atlassian.net/jira/software/c/projects/RDC/issues/?jql={urllib.parse.quote(jira_filter_jql)}"
    os.system(f"open '{jira_filer_url}'")


def main():
    """
    Simple helper script to make creating a monthly report easier. Opens Github repos
    to closed PRs where you are the other and the PR was closed the previous month.

    The default assumption is you are running this script to create a monthly
    report for the previous month. So if you are running this on June 6th, it
    will help find relevant information from May 1st to May 31st.
    """

    current_month = datetime.now().month
    parser = argparse.ArgumentParser(
        prog="monthly_helper",
        description=main.__doc__,
        epilog="Enjoy the report!",
    )
    parser.add_argument(
        "-m",
        "--month",
        type=int,
        help="The month for the report.",
        default=current_month - 1,
        choices=range(1, 13),
    )
    parser.add_argument(
        "-b",
        "--day-buffer",
        type=int,
        help="Number of days to look outside of prior month.",
        default=0,
    )
    parser.add_argument(
        "-md",
        "--use-merged-date",
        action="store_true",
        help="Use the merged date instead of the created date for PR filters.",
        default=False,
    )
    parser.add_argument(
        "--include-reviewed",
        action="store_true",
        help="Also will open Github PRs filtered to show those you reviewed in the previous month.",
        default=False,
    )
    parser.add_argument(
        "--skip-jira",
        action="store_true",
        help="Don't open the Jira issues page.",
        default=False,
    )
    parser.add_argument(
        "--skip-github",
        action="store_true",
        help="Don't open the Github PR pages.",
        default=False,
    )

    args = parser.parse_args()

    target_month = datetime.now().replace(month=args.month)
    first_day_of_month = target_month.replace(day=1)
    last_day_of_month = first_day_of_month.replace(month=args.month + 1) - timedelta(
        days=1
    )

    if args.buffer:
        first_day_of_month -= timedelta(days=args.buffer)
        last_day_of_month += timedelta(days=args.buffer)

    first_day_of_month = first_day_of_month.strftime("%Y-%m-%d")
    last_day_of_month = last_day_of_month.strftime("%Y-%m-%d")

    print(f"Opening monthly report resources for {target_month.strftime('%B %Y')}...")

    if github_org and github_username and not args.skip_github:
        open_github_pr_pages(
            first_day_of_month,
            last_day_of_month,
            args.use_merged_date,
            args.include_reviewed,
        )

    if jira_org and not args.skip_jira:
        open_jira_filter(first_day_of_month, last_day_of_month)


if __name__ == "__main__":
    main()
