import unittest
from src.risk_model import WearableFeatures, risk_score

class RiskModelTests(unittest.TestCase):
    def test_higher_risk_profile_scores_higher(self):
        low = WearableFeatures(28, 60, 70, 8, 11000, 180)
        high = WearableFeatures(65, 92, 20, 5, 2500, 20)
        self.assertGreater(risk_score(high)["score"], risk_score(low)["score"])

    def test_band_output(self):
        x = WearableFeatures(30, 65, 60, 8, 9000, 150)
        self.assertIn(risk_score(x)["band"], {"LOW","MODERATE","ELEVATED"})

    def test_invalid_input_rejected(self):
        with self.assertRaises(ValueError):
            risk_score(WearableFeatures(10, 70, 50, 8, 5000, 30))

if __name__ == "__main__":
    unittest.main()
