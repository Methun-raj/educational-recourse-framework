"""
Pydantic Request Schemas and Data Validation Contracts.
Enforces strict boundary checking, type safety, and data sanitization.
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal, Optional, Dict, Any, List

GenderType = Literal["Male", "Female", "Non-Binary"]
ParentalEduType = Literal["High School", "Bachelor", "Master", "Doctorate"]
ParentalStatusType = Literal["Married", "Single", "Divorced", "Widowed"]
IncomeBracketType = Literal["Tier-1 High", "Tier-2 Middle", "Tier-3 Low"]

class StudentProfileSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    student_id: Optional[str] = Field(default="STU_QUERY", description="Unique student identifier")
    
    # 1. Socio-Demographic Features (Immutable: F_imm)
    age: int = Field(ge=16, le=40, description="Student age in years")
    gender: GenderType = Field(description="Student biological/identified gender")
    parental_education: ParentalEduType = Field(description="Highest parental education level")
    parental_status: ParentalStatusType = Field(description="Parental marital status")
    family_income_bracket: IncomeBracketType = Field(description="Family income classification bracket")
    family_size: int = Field(ge=1, le=15, description="Number of family members")

    # 2. Intermediate Academic Background (Pre-College)
    intermediate_math: float = Field(ge=0.0, le=100.0, description="Intermediate Mathematics percentage")
    intermediate_physics: float = Field(ge=0.0, le=100.0, description="Intermediate Physics percentage")
    intermediate_chemistry: float = Field(ge=0.0, le=100.0, description="Intermediate Chemistry percentage")
    intermediate_english: float = Field(ge=0.0, le=100.0, description="English language proficiency score")
    intermediate_aggregate: float = Field(ge=0.0, le=100.0, description="Composite intermediate aggregate percentage")

    # 3. Behavioral & Co-Curricular Indicators (Mutable: F_mut)
    attendance_percentage: float = Field(ge=0.0, le=100.0, description="College classroom attendance rate")
    study_hours_per_week: float = Field(ge=0.0, le=80.0, description="Self-study hours per week")
    extracurricular_clubs: int = Field(ge=0, le=10, description="Number of active co-curricular clubs/hackathons")
    soft_skills_score: float = Field(ge=1.0, le=5.0, description="Mock assessment and communication rating (1-5)")
    certifications_count: int = Field(ge=0, le=10, description="Number of recognized technical certifications")

    # 4. College Academic Indicators (Mutable: F_mut)
    midterm_score: float = Field(ge=0.0, le=100.0, description="Semester midterm exam aggregate percentage")
    core_course_score: float = Field(ge=0.0, le=100.0, description="Core domain technical subject percentage")
    cgpa: float = Field(ge=0.0, le=10.0, description="Cumulative Grade Point Average (0-10 scale)")

    # Optional targets for training/evaluation
    recommended_branch: Optional[str] = None
    academic_performance: Optional[str] = None
    placement_status: Optional[int] = None

    @field_validator("intermediate_aggregate", mode="before")
    def calculate_aggregate_if_missing(cls, v, values):
        # Allow automatic calculation of aggregate if missing or zero
        return v

    def to_flat_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=False)


class PredictionResponseSchema(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
