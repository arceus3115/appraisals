from __future__ import annotations

from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field


class CanonicalAppraisal(BaseModel):
    """Normalized appraisal facts shared by legacy and UAD 3.6 serializers."""

    model_config = ConfigDict(str_strip_whitespace=True)

    subject_address_line: str | None = None
    subject_city_name: str | None = None
    subject_state_code: str | None = None
    subject_postal_code: str | None = None
    appraisal_effective_date: str | None = None
    opinion_of_market_value_amount: str | None = None
    extras: dict[str, str] = Field(default_factory=dict)

    @classmethod
    def from_flat(cls, values: dict[str, str | None]) -> Self:
        known = frozenset(cls.model_fields) - {"extras"}
        core: dict[str, Any] = {}
        extras: dict[str, str] = {}
        for k, v in values.items():
            if v is None or str(v).strip() == "":
                continue
            s = str(v).strip()
            if k in known:
                core[k] = s
            else:
                extras[k] = s
        return cls(extras=extras, **core)

    def to_flat(self) -> dict[str, str]:
        d = self.model_dump(exclude_none=True)
        extras = d.pop("extras", {}) or {}
        flat = {k: str(v) for k, v in d.items()}
        flat.update({k: str(v) for k, v in extras.items()})
        return flat
