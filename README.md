# TTOOL (Tugy Tools)

This Repository is for utils that me, Tugy, thought that will be usefull.

Author: [Tugy](https://github.com/IamTugy) | Github Repo: [tugytools](https://github.com/IamTugy/tugytools)

## Installation:
    $ pip install ttool
## Packages:
### Jira:
To use the Jira utils you need to create 2 Global variables:
`JIRA_API_TOKEN` and `JIRA_MAIL`.
Get your `JIRA_API_TOKEN` [here](https://id.atlassian.com/manage-profile/security/api-tokens).

Your `JIRA_MAIL` should store your jira mail ofc..

I suggest that you store this values in `$HOME/.bashrc` or `$HOME/.aliases` if you have one.

    $ ttool jira --help

    Usage: ttool jira [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.
    
    Commands:
      checkout  Checkout/Print your chosen jira issue with...
      setup     Set up your jira configurations.

#### The Setup Command
To setup a local config file to store your jira project and host.

    $ ttool jira setup --help

    Usage: ttool jira setup [OPTIONS]

      Set up your jira configurations.

    Options:
      --help  Show this message and exit.

#### The Checkout Command:
It really annoyed me every time to copy the key and description from the jira and create indicative branch names.
So this command let you pick a ticket of yours from the jira in the CLI, and then checkout to a branch with this syntax:
`ISSUE-123/My-issue-description`

    $ ttool jira checkout --help
    
    Usage: ttool jira checkout [OPTIONS]
    
      Checkout/Print your chosen jira issue with 'ISSUE-ID/the-issue-summery'
      format. use --print to print the branch name without checkout
    
    Options:
      --print / --no-print  [default: no-print]
      --help                Show this message and exit.
