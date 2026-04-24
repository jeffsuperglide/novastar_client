# src/novastar_client/models/meta.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class ApiVersion:
    api_version_major: str
    api_version_minor: str
    api_version_micro: str
    api_version_modifier: str
    api_version_date: str
    api_version_time: str
    api_dot_delimited_version: str

    @classmethod
    def from_api(cls, data: dict) -> "ApiVersion":
        return cls(
            api_version_major=data.get("apiVersionMajor", ""),
            api_version_minor=data.get("apiVersionMinor", ""),
            api_version_micro=data.get("apiVersionMicro", ""),
            api_version_modifier=data.get("apiVersionModifier", ""),
            api_version_date=data.get("apiVersionDate", ""),
            api_version_time=data.get("apiVersionTime", ""),
            api_dot_delimited_version=data.get("apiDotDelimitedVersion", ""),
        )


@dataclass
class AttributionAndUsage:
    provider_organization_text: str
    provider_organization_uri: str
    data_policy_uri: str
    disclaimer_text: str
    disclaimer_uri: str
    license_text: str
    license_uri: str
    usage_constraints_text: str
    usage_constraints_uri: str
    recommended_attribution_text: str

    @classmethod
    def from_api(cls, data: dict) -> "AttributionAndUsage":
        return cls(
            provider_organization_text=data.get("providerOrganizationText", ""),
            provider_organization_uri=data.get("providerOrganizationUri", ""),
            data_policy_uri=data.get("dataPolicyUri", ""),
            disclaimer_text=data.get("disclaimerText", ""),
            disclaimer_uri=data.get("disclaimerUri", ""),
            license_text=data.get("licenseText", ""),
            license_uri=data.get("licenseUri", ""),
            usage_constraints_text=data.get("usageConstraintsText", ""),
            usage_constraints_uri=data.get("usageConstraintsUri", ""),
            recommended_attribution_text=data.get("recommendedAttributionText", ""),
        )


@dataclass
class ResponseInfo:
    url_original: str
    url_original_encoded: str
    url: str
    url_encoded: str
    period_start: Optional[str]
    period_end: Optional[str]
    size: Optional[int]
    query_start: Optional[str]
    query_ms: Optional[int]
    query_target_ms: Optional[int]
    query_target_met: Optional[bool]
    is_cached: Optional[bool]
    cache_expiration_time: Optional[str]

    @classmethod
    def from_api(cls, data: dict) -> "ResponseInfo":
        return cls(
            url_original=data.get("urlOriginal", ""),
            url_original_encoded=data.get("urlOriginalEncoded", ""),
            url=data.get("url", ""),
            url_encoded=data.get("urlEncoded", ""),
            period_start=data.get("periodStart"),
            period_end=data.get("periodEnd"),
            size=data.get("size"),
            query_start=data.get("queryStart"),
            query_ms=data.get("queryMs"),
            query_target_ms=data.get("queryTargetMs"),
            query_target_met=data.get("queryTargetMet"),
            is_cached=data.get("isCached"),
            cache_expiration_time=data.get("cacheExpirationTime"),
        )
