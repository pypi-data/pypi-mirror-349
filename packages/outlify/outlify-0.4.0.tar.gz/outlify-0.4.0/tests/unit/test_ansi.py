import pytest

from outlify._ansi import Colors, Styles, AnsiCodes


@pytest.mark.unit
@pytest.mark.parametrize(
    'color,result',
    [
        (Colors.black, '\033[30m'),
        (Colors.red, '\033[31m'),
        (Colors.green, '\033[32m'),
        (Colors.yellow, '\033[33m'),
        (Colors.blue, '\033[34m'),
        (Colors.magenta, '\033[35m'),
        (Colors.cyan, '\033[36m'),
        (Colors.white, '\033[37m'),
        (Colors.default, '\033[39m'),
        (Colors.gray, '\033[90m'),
        (Colors.reset, '\033[0m'),
    ]
)
def test_colors(color: AnsiCodes, result: str):
    assert color == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'style,result',
    [
        (Styles.bold, '\033[1m'),
        (Styles.dim, '\033[2m'),
        (Styles.italic, '\033[3m'),
        (Styles.underline, '\033[4m'),
        (Styles.crossed_out, '\033[9m'),
        (Styles.default, '\033[22m'),
        (Styles.reset, '\033[0m'),
    ]
)
def test_styles(style: AnsiCodes, result: str):
    assert style == result
