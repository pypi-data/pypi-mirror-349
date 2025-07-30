__all__ = ['Colors', 'Styles', 'AnsiCodes']


CSI = '\033['  # Control Sequence Introducer
SGR = 'm'      # Select Graphic Rendition suffix


def code_to_ansi(*codes: int) -> str:
    return f"{CSI}{';'.join(map(str, codes))}{SGR}"


class AnsiCodes:
    def __init__(self):
        for name in (name for name in dir(self) if not name.startswith('_')):
            setattr(self, name, code_to_ansi(getattr(self, name)))

    @classmethod
    def get_available_values(cls) -> tuple[str, ...]:
        return tuple(value for value in dir(cls) if not value.startswith('_'))


class AnsiColorsCodes(AnsiCodes):
    black   = 30
    red     = 31
    green   = 32
    yellow  = 33
    blue    = 34
    magenta = 35
    cyan    = 36
    white   = 37
    default = 39
    gray    = 90

    reset = 0  # reset all styles include colors/styles


class AnsiStylesCodes(AnsiCodes):
    bold        = 1
    dim         = 2
    italic      = 3
    underline   = 4
    crossed_out = 9
    default     = 22

    reset       = 0  # reset all styles include colors/styles


Colors = AnsiColorsCodes()
Styles = AnsiStylesCodes()
