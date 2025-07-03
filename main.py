import os
import sys
import serial.tools.list_ports
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()


def list_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]


def choose_option(label, options, default_value=None):
    console.print(f"\n[bold]{label}[/bold]")

    default_index = None
    for idx, option in enumerate(options, 1):
        prefix = f"[cyan]{idx}[/cyan])"
        if option == default_value:
            prefix += " [green](default)[/green]"
            default_index = idx
        console.print(f"  {prefix} {option}")

    prompt_label = f"Enter number (1-{len(options)})"
    if default_index:
        prompt_label += f" [default: {default_index}]"

    while True:
        choice = Prompt.ask(prompt_label, default=str(default_index or 1))
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        console.print("[red]Invalid selection. Try again.[/red]")


def main():
    console.clear()
    console.print(Panel("Serial Port Selector", style="bold green"))

    ports = list_serial_ports()
    if not ports:
        console.print("[red]No serial ports found.[/red]")
        sys.exit(1)

    baud_rates = [
        "300", "1200", "2400", "4800",
        "9600", "14400", "19200", "38400",
        "57600", "115200", "230400", "460800"
    ]

    default_port = ports[-1]  # Last port
    default_baud = "115200"

    port = choose_option("Select Serial Port", ports, default_value=default_port)
    baud = choose_option("Select Baud Rate", baud_rates, default_value=default_baud)

    console.print(
        Panel(
            f"Running: [yellow]screen {port} {baud}[/yellow]",
            style="bold green"
        )
    )

    try:
        os.system(f"screen {port} {baud}")
    except KeyboardInterrupt:
        console.print("[red]Cancelled by user.[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
