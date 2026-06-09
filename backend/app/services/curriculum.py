from __future__ import annotations

from datetime import datetime, UTC
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.assessment import MasteryRecord
from app.models.curriculum import Concept, ConceptPrerequisite, LearningPath, LearningPathItem
from app.models.enums import (
    LearningPathItemStatus,
    LearningPathItemType,
    LearningPathStatus,
    TargetLevel,
)
from app.schemas.curriculum import (
    CurriculumConceptSummary,
    CurriculumPlanResponse,
    LearningPathItemRead,
    LearningPathRead,
)
from app.services.onboarding import get_profile_or_404, get_user_or_404


DEFAULT_MASTERY_SCORE = 0.0


def generate_learning_path_for_user(db: Session, user_id: UUID) -> CurriculumPlanResponse:
    get_user_or_404(db, user_id)
    profile = get_profile_or_404(db, user_id)

    concepts = db.scalars(
        select(Concept)
        .where(
            Concept.domain_key == profile.domain_key,
            Concept.is_active.is_(True),
        )
        .options(
            selectinload(Concept.prerequisites).selectinload(
                ConceptPrerequisite.prerequisite_concept
            )
        )
        .order_by(Concept.concept_order.asc())
    ).all()

    if not concepts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No concepts are configured for this learner domain.",
        )

    mastery_records = db.scalars(
        select(MasteryRecord)
        .where(MasteryRecord.user_id == user_id)
        .options(selectinload(MasteryRecord.concept))
    ).all()
    mastery_by_concept_id = {
        record.concept_id: record.mastery_score
        for record in mastery_records
    }

    thresholds = _resolve_mastery_thresholds(profile.target_level)
    skip_threshold = thresholds["skip"]
    review_threshold = thresholds["review"]

    skipped_concepts: list[CurriculumConceptSummary] = []
    actionable_concepts: list[CurriculumConceptSummary] = []
    path_blueprint: list[tuple[Concept, LearningPathItemType, str]] = []

    for concept in concepts:
        mastery_score = round(mastery_by_concept_id.get(concept.id, DEFAULT_MASTERY_SCORE), 4)
        unmet_prerequisites = [
            edge.prerequisite_concept.name
            for edge in concept.prerequisites
            if mastery_by_concept_id.get(edge.prerequisite_concept_id, DEFAULT_MASTERY_SCORE)
            < review_threshold
        ]

        if mastery_score >= skip_threshold and not unmet_prerequisites:
            skipped_concepts.append(
                CurriculumConceptSummary(
                    concept_id=concept.id,
                    concept_slug=concept.slug,
                    concept_name=concept.name,
                    mastery_score=mastery_score,
                    reason=f"Mastery {mastery_score:.2f} meets skip threshold {skip_threshold:.2f}.",
                )
            )
            continue

        if mastery_score >= review_threshold:
            item_type = LearningPathItemType.REVIEW
            reason = (
                f"Mastery {mastery_score:.2f} is above review threshold {review_threshold:.2f} "
                f"but below skip threshold {skip_threshold:.2f}."
            )
        else:
            item_type = LearningPathItemType.LEARN
            if mastery_score > 0:
                reason = f"Mastery {mastery_score:.2f} is below review threshold {review_threshold:.2f}."
            else:
                reason = "No reliable mastery evidence exists for this concept yet."

        if unmet_prerequisites:
            reason = f"{reason} Weak prerequisites: {', '.join(unmet_prerequisites)}."

        actionable_concepts.append(
            CurriculumConceptSummary(
                concept_id=concept.id,
                concept_slug=concept.slug,
                concept_name=concept.name,
                mastery_score=mastery_score,
                reason=reason,
            )
        )
        path_blueprint.append((concept, item_type, reason))

    if not path_blueprint:
        concept = concepts[-1]
        fallback_reason = "All core concepts are currently mastered. Added a review checkpoint to keep momentum."
        actionable_concepts.append(
            CurriculumConceptSummary(
                concept_id=concept.id,
                concept_slug=concept.slug,
                concept_name=concept.name,
                mastery_score=round(mastery_by_concept_id.get(concept.id, DEFAULT_MASTERY_SCORE), 4),
                reason=fallback_reason,
            )
        )
        path_blueprint.append((concept, LearningPathItemType.REVIEW, fallback_reason))

    learning_path = _persist_learning_path(
        db=db,
        user_id=user_id,
        learner_profile_id=profile.id,
        domain_key=profile.domain_key,
        path_blueprint=path_blueprint,
        rationale=_build_path_rationale(
            actionable_count=len(actionable_concepts),
            skipped_count=len(skipped_concepts),
            thresholds=thresholds,
        ),
    )

    return CurriculumPlanResponse(
        user_id=user_id,
        domain_key=profile.domain_key,
        generated_at=datetime.now(UTC),
        mastery_thresholds=thresholds,
        skipped_concepts=skipped_concepts,
        actionable_concepts=actionable_concepts,
        learning_path=_serialize_learning_path(learning_path),
    )


