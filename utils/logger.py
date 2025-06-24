from rich.console import Console
from rich.theme import Theme
from datetime import datetime

custom_theme = Theme({
    "info": "bold blue",
    "warning": "bold yellow",
    "error": "bold red",
    "success": "bold green",
    "tool": "bold cyan",
    "agent": "bold magenta"
})

console = Console(theme=custom_theme)

def log(message: str, level: str = "info") -> None:
    """
    Enhanced logging with colored output and timestamps
    
    Args:
        message: Message to log
        level: Log level (info, warning, error, success, tool, agent)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    
    if level == "info":
        console.print(log_message, style="info")
    elif level == "warning":
        console.print(log_message, style="warning")
    elif level == "error":
        console.print(log_message, style="error")
    elif level == "success":
        console.print(log_message, style="success")
    elif level == "tool":
        console.print(f"[TOOL] {log_message}", style="tool")
    elif level == "agent":
        console.print(f"[AGENT] {log_message}", style="agent")
    else:
        console.print(log_message)

def log_task(task: str, status: str = "started") -> None:
    """Specialized logging for tasks"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_map = {
        "started": ("▶", "blue"),
        "completed": ("✓", "green"),
        "failed": ("✗", "red"),
        "retry": ("↻", "yellow")
    }
    icon, color = status_map.get(status, ("•", "white"))
    console.print(f"[{timestamp}] {icon} [{color}]{task}[/{color}] - {status.upper()}")