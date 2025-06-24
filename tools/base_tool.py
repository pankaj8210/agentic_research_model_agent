from abc import ABC, abstractmethod
from typing import Any, Dict

class Tool(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool's main functionality
        
        Returns:
            Dictionary containing tool's output and metadata
        """
        pass