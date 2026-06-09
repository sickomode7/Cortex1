from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment import AssessmentQuestion, MasteryRecord
from app.models.content import Quiz, QuizAttempt
from app.models.curriculum import Concept
from app.schemas.assessment import AssessmentQuestionRead
from app.schemas.quiz import QuizAttemptSubmission, QuizCreate


class QuizService:
    @staticmethod
    def generate_quiz(db: Session, user_id: UUID, req: QuizCreate) -> tuple[Quiz, list[AssessmentQuestionRead]]:
        concept = db.scalar(select(Concept).where(Concept.id == req.concept_id))
        if not concept:
            raise HTTPException(status_code=404, detail="Concept not found")

        # Fetch questions from our seeded bank
        # In a real app, we would random.sample or sort by appropriate difficulty.
        stmt = select(AssessmentQuestion).where(
            AssessmentQuestion.concept_id == req.concept_id,
            AssessmentQuestion.is_active == True,
            AssessmentQuestion.is_approved == True
        ).limit(req.question_count)
        
        questions = db.scalars(stmt).all()
        # Fallback if no approved questions
        if not questions:
            stmt = select(AssessmentQuestion).where(
                AssessmentQuestion.concept_id == req.concept_id,
                AssessmentQuestion.is_active == True
            ).limit(req.question_count)
            questions = db.scalars(stmt).all()

        if not questions:
            raise HTTPException(status_code=400, detail="No questions available for this concept")

        quiz = Quiz(
            user_id=user_id,
            concept_id=req.concept_id,
            learning_path_item_id=req.learning_path_item_id,
            title=f"Quiz: {concept.name}",
            quiz_type=req.quiz_type,
            question_count=len(questions),
            configuration={"generated_question_ids": [str(q.id) for q in questions]}
        )
        
        db.add(quiz)
        db.commit()
        db.refresh(quiz)

        q_reads = [
            AssessmentQuestionRead(
                id=q.id,
                concept_id=q.concept_id,
                concept_slug=concept.slug,
                concept_name=concept.name,
                difficulty=q.difficulty,
                question_type=q.question_type,
                prompt=q.prompt,
                choices=q.choices,
                starter_code=q.starter_code
            )
            for q in questions
        ]

        return quiz, q_reads

    @staticmethod
    def submit_quiz(db: Session, user_id: UUID, quiz_id: UUID, submission: QuizAttemptSubmission) -> QuizAttempt:
        quiz = db.scalar(select(Quiz).where(Quiz.id == quiz_id, Quiz.user_id == user_id))
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        question_ids = quiz.configuration.get("generated_question_ids", [])
        
        # Load the expected answers
        questions = db.scalars(
            select(AssessmentQuestion).where(AssessmentQuestion.id.in_(question_ids))
        ).all()
        q_map = {str(q.id): q for q in questions}

        correct_count = 0
        total = len(question_ids)
        feedback = []
        submitted_dict = {}

        for ans in submission.answers:
            qid = str(ans.question_id)
            submitted_dict[qid] = ans.answer
            
            if qid in q_map:
                expected = q_map[qid].expected_answer
                # Very simple deterministic string match logic for MVP
                is_correct = (str(expected).strip().lower() == str(ans.answer).strip().lower())
                if is_correct:
                    correct_count += 1
                
                feedback.append({
                    "question_id": qid,
                    "is_correct": is_correct,
                    "expected": expected,
                    "explanation": q_map[qid].explanation
                })

        accuracy = correct_count / total if total > 0 else 0.0

        attempt = QuizAttempt(
            quiz_id=quiz.id,
            user_id=user_id,
            score=correct_count,
            accuracy=accuracy,
            submitted_answers=submitted_dict,
            feedback_payload={"results": feedback},
            completed_at=datetime.utcnow()
        )
        db.add(attempt)
        
        # Update Mastery deterministically
        mastery_record = db.scalar(
            select(MasteryRecord).where(
                MasteryRecord.user_id == user_id, 
                MasteryRecord.concept_id == quiz.concept_id
            )
        )
        if not mastery_record:
            mastery_record = MasteryRecord(
                user_id=user_id,
                concept_id=quiz.concept_id,
                mastery_score=0.0
            )
            db.add(mastery_record)
            
        # The mathematical mastery formula
        old_score = mastery_record.mastery_score
        new_score = (old_score * 0.5) + (accuracy * 0.5)
        mastery_record.mastery_score = round(new_score, 4)
        mastery_record.quiz_accuracy = accuracy
        mastery_record.last_evaluated_at = datetime.utcnow()

        db.commit()
        db.refresh(attempt)
        
        # Module 9: Adaptive Replanning Trigger
        # If the student struggled on this quiz, immediately recalculate their learning path
        # so review nodes are injected before they can proceed.
        if accuracy < 0.6:
            from app.services.curriculum import adapt_learning_path_for_user
            adapt_learning_path_for_user(db, user_id)
        
        return attempt
