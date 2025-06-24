from typing import Dict, Any, List
from tools.base_tool import Tool
from utils.logger import log
import random

class WebSearchTool(Tool):
    def __init__(self):
        self.sources = [
            "Academic Research Database",
            "Industry News Portal",
            "Government Statistics Site",
            "Technical Blog",
            "Nonprofit Organization Report"
        ]
    
    def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Mock web search that returns structured results
        
        Args:
            query: Search query string
            **kwargs: Additional context
            
        Returns:
            Dictionary containing search results
        """
        log(f"Executing web search for: {query}")
        
        try:
            # Mock implementation - in reality this would call an actual search API
            num_results = random.randint(3, 7)
            results = []
            
            for i in range(num_results):
                source = random.choice(self.sources)
                results.append({
                    'title': f"{query.capitalize()} - {source}",
                    'url': f"https://example.com/{query.replace(' ', '-')}-{i}",
                    'source': source,
                    'summary': self._generate_summary(query, source),
                    'relevance_score': round(random.uniform(0.5, 1.0), 2),
                    'date': f"2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
                })
            
            # Sort by relevance
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return {
                'status': 'success',
                'query': query,
                'results': results,
                'count': len(results),
                'topics': self._extract_topics(query)
            }
            
        except Exception as e:
            log(f"Web search failed: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'query': query
            }
    
    def _generate_summary(self, query: str, source: str) -> str:
        """Generate mock summary for search result"""
        summaries = [
            f"A comprehensive analysis of {query} from {source} showing recent trends.",
            f"{source}'s perspective on {query} with supporting data.",
            f"Key findings about {query} based on research from {source}.",
            f"Recent developments in {query} as reported by {source}."
        ]
        return random.choice(summaries)
    
    def _extract_topics(self, query: str) -> List[str]:
        """Extract key topics from query"""
        topics = {
            'environmental impact': ['sustainability', 'carbon footprint', 'energy consumption'],
            'market potential': ['growth', 'opportunities', 'trends', 'forecast'],
            'cryptocurrency': ['blockchain', 'mining', 'bitcoin', 'ethereum']
        }
        
        extracted = []
        for topic, keywords in topics.items():
            if topic in query.lower():
                extracted.extend(keywords)
        
        return extracted if extracted else ['general research']