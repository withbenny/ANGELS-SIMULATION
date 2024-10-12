from tools import ScoreCalculator
import pandas as pd

data = pd.read_csv('short.csv')
data = ScoreCalculator().apply_score(data)
data.to_csv('short_with_scores.csv', index=False)