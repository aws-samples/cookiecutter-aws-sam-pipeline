"""
    Tests cookiecutter baking process and rendered content
"""

import subprocess
import os


def test_project_generation_with_hooks(cookies):
    result = cookies.bake(
        extra_context={"project_name": "my project",
                       "source_code_repo": "CodeCommit"}
    )

    assert result.exit_code == 0
    assert result.exception is None

    bake_tmp_dir = os.path.dirname(result.project)

    assert os.path.isfile(os.path.join(
        bake_tmp_dir, "buildspec.yaml"))
    assert os.path.isfile(os.path.join(
        bake_tmp_dir, "pipeline.yaml"))
    assert os.path.isfile(os.path.join(
        bake_tmp_dir, "Pipeline-Instructions.md"))
    assert os.path.isfile(os.path.join(
        bake_tmp_dir, "pipeline-sample.png"))


def test_codecommit_pipeline_content(cookies):
    result = cookies.bake(
        extra_context={
            "project_name": "--pytest-cookies--",
            "source_code_repo": "CodeCommit",
        }
    )

    pipeline = result.project.join("pipeline.yaml")

    assert 0 == cloudformation_linting(template=pipeline)

    app_content = pipeline.readlines()
    app_content = "".join(app_content)

    contents = (
        "Amazon S3",
        "AWS CodeBuild",
        "AWS CloudFormation",
        "BuildArtifactsBucket",
        "BUILD_OUTPUT_BUCKET",
        "CodePipelineExecutionRole",
        "Name: SourceCodeRepo",
        "Category: Build",
        "Category: Deploy",
        "BuildArtifactAsZip",
        "SourceCodeAsZip",
        "AWS CodeCommit",
        "BranchName",
        "RepositoryName",
        "arn:aws:codecommit",
        "CodeCommitRepositoryHttpUrl",
        "CodeCommitRepositorySshUrl",
    )

    for content in contents:
        assert content in app_content


def test_github_pipeline_content(cookies):
    result = cookies.bake(
        extra_context={
            "project_name": "--pytest-cookies--",
            "source_code_repo": "Github",
        }
    )

    pipeline = result.project.join("pipeline.yaml")

    assert 0 == cloudformation_linting(template=pipeline)

    app_content = pipeline.readlines()
    app_content = "".join(app_content)

    contents = (
        "Amazon S3",
        "AWS CodeBuild",
        "AWS CloudFormation",
        "BuildArtifactsBucket",
        "BUILD_OUTPUT_BUCKET",
        "CodePipelineExecutionRole",
        "Name: SourceCodeRepo",
        "Category: Build",
        "Category: Deploy",
        "BuildArtifactAsZip",
        "SourceCodeAsZip",
        "GithubRepo",
        "GithubToken",
        "GithubUser",
        "OAuthToken",
    )

    for content in contents:
        assert content in app_content


def cloudformation_linting(template="pipeline.yaml"):
    """Cloudformation linting via cfn-lint

    Cloudformation linting to validate against the spec

    template : str, optional
        Cloudformation template file (the default is "pipeline.yaml", which is generated upon project baking)

    Returns
    -------
    Int
        Exit status code out of cfn-lint command

    Raises
    ------
    subprocess.CalledProcessError
        subprocess exception when executed command returns a non-0 exit status

    """

    cmd = "cfn-lint"
    exec_info = subprocess.check_call([cmd, template])

    return exec_info
