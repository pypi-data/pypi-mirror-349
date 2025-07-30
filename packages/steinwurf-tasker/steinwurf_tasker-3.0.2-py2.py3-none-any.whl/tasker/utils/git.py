from . import validate
import semver
import re


class Git(object):
    def checkout(self, shell, branch):
        shell.run(f"git checkout {branch}", hide=True)

    def pull(self, shell):
        result = shell.run("git pull", hide=True)
        return "Updating" in result.stdout

    def branch(self, shell):
        """Get the current branch."""
        branch = shell.run("git rev-parse --abbrev-ref HEAD", hide=True).stdout.strip()
        if branch == "HEAD":
            return None
        else:
            return branch

    def default_branch(self, shell):
        """Get the remote head (default branch)."""
        output = shell.run(
            "git branch --remotes --list 'origin/HEAD'", hide=True
        ).stdout

        # Parse out the default branch
        # origin/HEAD -> origin/master

        parser = re.compile(
            r"""
            \s*                   # Match zero or more spaces
            origin/HEAD           # Match 'origin/HEAD'
            \s*                   # Match zero or more spaces
            ->                    # Match '->'
            \s*                   # Match zero or more spaces
            origin/               # Match 'origin/'
            (?P<default_branch>   # Group and match
            \S+                   # Match one or more non-space characters
            )                     # End group
            """,
            re.VERBOSE,
        )

        match = parser.match(output)

        if not match:
            raise RuntimeError(f"Could not parse the default branch from: {output}")

        return match.group("default_branch")

    def tags(self, shell):
        output = shell.run("git tag -l", hide=True).stdout
        if not output:
            return []

        all_tags = set(output.split("\n"))

        valid_tags = set(validate.extract_valid_tags(all_tags))
        invalid_tags = all_tags - valid_tags

        return sorted(invalid_tags) + sorted(valid_tags, key=semver.parse_version_info)
