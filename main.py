import json
from unittest import skip
import requests
from github import Github as GitHub

from src.settings import SETTINGS
from src.secrets import SECRETS

# Secrets
gt_token = SECRETS["GITEA_TOKEN"]
gt_url = SECRETS["GITEA_URL"]
gh_url = SECRETS["GITHUB_URL"]
gh_token = SECRETS["GITHUB_TOKEN"]

# Settings
ignore_list = SETTINGS["ignore_list"]
skip_forks = SETTINGS["skip_forks"]

gh = GitHub(gh_token)

# Create a session
session = requests.Session()
session.headers.update({
    "Content-Type": "application/json",
    "Authorization": f"token {gt_token}"})

# GitHub
def gh_get_username():
    return gh.get_user().login


def gh_get_user_repos():
    return [repo.name for repo in gh.get_user().get_repos()]


def gh_get_starred():
    #repo_id = [i.id for i in gh.get_user().get_starred()]
    repo_name = [starred.name for starred in gh.get_user().get_starred()]
    # return list(zip(repo_id, repo_fn))
    return repo_name


#! Gitea
def gt_migrate(full_name):
    """ Migrate a repo from GitHub to Gitea """
    get_repo = gh.get_repo(full_name)

    data = {
        "repo_name": get_repo.name,
        "repo_id:": get_repo.id,
        "mirror": True,
        "issues": True,
        "labels": True,
        "lfs": True,
        "milestones": True,
        "pull_requests": True,
        "releases": True,
        "clone_addr": get_repo.clone_url,
        "description": get_repo.description}

    if get_repo.private:
        data["auth_username"] = get_repo.owner.login
        data["auth_password"] = gh_token
        data["private"] = True

    jsonstring = json.dumps(data)
    session.post(gt_url + "/repos/migrate", data=jsonstring)

    for topic in get_repo.get_topics():
        gt_put_repo_topics(gt_get_username(), get_repo.name, topic)
        print(f"[4/5] Added {topic} topic to {get_repo.name}")

    return True


def check_gitea():
    """ Check if Gitea is online """
    r = requests.get(f"{gt_url}/version")
    if r.status_code != 200:
        print(f"Can't reach Gitea. {r.status_code}")
        return False
    else:
        print("[1/5] Gitea is online.")
        return True


def gt_get_username():
    """ Get Gitea username """
    return session.get(f"{gt_url}/user").json()["username"]


def gt_get_user_repos():
    """ Get all repos of user from Gitea """
    payload = {"page": 1, "limit": 1000}
    response = session.get(f"{gt_url}/user/repos", params=payload).json()
    return [i["name"] for i in response]


def gt_get_repo_topics(owner, repo):
    """ Get topics of a repo from Gitea """
    payload = {"page": 1, "limit": 1000}
    return session.get(f"{gt_url}/repos/{owner}/{repo}/topics", params=payload).json()


def gt_put_repo_topics(owner, repo, topic):
    """ Add topic to a repository on Gitea """
    return session.put(f"{gt_url}/repos/{owner}/{repo}/topics/{topic}")


def main():
    """ Main function """

    if check_gitea():
        print(f"[2/5] Logged in as {gt_get_username()} on Gitea.")
        print(f"[3/5] Logged in as {gh_get_username()} on GitHub.")

        # * Check the difference between user repos on Gitea and GitHub and then get the repos from GitHub
        repo_difference = list(set(gh_get_user_repos()) - set(gt_get_user_repos()))

        repo_count = len(repo_difference)
        for user_repos in [i for i in gh.get_user().get_repos()]:
            if skip_forks and user_repos.fork:
                repo_count -= 1
            elif user_repos.name in ignore_list:
                repo_count -= 1

        while repo_count > 0:
            print(f"[4/5] {len(repo_difference)} repos from {gh_get_username()} to migrate.")
            print(f"{repo_difference}")
            # - Migrate the user repositories
            for user_repo in [repo for repo in gh.get_user().get_repos()]:
                # - Skip forks
                if skip_forks and user_repo.fork:
                    print(f"[4/5] Skipping fork {user_repo.full_name}")
                    continue
                # - Ignore the repos in the ignore list
                elif user_repo.name in ignore_list:
                    print(f"[4/5] Ignoring {user_repo.full_name}")
                    continue
                elif user_repo.name in repo_difference:
                    print(f"[4/5] Migrating {user_repo.full_name}")
                    gt_migrate(user_repo.full_name)
                    print(f"[4/5] Migrated {user_repo.full_name}")
                    repo_count -= 1
                    # - Add topics to repository
                    print(f"[4/5] Adding topics to {user_repo.full_name}")
                    print(f"[4/5] Added all topics. Moving on to next repo.")
                else:
                    print(f"[4/5] {user_repo.full_name} already migrated.")

        else:
            print(f"[4/5] No new user repos to migrate. Checking starred repos.")

            # * If there is no difference between Gitea and GitHub, then check starred repos from GitHub
            star_difference = list(set(gh_get_starred()) - set(gt_get_user_repos()))

            star_count = len(star_difference)
            for user_repos in [i for i in gh.get_user().get_starred()]:
                if skip_forks and user_repos.fork:
                    star_count -= 1
                elif user_repos.name in ignore_list:
                    star_count -= 1

            while star_count > 0:
                print(f"[5/5] {len(star_difference)} starred repos to migrate.")
                # - Migrate the starred repos
                for starred_repo in [repo for repo in gh.get_user().get_starred()]:
                    if skip_forks and starred_repo.fork:
                        print(f"[5/5] Skipping fork {starred_repo.full_name}")
                        continue
                    elif starred_repo.name in ignore_list:
                        print(f"[5/5] Ignoring {starred_repo.full_name}")
                        continue
                    elif starred_repo.name in star_difference:
                        print(f"[5/5] Migrating {starred_repo.full_name}")
                        gt_migrate(starred_repo.full_name)
                        print(f"[5/5] Migrated {starred_repo.full_name}")
                        star_count -= 1
                        # - Add topics to repository
                        print(f"[5/5] Adding topics to {starred_repo.full_name}")
                        print(f"[5/5] Added all topics. Moving on to next repo.")
                    # else:
                    #     print(f"[5/5] {starred_repo.full_name} already migrated.")
            else:
                print(f"[5/5] No new starred repos to migrate. You are all set.")

    else:
        quit


if __name__ == "__main__":
    main()
