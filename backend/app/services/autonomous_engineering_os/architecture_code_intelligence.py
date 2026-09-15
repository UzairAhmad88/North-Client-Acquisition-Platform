"""Phase 64 — Architecture Registry & Code Intelligence Graph Service."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from backend.app.services.autonomous_engineering_os.base import (
    BaseAutonomousEngineeringOsService,
    AttrDict,
    ArchitectureComponentModel,
    CodeRepositoryModel,
    CodeSymbolModel,
)


class ArchitectureCodeIntelligenceService(BaseAutonomousEngineeringOsService):
    """Service managing system architecture registry, code intelligence indexing, and symbol traversal."""

    def __init__(self, db: Optional[Session] = None):
        super().__init__(db)
        self._components: Dict[str, Any] = {}
        self._repositories: Dict[str, Any] = {}
        self._symbols: Dict[str, Any] = {}

    def register_architecture_component(
        self,
        tenant_id: str,
        project_id: str,
        name: str,
        component_type: str,
        owner_team: str,
        runtime_environment: str = "KUBERNETES",
        slo_target_latency_p95_ms: float = 50.0,
        slo_target_availability_pct: float = 99.95,
        dependencies: Optional[List[str]] = None,
    ) -> Any:
        """Register system component with topology dependencies."""
        comp_id = self.generate_id("eng_arch")
        now = datetime.utcnow()
        deps = dependencies or []

        if self.db is not None and ArchitectureComponentModel is not None:
            comp = ArchitectureComponentModel(
                id=comp_id,
                tenant_id=tenant_id,
                project_id=project_id,
                name=name,
                component_type=component_type,
                owner_team=owner_team,
                runtime_environment=runtime_environment,
                slo_target_latency_p95_ms=slo_target_latency_p95_ms,
                slo_target_availability_pct=slo_target_availability_pct,
                dependencies_json=deps,
                created_at=now,
            )
            self.db.add(comp)
            self.db.commit()
            self.db.refresh(comp)
            return comp
        else:
            comp = AttrDict({
                "id": comp_id,
                "tenant_id": tenant_id,
                "project_id": project_id,
                "name": name,
                "component_type": component_type,
                "owner_team": owner_team,
                "runtime_environment": runtime_environment,
                "slo_target_latency_p95_ms": slo_target_latency_p95_ms,
                "slo_target_availability_pct": slo_target_availability_pct,
                "dependencies_json": deps,
                "created_at": now,
            })
            self._components[comp_id] = comp
            return comp

    def list_architecture_components(
        self,
        tenant_id: str,
        project_id: Optional[str] = None,
    ) -> List[Any]:
        """List architecture components for tenant and optional project."""
        if self.db is not None and ArchitectureComponentModel is not None:
            query = self.db.query(ArchitectureComponentModel).filter(
                ArchitectureComponentModel.tenant_id == tenant_id
            )
            if project_id:
                query = query.filter(ArchitectureComponentModel.project_id == project_id)
            return query.all()
        results = [c for c in self._components.values() if c.tenant_id == tenant_id]
        if project_id:
            results = [c for c in results if c.project_id == project_id]
        return results

    def get_architecture_graph(self, tenant_id: str, project_id: Optional[str] = None) -> Dict[str, Any]:
        """Return visual architecture graph with nodes, edges, and SLO metrics."""
        comps = self.list_architecture_components(tenant_id, project_id)
        nodes = []
        edges = []
        for c in comps:
            nodes.append({
                "id": c.id,
                "label": c.name,
                "type": c.component_type,
                "team": c.owner_team,
                "runtime": c.runtime_environment,
                "slo_availability": c.slo_target_availability_pct,
                "slo_latency_p95": c.slo_target_latency_p95_ms,
            })
            for dep in (c.dependencies_json or []):
                edges.append({
                    "source": c.id,
                    "target": dep,
                    "relationship": "CALLS_OR_DEPENDS_ON",
                })
        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "nodes": nodes,
            "edges": edges,
        }

    def register_code_repository(
        self,
        tenant_id: str,
        name: str,
        organization: str = "uzaii-enterprise",
        provider: str = "GITHUB",
        default_branch: str = "main",
        language: str = "Python/TypeScript",
    ) -> Any:
        """Register Git repository for code intelligence indexing."""
        repo_id = self.generate_id("eng_repo")
        now = datetime.utcnow()

        if self.db is not None and CodeRepositoryModel is not None:
            repo = CodeRepositoryModel(
                id=repo_id,
                tenant_id=tenant_id,
                name=name,
                organization=organization,
                provider=provider,
                default_branch=default_branch,
                language=language,
                indexed_files_count=0,
                indexed_symbols_count=0,
                created_at=now,
            )
            self.db.add(repo)
            self.db.commit()
            self.db.refresh(repo)
            return repo
        else:
            repo = AttrDict({
                "id": repo_id,
                "tenant_id": tenant_id,
                "name": name,
                "organization": organization,
                "provider": provider,
                "default_branch": default_branch,
                "language": language,
                "indexed_files_count": 0,
                "indexed_symbols_count": 0,
                "created_at": now,
            })
            self._repositories[repo_id] = repo
            return repo

    def list_code_repositories(self, tenant_id: str) -> List[Any]:
        """List registered code repositories."""
        if self.db is not None and CodeRepositoryModel is not None:
            return self.db.query(CodeRepositoryModel).filter(CodeRepositoryModel.tenant_id == tenant_id).all()
        return [r for r in self._repositories.values() if r.tenant_id == tenant_id]

    def index_code_symbol(
        self,
        tenant_id: str,
        repository_id: str,
        name: str,
        file_path: str,
        symbol_type: str = "FUNCTION",
        line_start: int = 1,
        line_end: int = 1,
        docstring: Optional[str] = None,
        called_by: Optional[List[str]] = None,
        calls: Optional[List[str]] = None,
    ) -> Any:
        """Index a code symbol (Function, Class, API route, Model)."""
        sym_id = self.generate_id("eng_sym")

        if self.db is not None and CodeSymbolModel is not None:
            symbol = CodeSymbolModel(
                id=sym_id,
                tenant_id=tenant_id,
                repository_id=repository_id,
                name=name,
                symbol_type=symbol_type,
                file_path=file_path,
                line_start=line_start,
                line_end=line_end,
                docstring=docstring,
                called_by_symbols=called_by or [],
                calls_symbols=calls or [],
            )
            self.db.add(symbol)
            repo = self.db.query(CodeRepositoryModel).filter(
                CodeRepositoryModel.tenant_id == tenant_id,
                CodeRepositoryModel.id == repository_id,
            ).first()
            if repo:
                repo.indexed_symbols_count = (repo.indexed_symbols_count or 0) + 1
            self.db.commit()
            self.db.refresh(symbol)
            return symbol
        else:
            symbol = AttrDict({
                "id": sym_id,
                "tenant_id": tenant_id,
                "repository_id": repository_id,
                "name": name,
                "symbol_type": symbol_type,
                "file_path": file_path,
                "line_start": line_start,
                "line_end": line_end,
                "docstring": docstring,
                "called_by_symbols": called_by or [],
                "calls_symbols": calls or [],
            })
            self._symbols[sym_id] = symbol
            if repository_id in self._repositories:
                self._repositories[repository_id].indexed_symbols_count = (
                    self._repositories[repository_id].indexed_symbols_count or 0
                ) + 1
            return symbol

    def search_code_symbols(
        self,
        tenant_id: str,
        query: str,
        symbol_type: Optional[str] = None,
        repository_id: Optional[str] = None,
    ) -> List[Any]:
        """Search indexed code symbols across repository or symbol type."""
        if self.db is not None and CodeSymbolModel is not None:
            q = self.db.query(CodeSymbolModel).filter(
                CodeSymbolModel.tenant_id == tenant_id,
                CodeSymbolModel.name.ilike(f"%{query}%"),
            )
            if symbol_type:
                q = q.filter(CodeSymbolModel.symbol_type == symbol_type)
            if repository_id:
                q = q.filter(CodeSymbolModel.repository_id == repository_id)
            return q.all()
        results = [
            s for s in self._symbols.values()
            if s.tenant_id == tenant_id and query.lower() in s.name.lower()
        ]
        if symbol_type:
            results = [s for s in results if s.symbol_type == symbol_type]
        if repository_id:
            results = [s for s in results if s.repository_id == repository_id]
        return results
