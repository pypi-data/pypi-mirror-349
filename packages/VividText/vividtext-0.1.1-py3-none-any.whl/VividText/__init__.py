from time import sleep
from rich.console import Console

class VividText:

  def __init__(self,
               color="white",
               bold=False,
               dim=False,
               italic=False,
               underline=False,
               reverse=False,
               strike=False,
               sleep=0.05):
    self.console = Console()
    self.style_options = {
        "color": color.lower(),
        "bold": bold,
        "dim": dim,
        "italic": italic,
        "underline": underline,
        "reverse": reverse,
        "strike": strike,
    }
    self.sleep = min(sleep, 1)

  def reset_style(self, color="white", bold=False, dim=False, italic=False, underline=False, reverse=False, strike=False, sleep=0.05):
    self.style_options = {
        "color": color.lower(),
        "bold": bold,
        "dim": dim,
        "italic": italic,
        "underline": underline,
        "reverse": reverse,
        "strike": strike,
    }
    self.sleep = min(sleep, 1)

  def __build_style(self):
    style_parts = []

    # Add color (hex, named, or palette all supported)
    if self.style_options["color"]:
      style_parts.append(self.style_options["color"])

    # Add any active style flags
    for attr in ["bold", "dim", "italic", "underline", "reverse", "strike"]:
      if self.style_options[attr]:
        style_parts.append(attr)

    return " ".join(style_parts)

  def typewriter(self, msg, end='\n', input=False):
    style = self.__build_style()
    if input:
      for i, c in enumerate(msg, 1):
        self.console.print(f"[{style}]{c}[/]", end='', soft_wrap=True)
        sleep(self.sleep)
      if end:
        self.console.print(f"[{style}]{end}[/] ", end='', soft_wrap=True)
    else:
      for i, c in enumerate(msg, 1):
        self.console.print(f"[{style}]{c}[/]",
                           end=end if i == len(msg) else '',
                           soft_wrap=True)
        sleep(self.sleep)

  def menuTypewriter(self, split, *words):
    if len(words) == 1 and isinstance(words[0], list):
      worded = words[0]
    else:
      worded = list(words)

    formatted = f'{split}'.join(worded)
    self.typewriter(formatted)

  def inputTypewriter(self, msg, end=' >'):
    self.typewriter(msg, end=end, input=True)
    return input()

  def help(self):
    self.console.print(
        "\n[bold underline bright_black]Rich Color Options:[/]\n")

    self.console.print("[bold bright_yellow]Named Colors:[/]")
    self.console.print(
        "red, green, blue, yellow, magenta, cyan, white, and black. You can add bright_[color] for the same colors to make them brighter."
    )

    self.console.print("\n[bold bright_yellow]Hex Colors:[/]")
    self.console.print(
        "[#ff69b4]#ff69b4[/], [#00ffff]#00ffff[/], [#ffaa00]#ffaa00[/], any hex color will work"
    )

    self.console.print("\n[bold bright_yellow]Palette Colors:[/]")
    self.console.print(
        "Use 'color(0)' to 'color(255)'. For example: [color(201)]color(201)[/] is hot pink."
    )

    self.console.print("\n[bold bright_yellow]Attributes:[/]")
    self.console.print("bold, dim, italic, underline, reverse, strike, sleep time")

if __name__ == '__main__':
  vt = VividText(sleep=1)
  vt.reset_style(sleep=0.05)
  vt.typewriter("Hello World")