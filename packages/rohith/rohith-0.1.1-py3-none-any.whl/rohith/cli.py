from prompt_toolkit.styles import Style
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import rich.box as rb
import textwrap
import requests
import webbrowser
import os
# ========== Your intro card ==========
console = Console()
text = """I am currently looking for new opportunities,
          my inbox is always open. Whether you have a
          question or just want to say hi, I will try
          my best to get back to you!"""

def show_card():
    content = textwrap.dedent(f"""\
                          [bold green]Rohit Gowda R[/bold green]

        Aspiring AI Enginner | Technical Trainer | PESU`26

             [bold white]Twitter:[/] https://twitter.com/[cyan]rohithgowdax[/]
              [bold white]GitHub:[/] https://github.com/[green]rohithgowdax[/]
            [bold white]LinkedIn:[/] https://linkedin.com/in/[dark_blue]rohithgowdax[/]
                 [bold white]Web:[/] [yellow]https://rohithgowda.me[/]
                              

                Card: [dark_red]pipx[/] [blue]run[/] rohith

          [italic]{text}[/italic]
    """)

    panel = Panel(
        content,
        expand=False,
        border_style="green",
        box=rb.ROUNDED,
        padding=(1, 4)
    )
    aligned_panel = Align.center(panel)
    console.print(aligned_panel)


# ========== Styles ==========
custom_style = Style([
    ("qmark", "ansigreen"),
    ("question", "bold white"),
    ("answer", " bold green"),
    ("pointer", "fg:#42f5ef bold"),
    ("highlighted", "fg:#42f5ef bold"),
    ("selected", "fg:#42f5ef bold"),
    ("separator", "fg:#6C6C6C"),
    ("instruction", ""),
    ("text", ""),
])

# ========== Contact Form (Formspree) ==========
def contact_form():
    name = questionary.text("Your Name:", style=custom_style).ask()
    email = questionary.text("Your Email:", style=custom_style).ask()
    message = questionary.text("Your Message:", style=custom_style).ask()

    # 🔁 Replace with your actual Formspree form ID
    form_url = "https://formspree.io/f/xvgalddv"  # Replace with your Form ID

    # Send POST request to Formspree
    try:
        response = requests.post(form_url, data={
            "name": name,
            "email": email,
            "message": message
        })
        if response.status_code == 200:
            console.print("\n[bold green]Thanks! Your message was sent successfully.[/bold green]")
        else:
            console.print(f"\n[bold red]Something went wrong![/bold red] Status: {response.status_code}")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")

# ========== Menu ==========
def menu():
    console.print("\nTip: Try [bold cyan]cmd/ctrl + click[/bold cyan] on the links above\n")
    choice = questionary.select(
        "What would you like to do?",
        choices=[
            "Contact me",
            "Download my Resume?",
            "Schedule a Meeting?",
            "Just quit.",
        ],
        style=custom_style,
        pointer="❯"
    ).ask()

    if choice == "Contact me":
        contact_form()

    elif choice == "Download my Resume?":
        console.print("\n[bold yellow]Downloading your resume...[/bold yellow]")

        url = "https://docs.google.com/document/d/1RD3D1lg4DxV6RaEjaI4dia5OPP2NcT2oaYpP3BlwfcE/export?format=pdf"
        filename = "Rohit_Gowda_Resume.pdf"

        try:
            r = requests.get(url)
            with open(filename, "wb") as f:
                f.write(r.content)
            console.print(f"\n[green]Resume downloaded as '{filename}' in: {os.getcwd()}[/green]")
        except Exception as e:
            console.print(f"\n[bold red]Failed to download resume:[/bold red] {e}")

    elif choice == "Schedule a Meeting?":
        console.print("\n[bold cyan]Opening your calendar...[/bold cyan]")
        webbrowser.open("https://calendly.com/risedroyalruler/30min")

    else:
        console.print("\n[italic]See you around![/italic] 👋\n")

# ========== Main ==========
def main():
    show_card()
    menu()

if __name__ == "__main__":
    main()
