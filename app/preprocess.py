import pandas as pd
from app.player import RookieStats
# ----------------------------
# Preprocessing / Feature engineering
# (recrée les features de l'étape 3 + indices composites)
# ----------------------------
def to_dataframe(payload: RookieStats) -> pd.DataFrame:
    # Map pydantic -> colonnes dataset d'origine (sans 'Name' ni 'TARGET_5Yrs')
    d = payload.dict(by_alias=True)
    base = {
        "GP": d["gp"],
        "MIN": d["min"],
        "PTS": d["pts"],
        "FGM": d["fgm"],
        "FGA": d["fga"],
        "FG%": d["fg_pct"],
        "3P Made": d["three_p_made"],
        "3PA": d["three_p_attempts"],
        "3P%": d["three_p_pct"],
        "FTM": d["ftm"],
        "FTA": d["fta"],
        "FT%": d["ft_pct"],
        "OREB": d["oreb"],
        "DREB": d["dreb"],
        "REB": d["reb"],
        "AST": d["ast"],
        "STL": d["stl"],
        "BLK": d["blk"],
        "TOV": d["tov"],
    }
    return pd.DataFrame([base])

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.fillna(0.0)
    eps = 1e-9
    mins = df["MIN"] + eps

    # Ratios/relatifs (étape 3)
    df["EFFICIENCY_PTS"]  = df["PTS"] / mins
    df["AST_TOV_RATIO"]   = df["AST"] / (df["TOV"] + 1.0)
    df["REB_PER_MIN"]     = df["REB"] / mins
    df["USAGE"]           = (df["FGA"] + df["FTA"] + df["TOV"]) / mins
    df["SHOOTING_ACCURACY"] = (df["FG%"] + df["FT%"] + df["3P%"]) / 3.0

    # Indices composites avancés
    df["OFF_INDEX"] = 0.4*df["PTS"] + 0.2*df["AST"] + 0.2*df["FGM"] + 0.2*df["FTM"]
    df["OFF_EFF_INDEX"] = 0.5*df["EFFICIENCY_PTS"] + 0.25*df["FG%"] + 0.25*df["FT%"]
    df["DEF_INDEX"] = 0.4*df["REB"] + 0.3*df["STL"] + 0.3*df["BLK"]
    df["ACTIVITY_INDEX"] = df["OFF_INDEX"] + df["DEF_INDEX"]
    df["BALANCE_RATIO"] = df["OFF_INDEX"] / (df["DEF_INDEX"] + eps)
    df["CONSISTENCY_INDEX"] = (
        0.5 * df["AST_TOV_RATIO"] +
        0.25 * df["SHOOTING_ACCURACY"] +
        0.25 * (1 - (df["TOV"] / (df["GP"] + eps)))
    )

    return df

def scale(df_feat: pd.DataFrame, FEATURE_LIST, SCALER_BUNDLE) -> pd.DataFrame:
    scaler = SCALER_BUNDLE["scaler"]
    df_feat = df_feat.copy()
    df_feat[FEATURE_LIST] = scaler.transform(df_feat[FEATURE_LIST])
    return df_feat

