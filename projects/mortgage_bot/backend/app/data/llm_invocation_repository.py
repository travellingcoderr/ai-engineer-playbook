from sqlmodel import Session, func, select

from ..models.llm_invocation import LLMInvocation


class LLMInvocationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, payload: dict) -> LLMInvocation:
        invocation = LLMInvocation(**payload)
        self.session.add(invocation)
        self.session.commit()
        self.session.refresh(invocation)
        return invocation

    def list_recent(self, limit: int = 100) -> list[LLMInvocation]:
        statement = select(LLMInvocation).order_by(LLMInvocation.created_at.desc()).limit(limit)
        return self.session.exec(statement).all()

    def summary(self) -> dict:
        totals = self.session.exec(
            select(
                func.count(LLMInvocation.id),
                func.coalesce(func.sum(LLMInvocation.prompt_tokens), 0),
                func.coalesce(func.sum(LLMInvocation.completion_tokens), 0),
                func.coalesce(func.sum(LLMInvocation.total_tokens), 0),
                func.coalesce(func.sum(LLMInvocation.cost_usd), 0.0),
                func.coalesce(func.avg(LLMInvocation.latency_ms), 0.0),
            )
        ).one()

        feature_rows = self.session.exec(
            select(
                LLMInvocation.feature,
                func.count(LLMInvocation.id),
                func.coalesce(func.sum(LLMInvocation.total_tokens), 0),
                func.coalesce(func.sum(LLMInvocation.cost_usd), 0.0),
            )
            .group_by(LLMInvocation.feature)
            .order_by(func.count(LLMInvocation.id).desc())
        ).all()

        workflow_rows = self.session.exec(
            select(
                LLMInvocation.workflow_type,
                func.count(LLMInvocation.id),
                func.coalesce(func.sum(LLMInvocation.total_tokens), 0),
                func.coalesce(func.sum(LLMInvocation.cost_usd), 0.0),
            )
            .group_by(LLMInvocation.workflow_type)
            .order_by(func.count(LLMInvocation.id).desc())
        ).all()

        success_count = self.session.exec(
            select(func.count(LLMInvocation.id)).where(LLMInvocation.success.is_(True))
        ).one()
        total_count = totals[0] or 0

        return {
            "total_calls": total_count,
            "prompt_tokens": int(totals[1] or 0),
            "completion_tokens": int(totals[2] or 0),
            "total_tokens": int(totals[3] or 0),
            "total_cost_usd": float(totals[4] or 0.0),
            "avg_latency_ms": float(totals[5] or 0.0),
            "success_rate": (float(success_count or 0) / total_count) if total_count else 0.0,
            "by_feature": [
                {
                    "feature": row[0],
                    "calls": int(row[1] or 0),
                    "tokens": int(row[2] or 0),
                    "cost_usd": float(row[3] or 0.0),
                }
                for row in feature_rows
            ],
            "by_workflow": [
                {
                    "workflow_type": row[0],
                    "calls": int(row[1] or 0),
                    "tokens": int(row[2] or 0),
                    "cost_usd": float(row[3] or 0.0),
                }
                for row in workflow_rows
            ],
        }