def get_active_learning_path_for_user(db: Session, user_id: UUID) -> LearningPathRead:
    get_user_or_404(db, user_id)

    path = db.scalar(
        select(LearningPath)
        .where(
            LearningPath.user_id == user_id,
            LearningPath.is_active.is_(True),
        )
        .options(selectinload(LearningPath.items).selectinload(LearningPathItem.concept))
        .order_by(LearningPath.version.desc())
    )
    if path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active learning path exists for this learner yet.",
        )
    return _serialize_learning_path(path)


def adapt_learning_path_for_user(db: Session, user_id: UUID) -> CurriculumPlanResponse:
    """
    Module 9: Adaptive Replanning.
    Re-evaluates the Learner Profile and Mastery Records, archives the current path, 
    and generates a new version. This inserts Review nodes for concepts whose mastery dropped.
    """
    return generate_learning_path_for_user(db, user_id)


def _persist_learning_path(
    db: Session,
    user_id: UUID,
    learner_profile_id: UUID,
    domain_key: str,
    path_blueprint: list[tuple[Concept, LearningPathItemType, str]],
    rationale: str,
) -> LearningPath:
    current_active_paths = db.scalars(
        select(LearningPath).where(
            LearningPath.user_id == user_id,
            LearningPath.is_active.is_(True),
        )
    ).all()
    for path in current_active_paths:
        path.is_active = False
        path.status = LearningPathStatus.ARCHIVED

    latest_version = db.scalar(
        select(func.max(LearningPath.version)).where(LearningPath.user_id == user_id)
    ) or 0

    learning_path = LearningPath(
        user_id=user_id,
        learner_profile_id=learner_profile_id,
        domain_key=domain_key,
        status=LearningPathStatus.ACTIVE,
        version=latest_version + 1,
        is_active=True,
        rationale=rationale,
        started_at=datetime.now(UTC),
    )
    db.add(learning_path)
    db.flush()

    for position, (concept, item_type, reason) in enumerate(path_blueprint, start=1):
        item = LearningPathItem(
            learning_path_id=learning_path.id,
            concept_id=concept.id,
            position=position,
            item_type=item_type,
            status=LearningPathItemStatus.PENDING,
            unlock_condition=reason,
        )
        db.add(item)

    db.commit()
    db.refresh(learning_path)

    hydrated_path = db.scalar(
        select(LearningPath)
        .where(LearningPath.id == learning_path.id)
        .options(selectinload(LearningPath.items).selectinload(LearningPathItem.concept))
    )
    if hydrated_path is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Learning path was created but could not be reloaded.",
        )
    return hydrated_path


def _resolve_mastery_thresholds(target_level: TargetLevel) -> dict[str, float]:
    if target_level == TargetLevel.BEGINNER:
        return {"review": 0.45, "skip": 0.85}
    if target_level == TargetLevel.INTERMEDIATE:
        return {"review": 0.55, "skip": 0.9}
    if target_level == TargetLevel.ADVANCED:
        return {"review": 0.65, "skip": 0.93}
    return {"review": 0.7, "skip": 0.95}


def _build_path_rationale(actionable_count: int, skipped_count: int, thresholds: dict[str, float]) -> str:
    return (
        f"Generated deterministically from mastery thresholds "
        f"(review<{thresholds['review']:.2f}, skip>={thresholds['skip']:.2f}). "
        f"Actionable concepts: {actionable_count}. Skipped concepts: {skipped_count}."
    )


def _serialize_learning_path(path: LearningPath) -> LearningPathRead:
    sorted_items = sorted(path.items, key=lambda item: item.position)
    return LearningPathRead(
        id=path.id,
        user_id=path.user_id,
        learner_profile_id=path.learner_profile_id,
        domain_key=path.domain_key,
        status=path.status,
        version=path.version,
        is_active=path.is_active,
        rationale=path.rationale,
        started_at=path.started_at,
        completed_at=path.completed_at,
        created_at=path.created_at,
        updated_at=path.updated_at,
        items=[
            LearningPathItemRead(
                id=item.id,
                concept_id=item.concept_id,
                concept_slug=item.concept.slug,
                concept_name=item.concept.name,
                position=item.position,
                item_type=item.item_type,
                status=item.status,
                unlock_condition=item.unlock_condition,
            )
            for item in sorted_items
        ],
    )
