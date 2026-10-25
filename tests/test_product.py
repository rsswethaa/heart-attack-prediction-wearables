import unittest

import app as dashboard
from src.timeseries import analyse_history


class ProductTests(unittest.TestCase):
    def setUp(self):
        dashboard.app.config.update(TESTING=True)
        self.client = dashboard.app.test_client()

    def test_demo_dashboard_api(self):
        response = self.client.get('/api/demo')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn('trend_aware', payload)
        self.assertEqual(len(payload['series']), 14)

    def test_trend_aware_score_responds_to_deteriorating_series(self):
        rows = [
            {'date':f'2026-10-{10+i:02d}','resting_hr':65+i*2,'hrv_ms':65-i*3,'sleep_hours':7.5-i*.2,'steps':9000-i*300,'exercise_minutes':30,'spo2':98}
            for i in range(7)
        ]
        result = analyse_history(45, rows)
        self.assertGreaterEqual(result['trend_aware']['score'], result['baseline']['score'])
        self.assertIn('Resting HR', result['contributions'])

    def test_requires_enough_history(self):
        response = self.client.post('/api/analyse', json={'age':40,'readings':[{'resting_hr':70,'hrv_ms':50,'sleep_hours':7,'steps':8000}]})
        self.assertEqual(response.status_code, 400)

    def test_health(self):
        self.assertEqual(self.client.get('/health').get_json()['status'], 'ok')


if __name__ == '__main__':
    unittest.main()
