import os

import setupmeta


def test_wheel(sample_project):
    # Fake existence of a build folder, that should be in .gitignore (but isn't)
    # Presence of a new file there should not mark version as dirty
    build_folder = os.path.join(sample_project, "build")
    os.mkdir(build_folder)
    with open(os.path.join(build_folder, "report.txt"), "w") as fh:
        fh.write("This is some build report\n")

    setupmeta.run_program("pip", "wheel", "--only-binary", ":all:", "-w", "dist", ".")
    assert os.path.isfile(os.path.join(sample_project, "dist", "sample-0.1.0-py3-none-any.whl"))

    # Now let's modify one of the files
    with open(os.path.join(sample_project, "sample.py"), "w") as fh:
        fh.write("print('hello')\n")

    setupmeta.run_program("pip", "wheel", "--only-binary", ":all:", "-w", "dist", ".")
    assert os.path.isfile(os.path.join(sample_project, "dist", "sample-0.1.0.dirty-py3-none-any.whl"))