#!/usr/bin/env python

import os
import json
from os import environ
import sys
import re
import shutil
import time
from datetime import datetime


def _shell(cmd):
    # FIXME: os.system is not recommend and behavior different in windows system
    # https://docs.python.org/2/library/os.html
    assert os.system(cmd) == 0


def generate_cov():
    _shell('coverage html')
    return 'htmlcov'


def git_commit(owner, repo, commit, user, token, dest_folder, cov_folder):
    _shell('git clone --depth=1 --branch=gh-pages https://{user}:{token}@github.com/{owner}/{repo}.git {dest}'.format(
        user=user,
        token=token,
        owner=owner,
        repo=repo,
        dest=dest_folder
    ))

    if not os.path.exists('%s/autocov/%s' % (dest_folder, commit)):
        shutil.move(cov_folder, '%s/autocov/%s' % (dest_folder, commit))

        os.chdir('gh-pages')
        _shell('git config user.name "%s"' % user)
        _shell('git config user.email "%s@autocov"' % user)
        _shell('git add autocov')
        _shell('git commit -m "auto cov {commit}"'.format(commit=commit))

        for i in range(3):
            try:
                _shell('git pull')
                _shell('git push')
                break
            except:
                time.sleep(10)
                pass

        os.chdir('..')


def gen_cov(owner, repo, commit, user, token, dest_folder):
    cov_path = generate_cov()
    pc_cov = re.compile(r'<span class="pc_cov">([\d]+)%</span>')

    with open("%s/index.html" % cov_path) as ifile:
        cov = int(pc_cov.findall(ifile.read())[0])

    git_commit(owner, repo, commit, user, token, dest_folder, cov_path)

    return cov


def update_github_status(auth, repo, status):
    url = "https://api.github.com/repos/{}/{}/statuses/{}".format(
        repo['owner'],
        repo['repo'],
        repo['sha']
    )
    cmd = 'curl -u {}:{} -H "Content-Type: application/json" -X POST -d \'{}\' {}'.format(
        auth['user'],
        auth['token'],
        json.dumps(status),
        url
    )
    assert os.system(cmd) == 0


def auto_cov(user, token, cov_requirements=0):
    try:
        commit = environ['TRAVIS_COMMIT_RANGE'][-40:]
    except:
        commit = environ['TRAVIS_COMMIT']
    owner, repo = environ['TRAVIS_REPO_SLUG'].split('/')

    cov = gen_cov(owner, repo, commit, user, token, 'gh-pages')

    url = "http://%s.github.io/%s/autocov/%s/" % (owner, repo, commit)
    result = cov

    if result >= cov_requirements:
        state = "success"
    else:
        state = "failure"

    print state, result, cov_requirements

    status = {
        "state": state,
        "target_url": url,
        "description": "The current coverage is %s" % result,
        "context": "continuous-integration/autocov"
    }

    auth = {
        "user": user,
        "token": token
    }
    repo = {
        "repo": repo,
        "owner": owner,
        "sha": commit
    }
    update_github_status(auth, repo, status)


def docstring_summary(docstring):
    """Return summary of docstring."""
    return docstring.split('\n')[0] if docstring else ''


def create_parser():
    """Return command-line parser."""
    # Do import locally to be friendly to those who use autopep8 as a library
    # and are supporting Python 2.6.
    import argparse

    parser = argparse.ArgumentParser(description=docstring_summary(__doc__),
                                     prog='autocov')
    parser.add_argument('--user', help='the github user')
    parser.add_argument('--token', help='the github token')
    parser.add_argument(
        '--percent',
        type=int, help='the coverage percent requirement', default=0
    )
    return parser


def parse_args(arguments):
    """Parse command-line options."""
    parser = create_parser()
    args = parser.parse_args(arguments)
    return args


def main(argv=None):
    """Command-line entry."""
    if argv is None:
        argv = sys.argv

    args = parse_args(argv[1:])

    auto_cov(args.user, args.token, args.percent)

if __name__ == '__main__':
    sys.exit(main())
