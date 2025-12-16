from pydantic import BaseModel, Field, field_validator
from typing import Optional
import numpy as np


# ----------------------------
# Pydantic schema for raw input
# ----------------------------

class RookieStats(BaseModel):
    gp: float = Field(..., description="Games Played")
    min: float = Field(..., description="MinutesPlayed")
    pts: float
    fgm: float
    fga: float
    fg_pct: float = Field(..., ge=0, le=100, description="FieldGoalPercent in [0,100]")
    three_pm: float = Field(..., alias="three_p_made", description="3P Made")
    three_pa: float = Field(..., alias="three_p_attempts")
    three_p_pct: Optional[float] = Field(None, ge=0, le=100, description="3P% in [0,100]")
    ftm: float
    fta: float
    ft_pct: float = Field(..., ge=0, le=100, description="FT% in [0,100]")
    oreb: float
    dreb: float
    reb: float
    ast: float
    stl: float
    blk: float
    tov: float

    @field_validator("three_p_pct", mode="before")
    def fill_3p_pct(cls, v):
        # Certains rookies n'ont pas tenté -> 3P% manquant => 0.0
        return 0.0 if v is None or (isinstance(v, float) and np.isnan(v)) else v
