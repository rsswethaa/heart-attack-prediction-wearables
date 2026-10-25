import unittest
import app as app_module
class EndToEndSmokeTests(unittest.TestCase):
    def setUp(self): app_module.app.config['TESTING']=True; self.client=app_module.app.test_client()
    def test_health_home_platform(self):
        self.assertEqual(self.client.get('/health').status_code,200); self.assertEqual(self.client.get('/').status_code,200); self.assertEqual(self.client.get('/api/platform/status').status_code,200)
    def test_forecast(self):
        rows=[{'resting_hr':70+i,'hrv_ms':55-i,'sleep_hours':7-.1*i,'steps':8000-100*i,'spo2':98} for i in range(5)]; r=self.client.post('/api/forecast',json={'readings':rows}); self.assertEqual(r.status_code,200); self.assertIn('projections',r.get_json())
if __name__=='__main__': unittest.main()
