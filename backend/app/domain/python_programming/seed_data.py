from __future__ import annotations

from dataclasses import dataclass

from app.models.enums import DifficultyLevel, QuestionType

DOMAIN_KEY = "python_programming"


@dataclass(frozen=True)
class ConceptSeed:
    slug: str
    name: str
    description: str
    concept_order: int
    prerequisites: tuple[str, ...] = ()


@dataclass(frozen=True)
class AssessmentQuestionSeed:
    concept_slug: str
    difficulty: DifficultyLevel
    question_type: QuestionType
    prompt: str
    expected_answer: str
    explanation: str
    choices: list[str] | None = None
    starter_code: str | None = None


PYTHON_CONCEPTS: tuple[ConceptSeed, ...] = (
    ConceptSeed(
        slug="variables",
        name="Variables",
        description="Store values in named references and understand reassignment in Python.",
        concept_order=1,
    ),
    ConceptSeed(
        slug="data_types",
        name="Data Types",
        description="Recognize core Python data types like strings, integers, floats, and booleans.",
        concept_order=2,
        prerequisites=("variables",),
    ),
    ConceptSeed(
        slug="operators",
        name="Operators",
        description="Use arithmetic, comparison, logical, and assignment operators to build expressions.",
        concept_order=3,
        prerequisites=("data_types",),
    ),
    ConceptSeed(
        slug="conditionals",
        name="Conditionals",
        description="Control program flow with if, elif, and else branches.",
        concept_order=4,
        prerequisites=("operators",),
    ),
    ConceptSeed(
        slug="loops",
        name="Loops",
        description="Repeat actions with for and while loops while tracking iteration state.",
        concept_order=5,
        prerequisites=("conditionals",),
    ),
    ConceptSeed(
        slug="functions",
        name="Functions",
        description="Break code into reusable units with parameters, return values, and scope.",
        concept_order=6,
        prerequisites=("loops",),
    ),
    ConceptSeed(
        slug="lists",
        name="Lists",
        description="Store ordered collections and manipulate them with indexing, slicing, and methods.",
        concept_order=7,
        prerequisites=("functions",),
    ),
    ConceptSeed(
        slug="dictionaries",
        name="Dictionaries",
        description="Work with key-value data structures for fast lookup and structured data handling.",
        concept_order=8,
        prerequisites=("lists",),
    ),
    ConceptSeed(
        slug="oop",
        name="Object-Oriented Programming",
        description="Model behavior and state with classes, objects, attributes, and methods.",
        concept_order=9,
        prerequisites=("functions", "dictionaries"),
    ),
    ConceptSeed(
        slug="file_handling",
        name="File Handling",
        description="Read from and write to files using Python file APIs and context managers.",
        concept_order=10,
        prerequisites=("functions",),
    ),
    ConceptSeed(
        slug="exception_handling",
        name="Exception Handling",
        description="Handle runtime errors gracefully with try, except, else, and finally.",
        concept_order=11,
        prerequisites=("conditionals", "functions"),
    ),
    ConceptSeed(
        slug="modules",
        name="Modules and Packages",
        description="Organize Python code across files and reuse functionality through imports.",
        concept_order=12,
        prerequisites=("functions", "file_handling"),
    ),
)


