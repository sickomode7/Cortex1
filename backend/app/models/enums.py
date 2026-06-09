from enum import Enum


class GoalType(str, Enum):
    COLLEGE_COURSE = "college_course"
    INTERVIEW_PREPARATION = "interview_preparation"
    BUILD_PROJECTS = "build_projects"
    CAREER_GROWTH = "career_growth"
    HOBBY = "hobby"


class TargetLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    JOB_READY = "job_ready"


class TimeCommitment(str, Enum):
    FIFTEEN_MINUTES = "15_min_per_day"
    THIRTY_MINUTES = "30_min_per_day"
    ONE_HOUR = "1_hr_per_day"
    TWO_PLUS_HOURS = "2_plus_hr_per_day"


class LearningStyle(str, Enum):
    READING = "reading"
    EXAMPLES = "examples"
    PRACTICE = "practice"
    MIXED = "mixed"


class MotivationType(str, Enum):
    CURIOSITY = "curiosity"
    CAREER = "career"
    EXAMS = "exams"
    BUILDING_PRODUCTS = "building_products"


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionType(str, Enum):
    MCQ = "mcq"
    SHORT_ANSWER = "short_answer"
    CODE_UNDERSTANDING = "code_understanding"
    CODING_EXERCISE = "coding_exercise"


class LearningPathStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class LearningPathItemType(str, Enum):
    LEARN = "learn"
    REVIEW = "review"
    PRACTICE = "practice"
    ASSESSMENT = "assessment"


class LearningPathItemStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class LessonStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    COMPLETED = "completed"


class QuizType(str, Enum):
    ASSESSMENT = "assessment"
    PRACTICE = "practice"
    MASTERY_CHECK = "mastery_check"


class TutorConversationStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"


class TutorMessageRole(str, Enum):
    SYSTEM = "system"
    TUTOR = "tutor"
    LEARNER = "learner"

