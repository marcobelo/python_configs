import os
import subprocess

from hamcrest import assert_that, equal_to

PROJECT_FOLDER = "project_one"


def _post_test():
    os.chdir("..")
    subprocess.run(["rm", "-rf", PROJECT_FOLDER])


def _check_inserted_files():
    subprocess.run(["git", "clone", "https://github.com/barone-dev/python_configs.git"])
    files_to_check = [
        ".coveragerc",
        ".gitignore",
        "Makefile",
        "pytest.ini",
        "requirements/base.txt",
        "requirements/dev.txt",
        "requirements/prod.txt",
        "makes/cmd.mk",
        "makes/django.mk",
        "makes/git.mk",
        "makes/prepare.mk",
    ]
    for filepath in files_to_check:
        downloaded = open(f"python_configs/{filepath}", "r").read()
        copied = open(f"{filepath}", "r").read()
        assert copied == downloaded


def test_adding_configs_to_a_new_project():
    os.mkdir(PROJECT_FOLDER)
    os.chdir(PROJECT_FOLDER)
    subprocess.run(["git", "clone", "https://github.com/barone-dev/python_configs.git"])
    subprocess.run(["chmod", "+x", "python_configs/install.sh"])
    subprocess.run(["./python_configs/install.sh"], shell=True)

    folders_files = [item for item in os.walk(".")]

    # Asserting the result structure of folders and files:
    root_folders_files = (
        ".",
        ["makes", "requirements"],
        [".coveragerc", ".gitignore", "Makefile", "pytest.ini"],
    )
    makes_folder = ("./makes", [], ["django.mk", "cmd.mk", "git.mk", "prepare.mk"])
    requirements_folder = ("./requirements", [], ["dev.txt", "base.txt", "prod.txt"])

    assert_that(folders_files[0], equal_to(root_folders_files))
    assert_that(folders_files[1], equal_to(makes_folder))
    assert_that(folders_files[2], equal_to(requirements_folder))

    # Asserting the content added to the project (this configs):
    _check_inserted_files()

    # cleaning test dirty
    _post_test()


def test_adding_configs_overwriting_the_configs_in_a_project():
    """
    This test should move all the files that will be overwriting to a backup folder on ".old/python_configs_<timestamp>".
    """
    os.mkdir(PROJECT_FOLDER)
    os.chdir(PROJECT_FOLDER)

    # Populating with some fake config files
    open(".gitignore", "w").write(".gitignore")
    open("README.md", "w").write("README.md")
    open("pytest.ini", "w").write("pytest.ini")
    open(".coveragerc", "w").write(".coveragerc")
    open("Makefile", "w").write("Makefile")
    os.mkdir("requirements")
    os.chdir("requirements")
    open("dev.txt", "w").write("dev.txt")
    open("base.txt", "w").write("base.txt")
    open("other.txt", "w").write("other.txt")
    os.chdir("..")
    os.mkdir("makes")
    os.chdir("makes")
    open("my_make.mk", "w").write("my_make.mk")
    os.chdir("..")

    # Applying python_configs to the project
    subprocess.run(["git", "clone", "https://github.com/barone-dev/python_configs.git"])
    subprocess.run(["chmod", "+x", "python_configs/install.sh"])
    subprocess.run(["./python_configs/install.sh"], shell=True)

    folders_files = [item for item in os.walk(".")]

    # Asserting the result structure of folders and files:
    root_folders_files = (
        ".",
        ["makes", ".old", "requirements"],
        [".coveragerc", "README.md", ".gitignore", "Makefile", "pytest.ini"],
    )
    makes_folder = ("./makes", [], ["django.mk", "cmd.mk", "git.mk", "prepare.mk"])
    old_folder = ("./.old", ["python_configs_1571438373"], [])
    backup_folder = (
        "./.old/python_configs_1571438373",
        ["makes", "requirements"],
        [".coveragerc", ".gitignore", "Makefile", "pytest.ini"],
    )
    backup_makes = ("./.old/python_configs_1571441912/makes", [], ["my_make.mk"])
    backup_requirements = (
        "./.old/python_configs_1571441412/requirements",
        [],
        ["other.txt", "dev.txt", "base.txt"],
    )
    requirements_folder = ("./requirements", [], ["dev.txt", "base.txt", "prod.txt"])

    assert_that(folders_files[0], equal_to(root_folders_files))
    assert_that(folders_files[1], equal_to(makes_folder))

    assert_that(folders_files[2][0], equal_to(old_folder[0]))
    assert_that(folders_files[2][1][0][:-10], equal_to(old_folder[1][0][:-10]))
    assert_that(folders_files[2][2], equal_to(old_folder[2]))

    assert_that(folders_files[3][0][:-10], equal_to(backup_folder[0][:-10]))
    assert_that(folders_files[3][1], equal_to(backup_folder[1]))
    assert_that(folders_files[3][2], equal_to(backup_folder[2]))

    assert_that(folders_files[4][0][:-16], equal_to(backup_makes[0][:-16]))
    assert_that(folders_files[4][0][-6:], equal_to(backup_makes[0][-6:]))
    assert_that(folders_files[4][1], equal_to(backup_makes[1]))
    assert_that(folders_files[4][2], equal_to(backup_makes[2]))

    assert_that(folders_files[5][0][:-23], equal_to(backup_requirements[0][:-23]))
    assert_that(folders_files[5][0][-13:], equal_to(backup_requirements[0][-13:]))
    assert_that(folders_files[5][1], equal_to(backup_requirements[1]))
    assert_that(folders_files[5][2], equal_to(backup_requirements[2]))

    assert_that(folders_files[6], equal_to(requirements_folder))

    # Asserting the content added to the project (this configs):
    _check_inserted_files()

    # Asserting the content in the backuped files:
    coverage_content = open(f"{folders_files[3][0][2:]}/.coveragerc", "r").read()
    gitignore_content = open(f"{folders_files[3][0][2:]}/.gitignore", "r").read()
    makefile_content = open(f"{folders_files[3][0][2:]}/Makefile", "r").read()
    pytest_content = open(f"{folders_files[3][0][2:]}/pytest.ini", "r").read()
    my_make_content = open(f"{folders_files[4][0][2:]}/my_make.mk", "r").read()
    base_content = open(f"{folders_files[5][0][2:]}/base.txt", "r").read()
    dev_content = open(f"{folders_files[5][0][2:]}/dev.txt", "r").read()
    other_content = open(f"{folders_files[5][0][2:]}/other.txt", "r").read()
    assert coverage_content == ".coveragerc"
    assert gitignore_content == ".gitignore"
    assert makefile_content == "Makefile"
    assert pytest_content == "pytest.ini"
    assert my_make_content == "my_make.mk"
    assert base_content == "base.txt"
    assert dev_content == "dev.txt"
    assert other_content == "other.txt"

    # cleaning test dirty
    _post_test()