PYTHON_ASSESSMENT_QUESTIONS: tuple[AssessmentQuestionSeed, ...] = (
    AssessmentQuestionSeed(
        concept_slug="variables",
        difficulty=DifficultyLevel.EASY,
        question_type=QuestionType.MCQ,
        prompt="Which statement correctly creates a variable named `age` with the value 21 in Python?",
        choices=["var age = 21", "age := 21", "age = 21", "int age = 21"],
        expected_answer="age = 21",
        explanation="Python uses simple assignment with `=` and does not require a type keyword.",
    ),
    AssessmentQuestionSeed(
        concept_slug="data_types",
        difficulty=DifficultyLevel.EASY,
        question_type=QuestionType.MCQ,
        prompt="What is the type of the value `True` in Python?",
        choices=["int", "string", "bool", "float"],
        expected_answer="bool",
        explanation="`True` and `False` are boolean values in Python.",
    ),
    AssessmentQuestionSeed(
        concept_slug="operators",
        difficulty=DifficultyLevel.MEDIUM,
        question_type=QuestionType.SHORT_ANSWER,
        prompt="What is the result of `3 * 2 + 4` in Python?",
        expected_answer="10",
        explanation="Multiplication runs before addition, so `3 * 2` becomes `6`, then `6 + 4` becomes `10`.",
    ),
    AssessmentQuestionSeed(
        concept_slug="conditionals",
        difficulty=DifficultyLevel.MEDIUM,
        question_type=QuestionType.CODE_UNDERSTANDING,
        prompt="What will this print?\n\nx = 7\nif x > 10:\n    print('big')\nelse:\n    print('small')",
        expected_answer="small",
        explanation="Since 7 is not greater than 10, the `else` branch executes.",
    ),
    AssessmentQuestionSeed(
        concept_slug="loops",
        difficulty=DifficultyLevel.MEDIUM,
        question_type=QuestionType.CODE_UNDERSTANDING,
        prompt="How many times does this loop print `Hi`?\n\nfor i in range(3):\n    print('Hi')",
        expected_answer="3",
        explanation="`range(3)` produces three values: 0, 1, and 2.",
    ),
    AssessmentQuestionSeed(
        concept_slug="functions",
        difficulty=DifficultyLevel.MEDIUM,
        question_type=QuestionType.SHORT_ANSWER,
        prompt="What keyword is used to send a value back from a function in Python?",
        expected_answer="return",
        explanation="The `return` keyword exits the function and passes a value back to the caller.",
    ),
    AssessmentQuestionSeed(
        concept_slug="lists",
        difficulty=DifficultyLevel.MEDIUM,
        question_type=QuestionType.CODE_UNDERSTANDING,
        prompt="What is the value of `items[1]` in this code?\n\nitems = ['a', 'b', 'c']",
        expected_answer="b",
        explanation="Python list indexing starts at 0, so index 1 refers to the second element.",
    ),
    AssessmentQuestionSeed(
        concept_slug="dictionaries",
        difficulty=DifficultyLevel.MEDIUM,
        question_type=QuestionType.SHORT_ANSWER,
        prompt="Which syntax gets the value stored under the key `name` in `user = {'name': 'Ada'}`?",
        expected_answer="user['name']",
        explanation="Dictionary values are retrieved by key with square bracket notation.",
    ),
    AssessmentQuestionSeed(
        concept_slug="oop",
        difficulty=DifficultyLevel.HARD,
        question_type=QuestionType.SHORT_ANSWER,
        prompt="In object-oriented Python, what do we call a specific object created from a class?",
        expected_answer="instance",
        explanation="A class defines a blueprint; an object created from it is an instance.",
    ),
    AssessmentQuestionSeed(
        concept_slug="file_handling",
        difficulty=DifficultyLevel.MEDIUM,
        question_type=QuestionType.SHORT_ANSWER,
        prompt="Which mode should you pass to `open()` when you want to read a text file?",
        expected_answer="r",
        explanation="`r` opens a file in read mode.",
    ),
    AssessmentQuestionSeed(
        concept_slug="exception_handling",
        difficulty=DifficultyLevel.MEDIUM,
        question_type=QuestionType.SHORT_ANSWER,
        prompt="Which keyword catches an exception in Python?",
        expected_answer="except",
        explanation="`except` defines the branch that handles an error raised in the `try` block.",
    ),
    AssessmentQuestionSeed(
        concept_slug="modules",
        difficulty=DifficultyLevel.MEDIUM,
        question_type=QuestionType.SHORT_ANSWER,
        prompt="Which keyword brings code from another Python module into the current file?",
        expected_answer="import",
        explanation="Python uses the `import` keyword to load modules.",
    ),
)
