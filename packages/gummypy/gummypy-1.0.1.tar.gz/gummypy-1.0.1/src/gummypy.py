"""
A simple library that contains wrapper to interact with gum CLI tool.
"""

# Thank you https://github.com/maysara-elshewehy for making this good code divider.

# ╔══════════════════════════════════════ imports ══════════════════════════════════════╗
import os
from typing import Callable
from typing import Any
# ╚══════════════════════════════════════ imports ══════════════════════════════════════╝

# ╔══════════════════════════════════════ type aliases ══════════════════════════════════════╗

# Comment out the type alias because it is supported on python 3.12
# all supported types of an option in `gum`
# type SupportedOptionTypes = str | int | bool
# all supported types of a parameter in `gum`
# type SupportedParameterTypes = str | list[str] | None

# ╚══════════════════════════════════════ type aliases ══════════════════════════════════════╝


# ╔══════════════════════════════════════ Classes ══════════════════════════════════════╗
class GumCommandBuilder:
    """
    `GumCommandBuilder` is an abstraction on how to invoke `gum` from python.
    """

    def __init__(
        self,
        subcommand: str,
        allowed_opts: dict[str, type],
    ) -> None:
        """
        Initialize `GumCommandBuilder`.

        Args:
            `subcommand`: which subcommand of gum the user wants to invoke
            `allowed_opts`: all possible options for that subcommand
        """

        self.subcommand: str = subcommand
        self.possible_opts: dict[str, type] = allowed_opts
        self.args: list[tuple[str, str]] = []

    def add_args(self, optname: str, value: str | int | bool):
        """
        A method to add user-defined **kwargs into GumCommandBuilder's arguments list
        """
        # Checks if `optname` is a valid option in accordance to `self.possible_opts` in `self.subcommand`.
        if optname not in self.possible_opts:
            raise KeyError("[ERROR]: invalid option")

        # Checks if the type of some value of an `optname` is in accordance to the value of `self.possible_opts[optname]` which is a type.
        if not isinstance(value, self.possible_opts[optname]):
            raise ValueError("[ERROR]: invalid value")

        stringified_value: str = GumCommandBuilder.stringify_opt_value(value)

        self.args.append((optname, stringified_value))

    def execute(self, param: str | list[str] | None = None, stringify=True) -> int:
        """

        A method to execute all a gum command needs (options and parameter)

        Args:
            `param`: the parameter for a given subcommand
        """
        # The command to execute in a process
        to_execute: str = "gum " + self.subcommand + " "

        # Appends all options in `self.args` in a long option format with a value associated with it (--<flag-name>=<flag-value>)
        for optname, value in self.args:
            # TODO: convert the snake-cased option name into an option that `gum` can parse.
            if GumCommandBuilder.is_long_dot_option(optname):
                first_dash = optname.find("_")
                second_dash = optname.find("_", first_dash + 1)

                before_second_dash = optname[:second_dash]
                before_second_dash = before_second_dash.replace("_", "-")
                after_second_dash = optname[second_dash + 1 :]

                to_execute += f"--{before_second_dash}.{after_second_dash}={value}"

            elif GumCommandBuilder.is_short_dot_option(optname):
                dot_opt: str = optname.replace("_", ".")
                to_execute += f"--{dot_opt}={value} "

            else:
                # If its not a short or a long option it implies that the option is just a normal long option.
                dash_opt: str = optname.replace("_", "-")
                to_execute += f"--{dash_opt}={value} "

        # Checks if `param` is present and has the expected value
        if isinstance(param, str):
            if stringify:
                to_execute += GumCommandBuilder.stringify_opt_value(param)
            else:
                to_execute += param
        elif isinstance(param, list) and all(isinstance(item, str) for item in param):
            for pr in param:
                if stringify:
                    to_execute += GumCommandBuilder.stringify_opt_value(pr) + " "
                else:
                    to_execute += pr + " "

        # Executes the command without getting the output
        return os.system(to_execute)

    def execute_with_ret(self, param: str | list[str] | None = None) -> str:
        """
        A method to execute all a gum command needs (options and parameter) and returns its output

        Args:
            `param`: the parameter for a given subcommand
        """

        # The command to execute in a process
        to_execute: str = "gum " + self.subcommand + " "

        # Appends all options in `self.args` in a long option format with a value associated with it (--<flag-name>=<flag-value>)
        for optname, value in self.args:
            # TODO: convert the snake-cased option name into an option that `gum` can parse.
            if GumCommandBuilder.is_long_dot_option(optname):
                first_dash = optname.find("_")
                second_dash = optname.find("_", first_dash + 1)

                before_second_dash = optname[:second_dash]
                before_second_dash = before_second_dash.replace("_", "-")
                after_second_dash = optname[second_dash + 1 :]

                to_execute += f"--{before_second_dash}.{after_second_dash}={value}"

            elif GumCommandBuilder.is_short_dot_option(optname):
                dot_opt: str = optname.replace("_", ".")
                to_execute += f"--{dot_opt}={value} "

            else:
                # If its not a short or a long option it implies that the option is just a normal long option.
                dash_opt: str = optname.replace("_", "-")
                to_execute += f"--{dash_opt}={value} "

        # checks if `param` is present and has the expected value
        if isinstance(param, str):
            to_execute += param
        elif isinstance(param, list) and all(isinstance(item, str) for item in param):
            for pr in param:
                to_execute += pr + " "

        # Executes the command and gets the output
        return os.popen(to_execute).read().strip()

    # Convenience function to convert `SupportedOptionTypes` into a `str`
    @classmethod
    def stringify_opt_value(cls, value: str | int | bool) -> str:
        # It's important to handle `bool` before handling `int` because a `bool` is just a number
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, int):
            return str(value)

    @classmethod
    def is_long_dot_option(cls, optname: str) -> bool:
        idx: int = optname.find("_")
        if idx == -1:
            return False
        beginning: str = optname[:idx]
        match beginning:
            case "cursor":
                rest: str = optname[idx + 1 :]

                queries: list[str] = [
                    "text_foreground",
                    "text_background",
                    "line_number_foreground",
                    "line_number_background",
                    "line_foreground",
                    "line_foreground",
                ]

                for query in queries:
                    if query in rest:
                        return True
                return False
            case "file":
                rest: str = optname[idx + 1 :]
                return True if "size" in rest else False
            case "match":
                rest: str = optname[idx + 1 :]
                return True if "highlight" in rest else False
            case "selected":
                rest: str = optname[idx + 1 :]
                return True if "indicator" in rest else False
            case "unselected":
                rest: str = optname[idx + 1 :]
                return True if "prefix" in rest else False
            case _:
                return False

    @classmethod
    def is_short_dot_option(cls, optname: str) -> bool:
        idx: int = optname.find("_")
        if idx == -1:
            return False
        beginning: str = optname[:idx]
        match beginning:
            case "base":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "border":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "cell":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "cursor":
                return True if "mode" in optname else False
            case "directory":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "file":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "header":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "help":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "item":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "indicator":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "text":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "key":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "level":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "match":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "message":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "permissions":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "placeholder":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "prefix":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "prompt":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "selected":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "separator":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "spinner":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "symlink":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "time":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "title":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "unselected":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case "value":
                return (
                    True
                    if "background" in optname or "foreground" in optname
                    else False
                )
            case _:
                return False


