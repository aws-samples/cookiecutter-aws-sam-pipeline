"""
    Tests cookiecutter baking process and rendered content
"""

import subprocess
import os
import pytest


@pytest.fixture()
def codecommit(cookies):
    result = cookies.bake(
        extra_context={"project_name": "my project",
                       "source_code_repo": "CodeCommit"}
    )
    yield result


@pytest.fixture()
def github(cookies):
    result = cookies.bake(
        extra_context={"project_name": "my project",
                       "source_code_repo": "Github"}
    )
    yield result


def test_project_generation(cookies, codecommit):
    assert codecommit.exit_code == 0
    assert codecommit.exception is None

    bake_tmp_dir = os.path.dirname(codecommit._project_dir)

    assert os.path.isfile(os.path.join(
        bake_tmp_dir, "buildspec.yaml"))
    assert os.path.isfile(os.path.join(
        bake_tmp_dir, "pipeline.yaml"))
    assert os.path.isfile(os.path.join(
        bake_tmp_dir, "Pipeline-Instructions.md"))
    assert os.path.isfile(os.path.join(
        bake_tmp_dir, "pipeline-sample.png"))


def test_codecommit_pipeline_content(cookies, codecommit):

    bake_tmp_dir = os.path.dirname(codecommit._project_dir)
    pipeline = os.path.join(bake_tmp_dir, "pipeline.yaml")

    assert 0 == cloudformation_linting(template=pipeline)

    with open(pipeline) as f:
        pipeline_content = f.readlines()
        pipeline_content = "".join(pipeline_content)

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
        assert content in pipeline_content


def test_github_pipeline_content(cookies, github):
    bake_tmp_dir = os.path.dirname(github._project_dir)
    pipeline = os.path.join(bake_tmp_dir, "pipeline.yaml")

    with open(pipeline) as f:
        pipeline_content = f.readlines()
        pipeline_content = "".join(pipeline_content)

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
        "GithubTokenSecretArnSuffix",
        "GithubUser",
        "OAuthToken",
    )

    for content in contents:
        assert content in pipeline_content


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
