import os
import re
import subprocess
import sys

import httpx


def main():
    sys.exit(_main())


def _main() -> int:
    if not 2 <= len(sys.argv) <= 3:
        print('Usage: git ppr <pull request id> [pull/push]')
        return 1

    pr_id = int(sys.argv[1])
    p = subprocess.run(['git', 'remote', '-v'], check=True, stdout=subprocess.PIPE, text=True)
    m = re.search(r'github.com:([\w\-]+/.+?)\.git', p.stdout)
    assert m, 'repo and username not found in "git remote -v":' + repr(p.stdout)
    repo = m.group(1)

    if username_token := os.getenv('GITHUB_USERNAME_TOKEN'):
        auth = httpx.BasicAuth(*username_token.split(':', 1))
    else:
        auth = None

    r = httpx.get(f'https://api.github.com/repos/{repo}/pulls/{pr_id}', auth=auth)
    r.raise_for_status()
    data = r.json()
    print('Pull Request: \x1b[1;36m{title} #{number}\x1b[0m\n'.format(**data))
    head = data['head']
    remote_branch_name = head['ref']
    local_branch_name = f'PPR#{pr_id}-{head["user"]["login"]}/{remote_branch_name}'
    # could use head['repo']['git_url'] here
    origin = head['repo']['ssh_url']

    try:
        if sys.argv[2].lower() == 'push' if len(sys.argv) == 3 else False:
            push(origin, remote_branch_name, local_branch_name)
        else:
            pull(origin, remote_branch_name, local_branch_name)
    except subprocess.CalledProcessError as e:
        print(f'error executing command: "{" ".join(e.cmd)}"')
        return 1
    return 0


def pull(origin: str, remote_branch_name: str, local_branch_name: str) -> None:
    p = subprocess.run(['git', 'branch'], check=True, stdout=subprocess.PIPE, text=True)
    branches = {b.strip(' *') for b in p.stdout.split('\n')}
    m = re.search(r'^\*\s+(\w+)', p.stdout, flags=re.M)
    assert m, 'unable to extract default branch from stdout'
    default_branch = m.group(1)
    if local_branch_name in branches:
        subprocess.run(['git', 'checkout', default_branch], check=True)
        subprocess.run(['git', 'branch', '-D', local_branch_name], check=True)
    subprocess.run(['git', 'fetch', origin, f'{remote_branch_name}:{local_branch_name}'], check=True)
    subprocess.run(['git', 'checkout', local_branch_name], check=True)


def push(origin: str, remote_branch_name: str, local_branch_name: str) -> None:
    subprocess.run(['git', 'push', origin, f'{local_branch_name}:{remote_branch_name}'], check=True)


if __name__ == '__main__':
    main()
