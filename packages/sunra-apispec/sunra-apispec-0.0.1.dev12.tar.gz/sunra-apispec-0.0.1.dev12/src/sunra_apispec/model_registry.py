import importlib.util
import importlib.machinery
from pathlib import Path
from typing import Dict, Any, List, Optional

class ModelRegistry:
    def __init__(self):
        self.registries: Dict[str, List[Dict[str, Any]]] = {}
        self._initialize_registries()
    
    def _initialize_registries(self):
        current_dir = Path(__file__).parent
        specs_dir = current_dir / "specs"
        
        for provider_dir in specs_dir.iterdir():
            if not provider_dir.is_dir():
                continue
            
            for model_dir in provider_dir.iterdir():
                if not model_dir.is_dir():
                    continue
                
                endpoints_file = model_dir / "endpoints.py"
                if not endpoints_file.exists():
                    continue
                
                try:
                    module_name = f"specs.{provider_dir.name}.{model_dir.name}.endpoints"
                    
                    spec = importlib.util.spec_from_file_location(module_name, endpoints_file)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        if hasattr(module, "registry_items"):
                            registry_items = getattr(module, "registry_items")
                            self.registries.update(registry_items)
                                
                except Exception as e:
                    print(f"Error importing {endpoints_file}: {e}")

    def get(self, model_endpoint: str, service_provider: str) -> Optional[Dict[str, Any]]:
        registry_item = self.registries[model_endpoint]

        for item in registry_item:
            if item['service_provider'] == service_provider:
                return item
        return None
