"""Pydantic data models for Solution Design Intelligence Agent."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SolutionFeatureSchema(BaseModel):
    title: str = Field(..., description="Short feature name")
    description: str = Field(..., description="Technical & functional description")
    category: str = Field(..., description="Category code (e.g. BOOKING, AUTOMATION, DASHBOARD)")
    status: str = Field("RECOMMENDED", description="REQUIRED, RECOMMENDED, OPTIONAL, DEFERRED, OUT_OF_SCOPE")
    priority: str = Field("MEDIUM", description="CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL")
    supporting_requirement_titles: List[str] = Field(default_factory=list)


class SolutionDeliverableSchema(BaseModel):
    name: str
    description: str
    status: str = Field("PROPOSED")
    priority: str = Field("HIGH")
    supporting_feature_titles: List[str] = Field(default_factory=list)


class SolutionDependencySchema(BaseModel):
    feature_title: str
    depends_on_title: str
    dependency_type: str = Field("REQUIRES")


class SolutionIntegrationSchema(BaseModel):
    purpose: str
    provider: str
    data_flow: str
    status: str = Field("PROPOSED")


class SolutionAssumptionSchema(BaseModel):
    assumption_text: str
    status: str = Field("UNCONFIRMED", description="CONFIRMED, UNCONFIRMED, REQUIRES_CLIENT_INPUT")
    risk_level: str = Field("MEDIUM", description="LOW, MEDIUM, HIGH")


class SolutionArchitectureSchema(BaseModel):
    frontend: str = Field("Modern Responsive Web Application")
    backend: str = Field("REST API Microservice")
    database: str = Field("Relational Database")
    authentication: str = Field("Role-Based Identity & Access Control")
    deployment: str = Field("Cloud Container Platform")
    diagram_summary: str = Field("Client -> Web Frontend -> API Service -> Database -> Provider Services")


class SolutionDesignResult(BaseModel):
    overview: str
    architecture_summary: str
    complexity_tier: str = Field("MEDIUM", description="LOW, MEDIUM, HIGH, VERY_HIGH, UNKNOWN")

    features: List[SolutionFeatureSchema] = Field(default_factory=list)
    deliverables: List[SolutionDeliverableSchema] = Field(default_factory=list)
    dependencies: List[SolutionDependencySchema] = Field(default_factory=list)
    integrations: List[SolutionIntegrationSchema] = Field(default_factory=list)
    assumptions: List[SolutionAssumptionSchema] = Field(default_factory=list)
    architecture: SolutionArchitectureSchema = Field(default_factory=SolutionArchitectureSchema)
    out_of_scope: List[str] = Field(default_factory=list)
    optional_features: List[str] = Field(default_factory=list)
