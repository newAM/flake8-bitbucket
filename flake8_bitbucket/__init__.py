from flake8.formatting import base
from typing import List
from typing import Tuple
import atlassian
import copy
import git
import os
import requests
import traceback

args = None


class Bitbucket(atlassian.Bitbucket):
    """ Extends Bitbucket API to provide code insights annotations. """

    def create_code_insights_report_annotations(
        self,
        project_key: str,
        repository_slug: str,
        commit_id: str,
        report_key: str,
        annotations: List[dict],
    ):
        url = (
            "rest/insights/1.0/projects/{projectKey}/repos/{repositorySlug}/commits/"
            "{commitId}/reports/{key}/annotations"
        ).format(
            projectKey=project_key,
            repositorySlug=repository_slug,
            commitId=commit_id,
            key=report_key,
        )
        self.post(url, data={"annotations": annotations})


def bitbucket_categorize(code: str) -> Tuple[str, str]:
    """
    Categorizes a flake8 code to a bitbucket severity and type.

    Args:
        code: Violation code string.

    Returns:
        Tuple containing bitbucket bitbucket severity and bitbucket type.

        Example return value::

            ("LOW", "CODE_SMELL")
    """
    code = code.upper()
    if code.startswith(("B", "E9", "F8", "F9", "W6")):
        return ("HIGH", "BUG")
    elif code.startswith(("W1", "W6", "E722")):
        return ("HIGH", "CODE_SMELL")
    elif code.startswith(("F4", "E7", "N")):
        return ("MEDIUM", "CODE_SMELL")
    elif code.startswith(("E1", "E2", "E3", "E4", "E5", "W2", "W3", "W5")):
        return ("LOW", "CODE_SMELL")

    return ("LOW", "CODE_SMELL")


class Flake8Bitbucket(base.BaseFormatter):
    name = "flake8-bitbucket"
    version = "0.1.0"

    @staticmethod
    def add_options(parser):
        parser.add_option(
            "--bitbucket-api-token",
            type=str,
            parse_from_config=True,
            default=None,
            help=(
                "Bitbucket API token for authentication, "
                "or a path to a file containing the token. "
                "Setting this option will automatically enable "
                f"{Flake8Bitbucket.name} as the formatter."
            ),
        )
        parser.add_option(
            "--bitbucket-url",
            type=str,
            parse_from_config=True,
            default=None,
            help="Bitbucket server URL, such as http://localhost:8090.",
        )
        parser.add_option(
            "--bitbucket-project-key",
            type=str,
            parse_from_config=True,
            default=None,
            help="Bitbucket project key.",
        )
        parser.add_option(
            "--bitbucket-repository-slug",
            type=str,
            parse_from_config=True,
            default=None,
            help="Bitbucket respository slug.",
        )
        parser.add_option(
            "--bitbucket-suppress",
            action="store_true",
            parse_from_config=True,
            default=False,
            help="Exit with code 0 on bitbucket HTTP failures.",
        )
        parser.add_option(
            "--bitbucket-verify",
            type=str,
            parse_from_config=True,
            default=True,
            help="Path to SSL certificate (.pem) for HTTPS bitbucket connections.",
        )
        parser.add_option(
            "--bitbucket-delete",
            action="store_true",
            default=False,
            help="Delete the report and exit.",
        )

    @staticmethod
    def parse_options(options):
        global args
        args = copy.deepcopy(options)
        if options.bitbucket_api_token:
            options.format = Flake8Bitbucket.name

    def start(self):
        self.violations = []

    def format(self, error):
        self.violations.append(error)
        return (
            f"{error.filename}:{error.line_number}:{error.column_number}: "
            f"{error.code} {error.text}"
        )

    def _stop(self):
        num_violations = len(self.violations)

        repo = git.Repo(search_parent_directories=True)
        commit = str(repo.head.object.hexsha)
        repo_path = os.path.abspath(repo.working_tree_dir)

        # relative paths if flake8 is not run in the root of the repo
        cwd = os.path.abspath(os.getcwd())
        relative_path = cwd.replace(repo_path, "")
        relative_path = relative_path.replace(os.sep, "/")  # windows
        relative_path = relative_path.strip("/")

        # unique keys for running flake8 in different directories in the same repo
        name = self.name + "-" + relative_path.replace("/", "-")

        if os.path.isfile(args.bitbucket_api_token):
            with open(args.bitbucket_api_token, "r") as f:
                token = f.read().strip()
        else:
            token = args.bitbucket_api_token

        bitbucket = Bitbucket(url=args.bitbucket_url, verify_ssl=args.bitbucket_verify)
        bitbucket._update_header("Authorization", f"Bearer {token}")
        try:
            bitbucket.delete_code_insights_report(
                project_key=args.bitbucket_project_key,
                repository_slug=args.bitbucket_repository_slug,
                commit_id=commit,
                report_key=name,
            )
        except requests.exceptions.HTTPError as e:
            # 404 returned if report or commit does not exist
            if not e.args[0].startswith("404"):
                raise

        if args.bitbucket_delete:
            return

        bitbucket.create_code_insights_report(
            project_key=args.bitbucket_project_key,
            repository_slug=args.bitbucket_repository_slug,
            commit_id=commit,
            report_key=name,
            report_title="flake8",
            details=(
                "flake8 is a tool to check your Python code against some "
                "of the style conventions in PEP 8."
            ),
            result="FAIL" if num_violations else "PASS",
            data=[{"title": "Violations", "type": "NUMBER", "value": num_violations}],
            reporter=name,
            logoUrl=(
                "https://www.python.org/static/community_logos/"
                "python-powered-h-140x182.png"
            ),
        )

        annotations = []
        for violation in self.violations:
            path = os.path.normpath(os.path.join(relative_path, violation.filename))
            severity, category = bitbucket_categorize(violation.code)
            annotation = {
                "line": violation.line_number,
                "message": f"{violation.code} {violation.text}",
                "path": path,
                "severity": severity,
                "type": category,
            }
            if annotation not in annotations:
                annotations.append(annotation)

        num_annotations = len(annotations)
        annotations = list(annotations)
        max_annotations = 1000
        if num_annotations > max_annotations:
            print(
                f"WARNING: bitbucket only supports {max_annotations} "
                f"annotations, found {num_annotations}"
            )
            annotations = annotations[:max_annotations]

        if num_annotations:
            bitbucket.create_code_insights_report_annotations(
                project_key=args.bitbucket_project_key,
                repository_slug=args.bitbucket_repository_slug,
                commit_id=commit,
                report_key=name,
                annotations=list(annotations),
            )

    def stop(self):
        try:
            self._stop()
        except requests.exceptions.HTTPError:
            if args.bitbucket_suppress:
                traceback.print_exc()
                print("--bitbucket-suppress is set, suppressing exception")
                return
            else:
                raise
