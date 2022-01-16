import requests
import unittest


APPLICATION_HOST = '192.168.100.23'
APPLICATION_PORT = 4000

class APITest(unittest.TestCase):
    def test_data_integrity(self):
        req = requests.post(f'http://{APPLICATION_HOST}:{APPLICATION_PORT}/api/gamecode', json=['batman', 'god of war'])
        self.assertEqual(type(req.json()), dict)

    def test_data_count(self):
        req = requests.post(f'http://{APPLICATION_HOST}:{APPLICATION_PORT}/api/gamecode', json=['batman'])
        self.assertLess(len(req.json()['batman']), 10)

    def test_invalid_game_id(self):
        req = requests.get(f'http://{APPLICATION_HOST}:{APPLICATION_PORT}/api/game/0000000000000000000000')
        self.assertEqual(req.text, '\"INVALID_APP_ID\"')

if __name__ == '__main__':
    unittest.main()