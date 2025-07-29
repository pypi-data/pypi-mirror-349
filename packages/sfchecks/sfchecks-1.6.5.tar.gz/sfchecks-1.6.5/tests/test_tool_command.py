import os
from src.sfchecks.tools import command
from sys import platform


def test_run(tmp_path):
    os.chdir(tmp_path)
    if platform in ["linux", "linux2"]:
        command.run("touch   beepboop")
        command.run('touch  "aaa           aaa"')
        res = command.run("ls -l")
        assert "beepboop" in str(res.stdout)
        assert "aaa           aaa" in str(res.stdout)
        res = command.run("ls -l", capture_output=False)
        assert res.stdout is None
        assert res.stderr is None
