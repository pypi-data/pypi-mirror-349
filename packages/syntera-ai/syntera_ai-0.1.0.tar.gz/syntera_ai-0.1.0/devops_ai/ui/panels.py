from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich import box
from rich.align import Align
from rich.rule import Rule
from rich.markdown import Markdown
from rich.padding import Padding
from rich.console import Group
from datetime import datetime


def create_header() -> Panel:
    """Create an enhanced header panel with more information."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    header_group = Group(
        Rule("SynteraAI DevOps", style="bright_cyan"),
        Text.from_markup(f"[bold cyan]🤖 SynteraAI DevOps Dashboard[/bold cyan]"),
        Text.from_markup(f"[dim]Your AI-powered DevOps assistant | {current_time}[/dim]")
    )
    
    return Panel(
        header_group,
        border_style="bright_blue", 
        box=box.HEAVY_EDGE,
        title="[bold white on blue] DevOps AI [/bold white on blue]",
        title_align="center"
    )


def create_tools_panel(active_tool=None) -> Panel:
    """Create an enhanced tools panel with better visual indicators."""
    tools_group = Group()
    
    # Add a title with better styling
    tools_group.renderables.append(Text("Available Tools", style="bold magenta underline"))
    tools_group.renderables.append(Text(""))
    
    # Define tool options with better visual indicators and descriptions
    tools = [
        {"key": "1", "icon": "📊", "name": "Analyze Logs", "desc": "Analyze log files for patterns and errors"},
        {"key": "2", "icon": "🏗️", "name": "Infrastructure", "desc": "Get infrastructure recommendations"},
        {"key": "3", "icon": "🔒", "name": "Security Scan", "desc": "Perform security vulnerability scanning"},
        {"key": "4", "icon": "⚡", "name": "Optimize", "desc": "Get performance optimization suggestions"},
        {"key": "5", "icon": "⚙️", "name": "Git Ingest", "desc": "Ingest and process a GitHub repository"},
        {"key": "6", "icon": "🧑‍💻", "name": "Code Quality", "desc": "Analyze code quality and maintainability"},
        {"key": "7", "icon": "📦", "name": "Dependency Check", "desc": "Check for outdated or vulnerable dependencies"},
        {"key": "8", "icon": "👥", "name": "Contributors", "desc": "Show contributor statistics and activity"},
        {"key": "9", "icon": "🐳", "name": "Docker Generation", "desc": "Generate Docker and docker-compose files"}
    ]
    
    # Add each tool with proper styling and highlighting for active tool
    for tool in tools:
        tool_text = Text()
        
        # Highlight active tool
        if active_tool == tool["key"]:
            prefix = "► "
            style = "bold white on blue"
            box_style = "on blue"
        else:
            prefix = "  "
            style = "cyan"
            box_style = ""
        
        # Format tool entry
        tool_text.append(f"{prefix}{tool['key']}. {tool['icon']} ", style=style)
        tool_text.append(f"{tool['name']}\n", style=style)
        tool_text.append(f"   {tool['desc']}\n", style="dim")
        
        tools_group.renderables.append(tool_text)
    
    # Add navigation help
    tools_group.renderables.append(Text(""))
    help_text = Text()
    help_text.append("Navigation:\n", style="bold yellow")
    help_text.append("• Enter 1-9 to select tool\n", style="dim")
    help_text.append("• Press 'q' to quit", style="dim")
    tools_group.renderables.append(help_text)
    
    return Panel(
        Padding(tools_group, (1, 2)),
        title="[bold white on blue] Tools [/bold white on blue]",
        border_style="bright_blue",
        box=box.HEAVY,
        title_align="center"
    )


def create_content_panel(content: str = "") -> Panel:
    """Create an enhanced content panel with better formatting."""
    if not content:
        welcome_md = """
        # Welcome to SynteraAI DevOps Dashboard
        
        This dashboard provides AI-powered tools to help with your DevOps tasks.
        
        ## Getting Started
        1. Select a tool from the left panel
        2. Provide the required input
        3. View the AI-generated results here
        
        ## Available Tools
        - **Analyze Logs**: Find patterns and issues in your log files
        - **Infrastructure**: Get recommendations for your infrastructure
        - **Security Scan**: Identify security vulnerabilities
        - **Optimize**: Discover performance optimization opportunities
        """
        content = Markdown(welcome_md)
    
    return Panel(
        Padding(content, (1, 2)),
        title="[bold white on blue] Results [/bold white on blue]",
        border_style="bright_blue",
        box=box.HEAVY,
        title_align="center"
    )


def create_footer() -> Panel:
    """Create an enhanced footer panel with more information."""
    footer_group = Group(
        Text.from_markup("[bold green]Input Instructions:[/bold green]"),
        Text.from_markup("[white]1. Type the number (1-9) to select a tool[/white]"),
        Text.from_markup("[white]2. Press Enter to confirm your selection[/white]"),
        Text.from_markup("[white]3. Type 'q' to quit the application[/white]")
    )
    
    return Panel(
        Align.center(footer_group),
        border_style="bright_green",
        box=box.HEAVY_EDGE,
        title="[bold white on green] Help [/bold white on green]",
        title_align="center"
    )


def create_input_panel(prompt_text="Select a tool (1-9) or 'q' to quit") -> Panel:
    """Create a dedicated input panel for better visibility."""
    input_text = Text()
    input_text.append("\n")
    input_text.append("► ", style="bold green")
    input_text.append(prompt_text, style="bold cyan")
    input_text.append("\n")
    
    return Panel(
        input_text,
        title="[bold white on green] Input [/bold white on green]",
        border_style="bright_green",
        box=box.HEAVY,
        title_align="center",
        padding=(1, 2)
    )


def create_result_table(result: str, title: str) -> Group:
    """Create a formatted result table."""
    # Create a more structured table with multiple columns
    table = Table(
        title=title,
        show_header=True,
        header_style="bold magenta",
        border_style="bright_blue",
        title_style="bold cyan",
        box=box.HEAVY,
        expand=True
    )
    
    # Add columns for better organization
    table.add_column("#", style="dim", width=3)
    table.add_column("Finding", style="white", ratio=1)
    
    # Process the result into sections
    sections = result.split("\n\n")
    for i, section in enumerate(sections, 1):
        if section.strip():
            table.add_row(str(i), section)
    
    # Create a group with a header and the table
    return Group(
        Rule(title, style="bright_cyan"),
        table
    )