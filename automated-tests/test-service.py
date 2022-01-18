import requests
import unittest


APPLICATION_HOST = '192.168.100.23'
APPLICATION_PORT = 4000

class APITest(unittest.TestCase):
    def test_data_integrity(self):
        req = requests.post(f'http://{APPLICATION_HOST}:{APPLICATION_PORT}/api/gamecode', json=['batman', 'god of war'])
        print(f'test_data_integrity [type(req.json()) == dict]={type(req.json()) == dict}')
        self.assertEqual(type(req.json()), dict)

    def test_data_count(self):
        req = requests.post(f'http://{APPLICATION_HOST}:{APPLICATION_PORT}/api/gamecode', json=['batman'])
        print(f'test_data_count [len(req.json()[\'batman\']) < 10]={len(req.json()["batman"]) < 10}')
        self.assertLess(len(req.json()['batman']), 10)

    def test_invalid_game_id(self):
        test_string = '\"INVALID_APP_ID\"'
        req = requests.get(f'http://{APPLICATION_HOST}:{APPLICATION_PORT}/api/game/0000000000000000000000')
        print(f'test_invalid_game_id [req.text, INVALID_APP_ID]={req.text == test_string}')
        self.assertEqual(req.text, test_string)

if __name__ == '__main__':
    unittest.main()