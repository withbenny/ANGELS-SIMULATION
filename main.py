from tools import ScoreCalculator, Classifier
import pandas as pd

data = pd.read_csv('angels_simulation.csv')
data = ScoreCalculator().apply_score(data)
data.to_csv('angels_simulation_with_score.csv', index=False)

data = pd.read_csv('angels_simulation.csv')
data = Classifier().apply_class(data)
data.to_csv('angels_simulation_with_class.csv', index=False)