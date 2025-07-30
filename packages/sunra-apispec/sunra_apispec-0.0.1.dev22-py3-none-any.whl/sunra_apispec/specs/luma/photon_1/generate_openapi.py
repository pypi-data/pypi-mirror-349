from .endpoints import service
import json

if __name__ == "__main__":
    schema = service.get_openapi()
    print(json.dumps(schema, indent=2))
