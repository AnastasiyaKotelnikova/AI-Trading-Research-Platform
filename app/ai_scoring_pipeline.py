import pandas as pd

from app.ai_ranker import add_ai_scores
from app.ai_score_engine import add_ai_analyst_score
from app.final_conviction import add_final_conviction
from app.portfolio_decision_engine import build_portfolio_decisions


def run_ai_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Runs the complete AI scoring pipeline on a dataframe.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    df = add_ai_scores(df)

    df = add_ai_analyst_score(df)

    df = add_final_conviction(df)

    df = build_portfolio_decisions(df)

    return df