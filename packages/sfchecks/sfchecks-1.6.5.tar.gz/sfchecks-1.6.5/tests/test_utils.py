from src.sfchecks.utils import check_for, run_checks, check, on_exit


def test_run_checks_exception_returns_broken_functionality():
    def exception_raising_func():
        1 / 0
        return True

    @check
    def main_check():
        result = run_checks([check_for("test", exception_raising_func)])
        return result

    assert main_check() == "broken-functionality"


def test_running_checks():
    def test_check():
        return True

    @check
    def main_check():
        result = run_checks([check_for("test", test_check)])
        return result

    result = main_check()
    assert result == "test"


def test_on_exit(capfd):
    def print_stuff():
        print("stuff")

    @check
    @on_exit(print_stuff)
    def func():
        return "test"

    func()

    out, err = capfd.readouterr()
    assert "stuff" in err
