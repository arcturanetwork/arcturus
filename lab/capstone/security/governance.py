"""Executable cloud data-governance rules for the CCSP capstone."""

from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum


class Classification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


@dataclass(frozen=True)
class DataPolicy:
    classification: Classification
    retention_days: int
    allowed_regions: frozenset[str]
    encryption_required: bool = True


@dataclass
class DataAsset:
    asset_id: str
    policy: DataPolicy
    created: date
    region: str
    legal_hold: bool = False
    deleted: bool = False
    key_destroyed: bool = False


class GovernanceError(RuntimeError):
    pass


def validate_placement(asset: DataAsset) -> None:
    if asset.region not in asset.policy.allowed_regions:
        raise GovernanceError("data residency violation")


def eligible_for_deletion(asset: DataAsset, today: date) -> bool:
    expires = asset.created + timedelta(days=asset.policy.retention_days)
    return today >= expires and not asset.legal_hold and not asset.deleted


def cryptographic_erase(asset: DataAsset, today: date) -> None:
    """Model crypto-erasure; real proof needs provider key/media evidence."""
    if asset.legal_hold:
        raise GovernanceError("legal hold blocks deletion")
    if not eligible_for_deletion(asset, today):
        raise GovernanceError("retention period has not expired")
    asset.key_destroyed = True
    asset.deleted = True


RESPONSIBILITY = {
    "facility": "provider",
    "hypervisor": "provider",
    "guest_os_patch_iaas": "customer",
    "identity_configuration": "customer",
    "data_classification": "customer",
    "provider_assurance": "shared",
    "incident_coordination": "shared",
}


def accountable_party(control: str) -> str:
    try:
        return RESPONSIBILITY[control]
    except KeyError as exc:
        raise GovernanceError("control has no assigned owner") from exc

