import json
import logging
from datetime import datetime
from typing import Optional

import boto3
from apscheduler.schedulers.blocking import BlockingScheduler
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.assessment import AssessmentQuestion
from app.models.curriculum import Concept
from app.models.enums import DifficultyLevel, QuestionType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QuestionHarvester")


class GeneratedQuestion(BaseModel):
    question_type: str = Field(description="Must be 'MCQ' or 'CODING_EXERCISE'")
    prompt: str = Field(description="The question prompt or coding task description")
    choices: Optional[list[str]] = Field(default=None, description="Exactly 4 choices if MCQ. Null if CODING_EXERCISE.")
    starter_code: Optional[str] = Field(default=None, description="Boilerplate python code if CODING_EXERCISE. Null if MCQ.")
    expected_answer: str = Field(description="The correct choice letter if MCQ. The hidden python 'assert' tests if CODING_EXERCISE.")
    explanation: str = Field(description="A brief explanation of why the answer is correct")
    difficulty: str = Field(description="One of: EASY, MEDIUM, HARD")


class LLMResponse(BaseModel):
    questions: list[GeneratedQuestion]


def generate_questions_with_bedrock(concept_name: str, count: int) -> list[GeneratedQuestion]:
    """
    Calls AWS Bedrock (using Amazon Nova) to generate questions via the Converse API.
    Generates a mix of MCQs and Coding Exercises.
    """
    client = boto3.client(
        'bedrock-runtime',
        region_name=settings.aws_default_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key
    )
    model_id = "amazon.nova-micro-v1:0"
    
    prompt = f"""
    You are an expert Python tutor creating quiz questions about "{concept_name}".
    Generate exactly {count} questions — a mix of 'MCQ' and 'CODING_EXERCISE' types.

    === RULES FOR CODING_EXERCISE ===
    - 'prompt': Clearly describe what the function should DO and what it must RETURN.
    - 'starter_code': MUST be a function stub with a signature and a placeholder body.
      Example: "def add(a, b):\n    # Write your code here\n    pass"
      CRITICAL RULES for starter_code:
        * NEVER use print() in the starter_code. The function MUST use `return`.
        * The function must RETURN a value, not print it.
        * Always end with `pass` as the placeholder.
    - 'expected_answer': Python assert statements that test the RETURN VALUE of the function.
      Example: "assert add(1, 2) == 3\nassert add(-1, 1) == 0"
      CRITICAL: The asserts must test the return value, not printed output.
    - 'choices': must be null.

    === RULES FOR MCQ ===
    - 'choices': exactly 4 strings.
    - 'expected_answer': must exactly match one of the 4 choices.
    - 'starter_code': must be null.

    Return ONLY valid JSON matching this exact schema (no markdown, no extra text):
    {{
      "questions": [
        {{
          "question_type": "CODING_EXERCISE",
          "prompt": "Write a function `sum_even(numbers)` that takes a list of integers and returns the sum of all even numbers.",
          "choices": null,
          "starter_code": "def sum_even(numbers):\n    # Write your code here\n    pass",
          "expected_answer": "assert sum_even([1, 2, 3, 4]) == 6\nassert sum_even([10, 20]) == 30\nassert sum_even([1, 3, 5]) == 0",
          "explanation": "Iterate through the list, check if each number is even using modulo, and accumulate the sum.",
          "difficulty": "EASY"
        }}
      ]
    }}
    """
    
    try:
        response = client.converse(
            modelId=model_id,
            messages=[{
                "role": "user",
                "content": [{"text": prompt}]
            }],
            inferenceConfig={
                "maxTokens": 3000,
                "temperature": 0.4
            }
        )
        
        raw_text = response['output']['message']['content'][0]['text']
        raw_text = raw_text.strip().removeprefix("```json").removesuffix("```").strip()
        
        parsed_json = json.loads(raw_text)
        validated_data = LLMResponse(**parsed_json)
        return validated_data.questions
    except Exception as e:
        logger.error(f"Failed to generate questions for {concept_name}: {e}")
        return []


def harvest_questions():
    logger.info(f"Starting Question Harvester run at {datetime.now()}")
    db: Session = SessionLocal()
    
    try:
        concepts = db.scalars(select(Concept).where(Concept.is_active == True)).all()
        
        for concept in concepts:
            count = db.scalar(
                select(func.count(AssessmentQuestion.id))
                .where(AssessmentQuestion.concept_id == concept.id, AssessmentQuestion.is_approved == True)
            ) or 0
            
            if count < 50:
                logger.info(f"Concept '{concept.name}' has only {count} questions. Generating 5 more...")
                generated = generate_questions_with_bedrock(concept.name, 5)
                
                for q in generated:
                    diff_map = {
                        "EASY": DifficultyLevel.EASY,
                        "MEDIUM": DifficultyLevel.MEDIUM,
                        "HARD": DifficultyLevel.HARD
                    }
                    
                    q_type = QuestionType.MCQ if q.question_type == "MCQ" else QuestionType.CODING_EXERCISE
                    
                    db_question = AssessmentQuestion(
                        concept_id=concept.id,
                        difficulty=diff_map.get(q.difficulty.upper(), DifficultyLevel.EASY),
                        question_type=q_type,
                        prompt=q.prompt,
                        choices=q.choices,
                        starter_code=q.starter_code,
                        expected_answer=q.expected_answer,
                        explanation=q.explanation,
                        is_active=True,
                        is_approved=False
                    )
                    db.add(db_question)
                
                db.commit()
                logger.info(f"Successfully saved {len(generated)} unapproved questions for '{concept.name}'.")
                
    except Exception as e:
        logger.error(f"Harvester job failed: {e}")
        db.rollback()
    finally:
        db.close()
        logger.info("Harvester run complete.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--run-now":
        harvest_questions()
    else:
        scheduler = BlockingScheduler()
        scheduler.add_job(harvest_questions, 'cron', hour='0,12', minute=0)
        logger.info("Starting APScheduler. Waiting for next cron interval (12 AM / 12 PM)...")
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
