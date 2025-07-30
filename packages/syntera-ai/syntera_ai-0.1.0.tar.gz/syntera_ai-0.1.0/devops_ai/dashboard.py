from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.prompt import Prompt
from datetime import datetime
import os
from pathlib import Path

from .core import DevOpsAITools
from .ui.panels import (
    create_header, create_tools_panel, create_content_panel,
    create_footer, create_input_panel, create_result_table
)
from .ui.tool_handlers import ToolHandlers

class TextDashboard:
    """An enhanced text-based dashboard for SynteraAI DevOps."""
    
    def __init__(self):
        self.console = Console()
        self.devops_tools = DevOpsAITools()
        self.layout = Layout()
        self.tool_handlers = ToolHandlers(self.devops_tools, self.console)
        
        # Track the active tool for highlighting
        self.active_tool = None
        self.github_repo_url = None  # To store the GitHub repository URL
        self.local_repo_path = None  # To store the local repository path

    def _display_result(self, result: str, title: str) -> None:
        """Display the result in a more structured and visually appealing way."""
        result_group = create_result_table(result, title)
        
        # Update the content panel
        self.layout["content"].update(create_content_panel(result_group))
        
    def run(self):
        """Run the enhanced dashboard with better user experience."""
        self.console.clear()

        # Create the layout structure first
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=8),
            Layout(name="input", size=3),
            Layout(name="footer", size=2)
        )
        
        # Split the body into tools panel and content area with better proportions
        self.layout["body"].split_row(
            Layout(name="tools", ratio=1),
            Layout(name="content", ratio=3)
        )
        
        # Initial layout setup
        self.layout["header"].update(create_header())
        self.layout["tools"].update(create_tools_panel())
        self.layout["content"].update(create_content_panel())
        self.layout["input"].update(create_input_panel())
        self.layout["footer"].update(create_footer())

        # Prompt for GitHub repository URL at the start
        self.console.print("\n")
        self.github_repo_url = Prompt.ask(
            "[bold green]►[/bold green] [bold cyan]Enter the GitHub repository URL to work on[/bold cyan]",
            default="https://github.com/example/repo" # Provide a default or leave empty
        )
        
        # Clone the repository and get the local path
        clone_output, self.local_repo_path = self.tool_handlers.set_repository(self.github_repo_url)
        
        # Display clone output if any
        if clone_output:
            self._display_result(clone_output, "Git Clone Output")
        
        # Display the initial layout
        with Live(self.layout, refresh_per_second=4, auto_refresh=False) as live:
            live.refresh()
            
            while True:
                # Exit the Live context to get user input
                live.stop()
                
                # Get user input with better visibility
                self.console.print("\n")
                choice = Prompt.ask(
                    "[bold green]►[/bold green] [bold cyan]Select a tool[/bold cyan]",
                    choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "q"],
                    default="q"
                )
                
                # Resume the Live display
                live.start()
                
                if choice == "q":
                    break
                
                # Update active tool for highlighting
                self.active_tool = choice
                self.layout["tools"].update(create_tools_panel(self.active_tool))
                live.refresh()
                
                # Process based on choice with enhanced status indicators
                if choice == "1":
                    # Update input panel with specific prompt
                    self.layout["input"].update(create_input_panel("Enter log file path"))
                    live.refresh()
                    
                    # Exit Live context to get input
                    live.stop()
                    result, title = self.tool_handlers.analyze_logs()
                    live.start()
                    
                    self._display_result(result, title)
                
                elif choice == "2":
                    # Infrastructure suggestions
                    prompt = "Enter infrastructure context"
                    if self.github_repo_url:
                        prompt = f"Generating infrastructure suggestions for {self.github_repo_url}"
                    
                    self.layout["input"].update(create_input_panel(prompt))
                    live.refresh()

                    live.stop()
                    result, title = self.tool_handlers.infrastructure()
                    live.start()

                    self._display_result(result, title)
                
                elif choice == "3":
                    # Security scan
                    self.layout["input"].update(create_input_panel("Enter target to scan"))
                    live.refresh()
                    
                    live.stop()
                    result, title = self.tool_handlers.security_scan()
                    live.start()
                    
                    self._display_result(result, title)
                
                elif choice == "4":
                    # Optimization
                    self.layout["input"].update(create_input_panel("Enter optimization context"))
                    live.refresh()
                    
                    live.stop()
                    result, title = self.tool_handlers.optimize()
                    live.start()
                    
                    self._display_result(result, title)

                elif choice == "5":
                    # Git ingest
                    if not self.github_repo_url:
                        self.console.print("[bold red]GitHub repository URL not set. Please restart or set it.[/bold red]")
                        live.refresh()
                        continue

                    self.layout["input"].update(create_input_panel(f"Processing Git Ingest for {self.github_repo_url}"))
                    live.refresh()
                    
                    result, title = self.tool_handlers.git_ingest()
                    self._display_result(result, title)

                elif choice == "6":
                    # Code quality
                    if not self.github_repo_url:
                        self.console.print("[bold red]GitHub repository URL not set. Please restart or set it.[/bold red]")
                        live.refresh()
                        continue

                    self.layout["input"].update(create_input_panel(f"Analyzing code quality for {self.github_repo_url}"))
                    live.refresh()
                    
                    result, title = self.tool_handlers.code_quality()
                    self._display_result(result, title)

                elif choice == "7":
                    # Dependency check
                    if not self.github_repo_url:
                        self.console.print("[bold red]GitHub repository URL not set. Please restart or set it.[/bold red]")
                        live.refresh()
                        continue

                    self.layout["input"].update(create_input_panel(f"Checking dependencies for {self.github_repo_url}"))
                    live.refresh()
                    
                    result, title = self.tool_handlers.dependency_check()
                    self._display_result(result, title)

                elif choice == "8":
                    # Contributors
                    if not self.github_repo_url:
                        self.console.print("[bold red]GitHub repository URL not set. Please restart or set it.[/bold red]")
                        live.refresh()
                        continue

                    self.layout["input"].update(create_input_panel(f"Fetching contributors for {self.github_repo_url}"))
                    live.refresh()
                    
                    result, title = self.tool_handlers.contributors()
                    self._display_result(result, title)
                
                elif choice == "9":
                    # Docker generation
                    if not self.github_repo_url:
                        self.console.print("[bold red]GitHub repository URL not set. Please restart or set it.[/bold red]")
                        live.refresh()
                        continue

                    self.layout["input"].update(create_input_panel(f"Generating Docker files for {self.github_repo_url}"))
                    live.refresh()

                    # Avoid Progress inside Live context to prevent crash
                    live.stop()
                    result, title = self.tool_handlers.docker_generation()
                    live.start()
                    
                    self._display_result(result, title)

                # Reset input panel after any operation
                self.layout["input"].update(create_input_panel())
                live.refresh()

def main():
    """Main entry point for the dashboard."""
    dashboard = TextDashboard()
    dashboard.run()

if __name__ == "__main__":
        main()