# Monthly Report Helper

Simple helper script to make creating a monthly report easier. Opens Github repos
to closed PRs where you are the other and the PR was closed the previous month.

The default assumption is you are running this script to create a monthly report for the
previous month. So if you are running this on June 6th, it will help find relevant
information from May 1st to May 31st.

```
options:
  -h, --help            show this help message and exit
  -m {1,2,3,4,5,6,7,8,9,10,11,12}, --month {1,2,3,4,5,6,7,8,9,10,11,12}
                        The month for the report.
  -b BUFFER, --buffer BUFFER
                        Number of days to look outside of prior month.
  -md, --use-merged-date
                        Use the merged date instead of the created date for PR filters.
  --include-reviewed    Also will open Github PRs filtered to show those you reviewed in the previous month.
  --skip-jira           Don't open the Jira issues page.
  --skip-github         Don't open the Github PR pages.
```
