"""UAD legacy (2.6-style) ↔ UAD 3.6 logical migration utilities."""

from appraisal_ai.uad.migrate import MigrationReport, migrate_xml_bytes

__all__ = ["migrate_xml_bytes", "MigrationReport"]
