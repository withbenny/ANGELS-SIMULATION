from tools import ScoreCalculator, Classify
import pandas as pd

data = pd.read_csv('short.csv')
data = ScoreCalculator().apply_score(data)
data.to_csv('short_with_score.csv', index=False)

data = pd.read_csv('short.csv')
data = Classify().classifier(data)
data.to_csv('short_with_class.csv', index=False)