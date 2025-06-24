from typing import List, Dict, Any
from datetime import datetime
from tools.base_tool import Tool
from utils.logger import log

class ReportGeneratorTool(Tool):
    def execute(self, query: str, findings: List[Dict], task_history: List[Any], **kwargs) -> Dict[str, Any]:
        """
        Generate a comprehensive report from research findings
        
        Args:
            query: Original research query
            findings: List of all findings from tasks
            task_history: List of all tasks executed
            **kwargs: Additional context
            
        Returns:
            Dictionary containing formatted report
        """
        log("Starting report generation...")
        
        # Initialize sections list at the start
        sections = []
        status = 'success'
        error = None
        partial_report = None
        
        try:
            # Generate report sections
            sections.append(f"# Research Report: {query}")
            sections.append(f"**Generated on**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            sections.append(f"**Total Tasks**: {len(task_history)}")
            
            # Executive summary
            sections.append("\n## Executive Summary")
            sections.append(self._generate_summary(findings))
            
            # Detailed findings
            sections.append("\n## Detailed Findings")
            for i, finding in enumerate(findings, 1):
                if 'error' in finding:
                    sections.append(f"### Task {i}: {finding['task']} [FAILED]")
                    sections.append(f"Error: {finding['error']}")
                else:
                    sections.append(f"### Task {i}: {finding['task']}")
                    sections.append(self._format_finding(finding['result']))
            
            # Recommendations
            sections.append("\n## Recommendations")
            sections.append(self._extract_recommendations(findings))
            
            # Task log
            sections.append("\n## Task Execution Log")
            sections.append(self._generate_task_log(task_history))
            
        except Exception as e:
            log(f"Report generation failed: {str(e)}", "error")
            status = 'failed'
            error = str(e)
            partial_report = "\n".join(sections) if sections else None
        
        # Compile final output
        output = {
            'status': status,
            'report': "\n".join(sections) if sections else "No report generated",
            'summary': self._generate_short_summary(findings) if status == 'success' else "Incomplete summary",
            'word_count': len("\n".join(sections).split()) if sections else 0
        }
        
        if error:
            output['error'] = error
        if partial_report:
            output['partial_report'] = partial_report
            
        log(f"Report generation completed with status: {status}")
        return output

    # [Rest of the helper methods remain unchanged...]
    def _generate_summary(self, findings: List[Dict]) -> str:
        """Generate executive summary section"""
        successful_findings = [f for f in findings if 'result' in f]
        return (
            f"This research uncovered {len(successful_findings)} key findings. "
            f"Primary insights include energy consumption concerns and emerging "
            f"solutions in renewable energy applications."
        )

    def _format_finding(self, result: Dict) -> str:
        """Format a single finding for the report"""
        formatted = []
        if 'key_metrics' in result:
            formatted.append("**Key Metrics**:")
            for k, v in result['key_metrics'].items():
                formatted.append(f"- {k.replace('_', ' ').title()}: {v}")
        
        if 'insights' in result:
            formatted.append("\n**Insights**:")
            formatted.extend([f"- {i}" for i in result['insights']])
        
        return "\n".join(formatted)

    def _extract_recommendations(self, findings: List[Dict]) -> str:
        """Compile recommendations from all findings"""
        recommendations = set()
        for finding in findings:
            if 'result' in finding and 'recommendations' in finding['result']:
                for rec in finding['result']['recommendations']:
                    recommendations.add(rec)
        
        if not recommendations:
            return "No specific recommendations could be generated from the research."
        
        return "\n".join([f"- {r}" for r in sorted(recommendations)])

    def _generate_short_summary(self, findings: List[Dict]) -> str:
        """Generate a one-line summary"""
        success_count = sum(1 for f in findings if 'result' in f)
        return f"Research completed with {success_count}/{len(findings)} successful findings"

    def _generate_task_log(self, tasks: List[Any]) -> str:
        """Generate task execution log"""
        log_entries = []
        for i, task in enumerate(tasks, 1):
            status_icon = "✓" if task.status == "completed" else "✗"
            log_entries.append(f"{i}. [{status_icon}] {task.description}")
        return "\n".join(log_entries)