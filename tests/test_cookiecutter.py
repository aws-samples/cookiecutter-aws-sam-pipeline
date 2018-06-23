"""
    Tests cookiecutter baking process and rendered content
"""

import subprocess


def test_project_tree(cookies):
    result = cookies.bake(
        extra_context={"project_name": "--pytest-cookies--", "source_code_repo": "1"}
    )
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == "--pytest-cookies--"
    assert result.project.isdir()
    assert result.project.join("buildspec.yaml").isfile()
    assert result.project.join("pipeline.yaml").isfile()
    assert result.project.join("Pipeline-Instructions.md").isfile()
    assert result.project.join("pipeline-sample.png").isfile()


def test_codecommit_pipeline_content(cookies):
    result = cookies.bake(
        extra_context={
            "project_name": "--pytest-cookies--",
            "source_code_repo": "CodeCommit",
        }
    )

    assert 0 == cloudformation_linting()

    pipeline = result.project.join("pipeline.yaml")
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

    assert 0 == cloudformation_linting()

    pipeline = result.project.join("pipeline.yaml")
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


def cloudformation_linting(template="pipeline.yamll"):
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