class GumWrappers:
    """
    A Class that contains usable wrappers for each gum subcommands (except `spin`).
    """

    @classmethod
    def choose(cls, items: list[str], **choose_opts) -> list[str]:
        """
        A classmethod that wraps the functionality of `gum choose`
        """
        possible_opts: dict[str, type] = {
            "ordered": bool,
            "height": int,  # 10
            "cursor": str,  # "> "
            "no_show_help": bool,
            "show_help": bool,
            "timeout": str,  # "0s"
            "header": str,  # "Choose:"
            "cursor_prefix": str,  # "• "
            "selected_prefix": str,  # "✓ "
            "unselected_prefix": str,  # "• "
            "selected": str,  # ",..."
            "input_delimiter": str,  # "\\n"
            "output_delimiter": str,  # "\\n"
            "label_delimiter": str,  # ""
            "no_strip_ansi": bool,
            "strip_ansi": bool,
            "limit": int,
            "no_limit": bool,
            "select_if_one": bool,
            "cursor_foreground": str,  # "212"
            "cursor_background": str,  # ""
            "header_foreground": str,  # "99"
            "header_background": str,  # ""
            "item_foreground": str,  # ""
            "item_background": str,  # ""
            "selected_foreground": str,  # "212"
            "selected_background": str,  # ""
        }
        cmd = GumCommandBuilder("choose", possible_opts)

        for optname, value in choose_opts.items():
            cmd.add_args(optname, value)

        return list(cmd.execute_with_ret(items))

    @classmethod
    def confirm(cls, prompt: str, **confirm_opts) -> bool:
        """
        A classmethod that wraps the functionality of `gum confirm`
        """

        possible_opts: dict[str, type] = {
            "default": bool,
            "show_output": bool,
            "affirmative": str,
            "negative": str,
            "no_show_help": bool,
            "show_help": bool,
            "timeout": str,
            "prompt-foreground": str,  # "#7571F9"
            "prompt-background": str,  # ""
            "selected-foreground": str,  # "230"
            "selected-background": str,  # "212"
            "unselected-foreground": str,  # "254"
            "unselected-background": str,  # "235"
        }

        cmd = GumCommandBuilder("confirm", possible_opts)

        for optname, value in confirm_opts.items():
            cmd.add_args(optname, value)

        return True if cmd.execute(prompt) == 0 else False

    @classmethod
    def file(cls, path: str, **file_opts) -> str:
        """
        A classmethod that wraps the functionality of `gum file`
        """

        possible_opts: dict[str, type] = {
            "cursor": str,  # ">"
            "all": bool,
            "no_permissions": bool,
            "permissions": bool,
            "no_size": bool,
            "size": bool,
            "file": str,
            "directory": str,
            "no_show_help": bool,
            "show_help": bool,
            "timeout": str,  # "0s"
            "header": str,  # ""
            "height": int,  # 10
            "cursor_foreground": str,  # "212"
            "cursor_background": str,  # ""
            "symlink_foreground": str,  # "36"
            "symlink_background": str,  # ""
            "directory_foreground": str,  # "99"
            "directory_background": str,  # ""
            "file_foreground": str,  # ""
            "file_background": str,  # ""
            "permissions_foreground": str,  # "242"
            "permissions_background": str,  # ""
            "selected_foreground": str,  # "212"
            "selected_background": str,  # ""
            "file-size_foreground": str,  # "240"
            "file-size_background": str,  # ""
            "header_foreground": str,  # 99
            "header_background": str,  # ""
        }

        cmd = GumCommandBuilder("file", possible_opts)
        for optname, value in file_opts.items():
            cmd.add_args(optname, value)

        return cmd.execute_with_ret(path)

    @classmethod
    def filter(cls, to_filter: list[str], **filter_opts) -> list[str]:
        """
        A classmethod that wraps the functionality of `gum filter`
        """
        possible_opts: dict[str, type] = {
            # flags
            "indicator": str,
            "selected": str,
            "no_show_help": bool,
            "show_help": bool,
            "selected_prefix": str,
            "unselected_prefix": str,
            "header": str,
            "placeholder": str,
            "prompt": str,
            "width": int,
            "height": int,
            "value": str,
            "reverse": bool,
            "no_fuzzy": bool,
            "fuzzy": bool,
            "no_fuzzy_sort": bool,
            "fuzzy_sort": bool,
            "timeout": str,
            "input_delimiter": str,
            "output_delimiter": str,
            # Style flags
            "indicator_foreground": str,
            "indicator_background": str,
            "selected_indicator_foreground": str,
            "selected_indicator_background": str,
            "unselected_prefix_foreground": str,
            "unselected_prefix_background": str,
            "header_foreground": str,
            "header_background": str,
            "text_foreground": str,
            "text_background": str,
            "cursor_text_foreground": str,
            "cursor_text_background": str,
            "match_foreground": str,
            "match_background": str,
            "prompt_foreground": str,
            "prompt_background": str,
            "placeholder_foreground": str,
            "placeholder_background": str,
            # Selection
            "limit": int,
            "no_limit": bool,
            "select_if_one": bool,
            "no_strict": bool,
            "strict": bool,
        }

        cmd = GumCommandBuilder("filter", possible_opts)

        for optname, value in filter_opts.items():
            cmd.add_args(optname, value)

        return list(cmd.execute_with_ret(to_filter))

    @classmethod
    def format(cls, txt_template: str, **format_opts) -> str:
        """
        A classmethod that wraps the functionality of `gum format`
        """

        possible_opts: dict[str, type] = {
            "theme": str,  # pink
            "language": str,  # ""
            "no_strip_ansi": bool,
            "strip_ansi": bool,
            "type": str,  # "markdown"
        }

        cmd = GumCommandBuilder("format", possible_opts)

        for optname, value in format_opts.items():
            cmd.add_args(optname, value)

        return cmd.execute_with_ret(txt_template)

    @classmethod
    def input(cls, **input_opts) -> str:
        """
        A classmethod that wraps the functionality of `gum input`
        """

        possible_opts: dict[str, type] = {
            "placeholder": str,  #  "Type something_.."
            "prompt": str,  # "> "
            "cursor_mode": str,  # "blink"
            "value": str,  # ""
            "char_limit": int,  # 400
            "width": int,  # 0
            "password": bool,
            "no_show_help": bool,
            "show_help": bool,
            "header": str,  # ""
            "timeout": str,  # "0s"
            "no_strip_ansi": bool,
            "strip_ansi": bool,
            "prompt_foreground": str,  # ""
            "prompt_background": str,  # ""
            "placeholder_foreground": str,  # "240"
            "placeholder_background": str,  # ""
            "cursor_foreground": str,  # "212"
            "cursor_background": str,  # ""
            "header_foreground": str,  # "240"
            "header_background": str,  # ""
        }

        cmd = GumCommandBuilder("input", possible_opts)

        for optname, value in input_opts.items():
            cmd.add_args(optname, value)

        return cmd.execute_with_ret()

    @classmethod
    def join(cls, *args, **join_opts):
        """
        A classmethod that wraps the functionality of `gum join`
        """

        possible_opts: dict[str, type] = {
            "align": str,  # "left"
            "horizontal": bool,
            "vertical": bool,
        }

        cmd = GumCommandBuilder("join", possible_opts)
        param = ""

        for optname, value in join_opts.items():
            cmd.add_args(optname, value)

        for arg in args:
            if not isinstance(arg, str):
                raise TypeError("[ERROR]: `arg` must have a type of `str`")
            param += arg + " "

        return cmd.execute_with_ret(param)

    @classmethod
    def pager(cls, filepath: str, **pager_opts) -> int:
        """
        A classmethod that wraps the functionality of `gum pager`
        """

        possible_opts: dict[str, type] = {
            "showline_numbers": bool,
            "no_soft_wrap": bool,
            "soft_wrap": bool,
            "timeout": str,  # "0s"
            "foreground": str,  # ""
            "background": str,  # ""
            "line_number_foreground": str,  # "237"
            "line_number_background": str,  # ""
            "match_foreground": str,  # "212"
            "match_background": str,  # ""
            "match_highlight_foreground": str,  # "235"
            "match_highlight_background": str,  # "225"
            "help_foreground": str,  # "241"
            "help_background": str,
        }

        cmd = GumCommandBuilder("pager", possible_opts)

        for optname, value in pager_opts.items():
            cmd.add_args(optname, value)

        return cmd.execute(filepath)

    # TODO: implement for `spin`
    @classmethod
    def spin(cls, fnc: Callable[..., Any], **spin_opts):
        """
        A classmethod that wraps the functionality of `gum spin` (unimplemented).
        """

        possible_opts: dict[str, type] = {
            "show_output": bool,
            "show_error": bool,
            "show_stdout": bool,
            "show_stderr": bool,
            "spinner": str,  # "dot"
            "title": str,  # "Loading..."
            "align": str,  # "left"
            "timeout": str,  # "0s"
        }

    @classmethod
    def style(cls, text_to_style: str, **style_opts) -> int:
        """
        A classmethod that wraps the functionality of `gum style`
        """

        possible_opts: dict[str, type] = {
            "trim": bool,
            "no_strip_ansi": bool,
            "strip_ansi": bool,
            "foreground": str,
            "background": str,
            "border": str,
            "border_background": str,
            "border_foreground": str,
            "align": str,
            "height": int,
            "width": int,
            "margin": str,
            "padding": str,
            "bold": bool,
            "faint": bool,
            "italic": bool,
            "strikethrough": bool,
            "underline": bool,
        }

        cmd = GumCommandBuilder("style", possible_opts)

        for optname, value in style_opts.items():
            cmd.add_args(optname, value)

        return cmd.execute(text_to_style)

    @classmethod
    def table(cls, filepath: str, **table_opts) -> int:
        """
        A classmethod that wraps the functionality of `gum table`
        """

        possible_opts: dict[str, type] = {
            "separator": str,  # ","
            "columns": str,
            "widths": str,
            "height": int,  # 0
            "print": bool,
            "file": str,  # ""
            "border": str,  # "rounded"
            "no_show_help": bool,
            "show_help": bool,
            "no_hide_count": bool,
            "hide_count": bool,
            "lazy_quotes": bool,
            "fields_per_record": int,  # 0
            "return_column": int,  # 0
            "timeout": str,  # "0s"
            "border_foreground": str,  # ""
            "border_background": str,  # ""
            "cell_foreground": str,  # ""
            "cell_background": str,  # ""
            "header_foreground": str,  # ""
            "header_background": str,  # ""
            "selected_foreground": str,  # ""
            "selected_background": str,  # ""
        }

        cmd = GumCommandBuilder("style", possible_opts)

        for optname, value in table_opts.items():
            cmd.add_args(optname, value)

        return cmd.execute(filepath)

    @classmethod
    def write(cls, **write_opts) -> str:
        """
        A classmethod that wraps the functionality of `gum write`
        """

        possible_opts: dict[str, type] = {
            "width": int,  # 0
            "height": int,  # 5
            "header": str,  # ""
            "placeholder": str,  # "Write something_.."
            "prompt": str,  # "|  "
            "show_cursor_line": bool,
            "show_line_numbers": bool,
            "value": str,  # ""
            "char_limit": int,  # 0
            "max_lines": int,  # 0
            "no_show_help": bool,
            "show_help": bool,
            "cursor_mode": str,  # "blink"
            "timeout": str,  # "0s"
            "no_strip_ansi": bool,
            "strip_ansi": bool,
            "base_foreground": str,  # ""
            "base_background": str,  # ""
            "cursor_line_number_foreground": str,  # "7"
            "cursor_line_number_background": str,  # ""
            "cursor_line_foreground": str,  # ""
            "cursor_line_background": str,  # ""
            "cursor_foreground": str,  # "212"
            "cursor_background": str,  # ""
            "end_of_buffer_foreground": str,  # "0"
            "end_of_buffer_background": str,  # ""
            "line_number_foreground": str,  # "7"
            "line_number_background": str,  # ""
            "header_foreground": str,  # "240"
            "header_background": str,  # ""
            "placeholder_foreground": str,  # "240"
            "placeholder_background": str,  # ""
            "prompt_foreground": str,  # "7"
            "prompt_background": str,  # ""
        }

        cmd = GumCommandBuilder("write", possible_opts)

        for optname, value in write_opts.items():
            cmd.add_args(optname, value)

        return cmd.execute_with_ret()

    @classmethod
    def log(cls, text: str, **log_opts) -> int:
        """
        A classmethod that wraps the functionality of `gum log`
        """

        possible_opts: dict[str, type] = {
            "file": str,  # ""
            "format": bool,
            "formatter": str,  # "text"
            "level": str,  # "none"
            "prefix": str,  # ""
            "structured": bool,
            "time": str,  # ""
            "min_level": str,  # ""
            "level_foreground": str,  # ""
            "level_background": str,  # ""
            "time_foreground": str,  # ""
            "time_background": str,  # ""
            "prefix_foreground": str,  # ""
            "prefix_background": str,  # ""
            "message_foreground": str,  # ""
            "message_background": str,  # ""
            "key_foreground": str,  # ""
            "key_background": str,  # ""
            "value_foreground": str,  # ""
            "value_background": str,  # ""
            "separator_foreground": str,  # ""
            "separator_background": str,  # ""
        }

        cmd = GumCommandBuilder("log", possible_opts)

        for optname, value in log_opts.items():
            cmd.add_args(optname, value)

        return cmd.execute(text)

    @classmethod
    def version_check(cls, **vc_opts) -> int:
        """
        A classmethod that wraps the functionality of `gum version-check`
        """

        possible_opts: dict[str, type] = {
            "help": bool,
            "version": bool,
        }

        cmd = GumCommandBuilder("version-check", possible_opts)

        for optname, value in vc_opts.items():
            cmd.add_args(optname, value)

        return cmd.execute()


# ╚══════════════════════════════════════ classes ══════════════════════════════════════╝
