from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from tools.web_search import WebSearchTool
from tools.data_analyzer import DataAnalyzerTool
from tools.report_generator import ReportGeneratorTool
from utils.logger import log
from utils.error_handler import retry

@dataclass
class Task:
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[Dict[str, Any]] = None
    required_tools: List[str] = None  # type: ignore # This is the line causing the first error

    def __post_init__(self):
        # Initialize required_tools if not provided
        if self.required_tools is None:
            self.required_tools = []

class ResearchAgent:
    def __init__(self, query: str):
        self.query = query
        self.tools = {
            'web_search': WebSearchTool(),
            'data_analyzer': DataAnalyzerTool(),
            'report_generator': ReportGeneratorTool()
        }
        self.task_history: List[Task] = []
        self.findings: List[Dict[str, Any]] = []
        self.max_retries = 3
        self.completed = False

    def decompose_query(self) -> List[Task]:
        """Break down the main query into sub-tasks with tool requirements"""
        log(f"Decomposing query: {self.query}")
        
        # This is a simplified version - in production you might use LLM for decomposition
        if "environmental impact" in self.query.lower():
            return [
                Task(
                    description="Find current statistics on environmental impact",
                    required_tools=["web_search", "data_analyzer"]
                ),
                Task(
                    description="Identify key contributing factors",
                    required_tools=["web_search", "data_analyzer"]
                ),
                Task(
                    description="Research sustainable alternatives",
                    required_tools=["web_search"]
                )
            ]
        else:  # Default decomposition pattern
            return [
                Task(
                    description=f"Background research on {self.query}",
                    required_tools=["web_search"]
                ),
                Task(
                    description=f"Analyze current trends in {self.query}",
                    required_tools=["web_search", "data_analyzer"]
                ),
                Task(
                    description=f"Recommendations regarding {self.query}",
                    required_tools=["web_search", "data_analyzer"]
                )
            ]

    @retry(max_attempts=3, delay=1)
    def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a task using the required tools"""
        task.status = "in_progress"
        log(f"Executing task: {task.description}")
        
        result: Dict[str, Any] = {}
        context: Dict[str, Any] = {}
        
        # Execute tools in sequence based on task requirements
        for tool_name in task.required_tools:
            try:
                tool = self.tools[tool_name]
                if tool_name == "web_search":
                    result = tool.execute(query=task.description, context=context)
                    context['search_results'] = result
                elif tool_name == "data_analyzer":
                    result = tool.execute(data=context.get('search_results', {}))
                    context['analysis'] = result
                else:
                    result = tool.execute(**context)
                
                log(f"Tool {tool_name} executed successfully")
            except Exception as e:
                log(f"Tool {tool_name} failed: {str(e)}")
                raise
        
        task.result = result
        task.status = "completed"
        return result

    def run(self) -> Dict[str, Any]:
        """Main method to execute the research workflow"""
        try:
            # Step 1: Break down the query
            tasks = self.decompose_query()
            self.task_history = tasks
            
            # Step 2: Execute each task
            for task in tasks:
                try:
                    task_result = self.execute_task(task)
                    self.findings.append({
                        'task': task.description,
                        'result': task_result
                    })
                except Exception as e:
                    log(f"Task failed after retries: {task.description}. Error: {str(e)}")
                    task.status = "failed"
                    self.findings.append({
                        'task': task.description,
                        'error': str(e)
                    })
            
            # Step 3: Generate final report
            report = self.tools['report_generator'].execute(
                query=self.query,
                findings=self.findings,
                task_history=self.task_history
            )
            
            self.completed = True
            return report if report else {}
            
        except Exception as e:
            log(f"Research failed: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'partial_findings': self.findings
            }

    def get_status(self) -> Dict[str, Any]:
        """Return current agent status"""
        return {
            'completed': self.completed,
            'tasks_total': len(self.task_history),
            'tasks_completed': sum(1 for t in self.task_history if t.status == "completed"),
            'tasks_failed': sum(1 for t in self.task_history if t.status == "failed")
        }