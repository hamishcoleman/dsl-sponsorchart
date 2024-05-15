#!/usr/bin/env python3
"""
Fetch a specific authenticated graphql endpoint and just return the result
"""

import argparse
import json
import urllib.request
import sys


def argparser():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument(
        "--token",
        help="The bearer token (github perm needed org:read)",
    )
    args.add_argument(
        "--url",
        help="The graphql endpoint",
        default="https://api.github.com/graphql",
    )
    args.add_argument(
        "--debug",
        action="store_true",
        default=False,
    )

    r = args.parse_args()

    if not r.token:
        try:
            f = open("token.txt", "r")
            r.token = f.read()
        except FileNotFoundError:
            pass

    return r


class GraphQL:
    def __init__(self, url):
        self.url = url
        self.token = None

    def set_token(self, token):
        self.token = token

    def query(self, q):
        body = json.dumps({"query": q}).encode("utf8")
        req = urllib.request.Request(self.url, data=body)
        if self.token:
            req.add_header("Authorization", f"bearer {self.token}")

        result = urllib.request.urlopen(req)
        data = result.read().decode("utf8")
        return data


# The hard-coded query we want data from
query = """
{
  organization(login: "dimsumlabs") {
    monthlyEstimatedSponsorsIncomeInCents
    estimatedNextSponsorsPayoutInCents
    sponsorsListing {
      activeGoal {
        description
        targetValue
      }
    }
  }
}
"""


def main():
    args = argparser()

    if args.debug:
        http = urllib.request.HTTPHandler(debuglevel=1)
        https = urllib.request.HTTPSHandler(debuglevel=1)
        opener = urllib.request.build_opener(http, https)
        urllib.request.install_opener(opener)

    gq = GraphQL(args.url)
    gq.set_token(args.token)

    try:
        print(gq.query(query))
    except urllib.error.HTTPError as e:
        print(e.url)
        print(e.code, e.reason)
        data = e.fp.read()
        print(data)
        sys.exit(1)


if __name__ == "__main__":
    main()
