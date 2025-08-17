from typing import Dict, List


class ContentService:
    def __init__(self, data: Dict[str, Dict]):
        self.data = data

    def get_categories(self) -> List[str]:
        return list({item["category"] for item in self.data.values()})

    def get_materials_by_category(self, category: str) -> List[Dict]:
        return [item for item in self.data.values() if item["category"] == category]
