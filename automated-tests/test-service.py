import requests
import unittest


APPLICATION_HOST = '192.168.100.2'
APPLICATION_PORT = 8000

class APITest(unittest.TestCase):
    def test_data_integrity(self):
        req = requests.post(f'http://{APPLICATION_HOST}:{APPLICATION_PORT}/api/gamesearch', json=['batman', 'god of war'])
        self.assertEqual(type(req.json()), dict)

    def test_data_count(self):
        req = requests.post(f'http://{APPLICATION_HOST}:{APPLICATION_PORT}/api/gamesearch', json=['batman'])
        self.assertLess(len(req.json()['batman']), 10)

    def test_invalid_game_id(self):
        req = requests.post(f'http://{APPLICATION_HOST}:{APPLICATION_PORT}/api/game/0000000000000000000000')
        self.assertEqual(req.text, '\"INVALID APPLICATION ID\"')

if __name__ == '__main__':
    unittest.main()