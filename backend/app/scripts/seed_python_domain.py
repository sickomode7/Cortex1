from __future__ import annotations

import argparse
from collections.abc import Iterable
from uuid import UUID

from sqlalchemy import select

from app.db.session import SessionLocal
from app.domain.python_programming.seed_data import (
    DOMAIN_KEY,
    PYTHON_ASSESSMENT_QUESTIONS,
    PYTHON_CONCEPTS,
)
from app.models.assessment import AssessmentQuestion
from app.models.curriculum import Concept, ConceptPrerequisite


def seed_concepts() -> dict[str, UUID]:
    session = SessionLocal()
    try:
        existing_concepts = {
            concept.slug: concept
            for concept in session.scalars(
                select(Concept).where(Concept.domain_key == DOMAIN_KEY)
            ).all()
        }

        for concept_seed in PYTHON_CONCEPTS:
            concept = existing_concepts.get(concept_seed.slug)
            if concept is None:
                concept = Concept(
                    domain_key=DOMAIN_KEY,
                    slug=concept_seed.slug,
                )
                session.add(concept)
                existing_concepts[concept_seed.slug] = concept

            concept.name = concept_seed.name
            concept.description = concept_seed.description
            concept.concept_order = concept_seed.concept_order
            concept.is_active = True

        session.flush()

        for concept_seed in PYTHON_CONCEPTS:
            concept = existing_concepts[concept_seed.slug]

            current_edges = {
                edge.prerequisite_concept.slug: edge
                for edge in concept.prerequisites
            }
            desired_slugs = set(concept_seed.prerequisites)

            for prerequisite_slug in desired_slugs - current_edges.keys():
                session.add(
                    ConceptPrerequisite(
                        concept_id=concept.id,
                        prerequisite_concept_id=existing_concepts[prerequisite_slug].id,
                    )
                )

            for prerequisite_slug, edge in current_edges.items():
                if prerequisite_slug not in desired_slugs:
                    session.delete(edge)

        concept_ids = {
            slug: concept.id
            for slug, concept in existing_concepts.items()
        }
        session.commit()
        return concept_ids
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def seed_assessment_questions(concept_ids_by_slug: dict[str, UUID]) -> tuple[int, int]:
    session = SessionLocal()
    created_count = 0
    updated_count = 0

    try:
        for question_seed in PYTHON_ASSESSMENT_QUESTIONS:
            concept_id = concept_ids_by_slug[question_seed.concept_slug]

            question = session.scalar(
                select(AssessmentQuestion).where(
                    AssessmentQuestion.concept_id == concept_id,
                    AssessmentQuestion.prompt == question_seed.prompt,
                )
            )

            if question is None:
                question = AssessmentQuestion(
                    concept_id=concept_id,
                    prompt=question_seed.prompt,
                )
                session.add(question)
                created_count += 1
            else:
                updated_count += 1

            question.difficulty = question_seed.difficulty
            question.question_type = question_seed.question_type
            question.choices = question_seed.choices
            question.expected_answer = question_seed.expected_answer
            question.starter_code = question_seed.starter_code
            question.explanation = question_seed.explanation
            question.is_active = True

        session.commit()
        return created_count, updated_count
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def build_summary_lines(concept_count: int, question_counts: tuple[int, int]) -> Iterable[str]:
    created_questions, updated_questions = question_counts
    total_prerequisites = sum(len(concept_seed.prerequisites) for concept_seed in PYTHON_CONCEPTS)

    yield f"Domain key: {DOMAIN_KEY}"
    yield f"Concepts configured: {concept_count}"
    yield f"Prerequisite edges configured: {total_prerequisites}"
    yield f"Assessment question templates configured: {len(PYTHON_ASSESSMENT_QUESTIONS)}"
    yield f"Questions created this run: {created_questions}"
    yield f"Questions updated this run: {updated_questions}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed the Python programming domain graph and starter assessment bank."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be seeded without connecting to the database.",
    )
    args = parser.parse_args()

    if args.dry_run:
        for line in build_summary_lines(len(PYTHON_CONCEPTS), (0, 0)):
            print(line)
        return

    concept_ids_by_slug = seed_concepts()
    question_counts = seed_assessment_questions(concept_ids_by_slug)

    print("Python domain seed completed.")
    for line in build_summary_lines(len(concept_ids_by_slug), question_counts):
        print(f"- {line}")


if __name__ == "__main__":
    main()
