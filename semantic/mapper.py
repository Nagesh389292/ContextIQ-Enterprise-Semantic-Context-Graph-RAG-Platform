"""
ContextIQ — Enterprise Data Harmonization & Semantic Mapper
Harmonizes heterogeneous enterprise source records into canonical concepts mapped to OWL ontology classes.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml
from loguru import logger

MAPPINGS_DIR = Path(__file__).parent / "mappings"


class ConceptMapper:
    """Harmonizes raw key-value enterprise records against YAML field maps & OWL ontology classes."""

    def __init__(self, mappings_path: Optional[Path] = None):
        self.mappings_path = mappings_path or MAPPINGS_DIR
        self.configs: Dict[str, Dict[str, Any]] = {}
        self.load_mappings()

    def load_mappings(self) -> None:
        """Load all YAML mapping files from semantic/mappings/."""
        if not self.mappings_path.exists():
            logger.warning(f"Mappings directory not found: {self.mappings_path}")
            return

        for yaml_file in self.mappings_path.glob("*.yaml"):
            try:
                content = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
                class_name = content.get("canonical_class")
                if class_name:
                    self.configs[class_name] = content
            except Exception as exc:
                logger.error(f"Error loading mapping file {yaml_file}: {exc}")

    def harmonize_record(self, raw_record: Dict[str, Any], target_class: str) -> Dict[str, Any]:
        """
        Transform raw record with arbitrary headers (e.g. equipment_code, VEND_NUM)
        into a canonical record matching the OWL ontology schema.
        """
        config = self.configs.get(target_class)
        if not config:
            # Fallback: pass-through if no mapping exists
            return raw_record

        field_maps = config.get("field_mappings", {})
        canonical_record: Dict[str, Any] = {
            "_ontology_concept": config.get("ontology_concept"),
            "_canonical_class": target_class,
        }

        for raw_key, value in raw_record.items():
            canonical_key = field_maps.get(raw_key, raw_key)
            canonical_record[canonical_key] = value

        return canonical_record
