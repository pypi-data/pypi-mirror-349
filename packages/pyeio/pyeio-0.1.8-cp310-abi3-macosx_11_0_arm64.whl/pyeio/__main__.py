from typing import Annotated
import cyclopts
from pathlib import Path
from pyeio import rs


cli = cyclopts.App(
    name="io", # type:ignore
)


def count_lines(content: str) -> int:
    return content.count("\n")


def count_words(content: str) -> int:
    return len(content.split())


def count_bytes(content: str) -> int:
    return len(content.encode())


def count_characters(content: str) -> int:
    return len(content)


def longest_line_length(content: str) -> int:
    return max(len(line) for line in content.splitlines()) if content else 0


@cli.command()
def wc(
    # libxo: bool = cyclopts.Option(False, "--libxo", help="Generate output via libxo(3)"),
    # l: bool = cyclopts.Argument(False, "-l", help="Count lines"),
    l: bool,
    # w: bool = cyclopts.Option(False, "-w", help="Count words"),
    # c: bool = cyclopts.Option(False, "-c", help="Count bytes"),
    # m: bool = cyclopts.Option(False, "-m", help="Count characters"),
    # L: bool = cyclopts.Option(False, "-L", help="Find longest line"),
    files: Annotated[list[Path] | None, cyclopts.Argument()] = None,
):
    """Display line, word, byte, and character counts for files."""
    files = files or list()
    for file in files:
        result = list()
        if l:
            n_lines = rs.count_lines_in_file(file)
            result.append(str(n_lines))
        result.append(str(file) if file else "-")
        print("\t".join(result))

    # for file in files or [None]:  # Defaults to standard input if no files specified
    #     content = file.read_text() if file else cyclopts.prompt("Enter text (EOF to end)")
    #     result = []

    #     if l:
    #         result.append(f"{count_lines(content)}")
    #     if w:
    #         result.append(f"{count_words(content)}")
    #     if c:
    #         result.append(f"{count_bytes(content)}")
    #     if m:
    #         result.append(f"{count_characters(content)}")
    #     if L:
    #         result.append(f"{longest_line_length(content)}")

    #     result.append(str(file) if file else "-")
    #     print("\t".join(result))


if __name__ == "__main__":
    cli()
