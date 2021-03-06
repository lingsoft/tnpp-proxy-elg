import unittest
import requests
import json


endpoint = 'http://localhost:8000/process'


def create_payload(text):
    return {"type": "text", "content": text}


def create_payload_with_params(text, params):
    return {"type": "text", "content": text, "params": params}


def call_api(payload):
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(payload)
    return requests.post(
            endpoint, headers=headers, data=payload).json()


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.steady_text = "Tämä on testi."

    def test_api_response_type(self):
        payload = create_payload(self.steady_text)
        response = call_api(payload)
        self.assertEqual(response["response"]["type"], "annotations")

    def test_api_response_content(self):
        payload = create_payload(self.steady_text)
        response = call_api(payload)
        self.assertIn("udpipe/tokens", response["response"]["annotations"])

    def test_api_response_with_empty_text(self):
        payload = create_payload("")
        response = call_api(payload)
        self.assertEqual(response["failure"]["errors"][0]["code"],
                         "elg.request.invalid")

    def test_api_response_with_whitespace_text(self):
        payload = create_payload("      ")
        response = call_api(payload)
        self.assertEqual(response["failure"]["errors"][0]["code"],
                         "elg.request.invalid")

    def test_api_response_with_too_long_text(self):
        long_text = "Hei! " * 3001
        payload = create_payload(long_text)
        response = call_api(payload)
        self.assertEqual(response["failure"]["errors"][0]["code"],
                         "elg.request.too.large")

    def test_api_response_with_long_token(self):
        long_token = "å" * 10000
        payload = create_payload(long_token)
        response = call_api(payload)
        self.assertIn("udpipe/tokens", response["response"]["annotations"])

    def test_api_response_with_special_characters(self):
        spec_text = "\N{grinning face}" + self.steady_text + "\u0008"
        payload = create_payload(spec_text)
        response = call_api(payload)
        self.assertIn("udpipe/tokens", response["response"]["annotations"])

    def test_api_response_with_unsupported_language(self):
        wrong_lang = "使用人口について正確な統計はないが、日本国内の人口、"
        payload = create_payload(wrong_lang)
        response = call_api(payload)
        self.assertIn("udpipe/tokens", response["response"]["annotations"])

    def test_api_response_with_valid_parameters(self):
        params = {"includeConllu": True}
        payload = create_payload_with_params(self.steady_text, params)
        response = call_api(payload)
        self.assertIn("udpipe/conllu", response["response"]["annotations"])

    def test_api_response_with_invalid_parameters(self):
        params = {"includeConllu": "True"}
        payload = create_payload_with_params(self.steady_text, params)
        response = call_api(payload)
        self.assertEqual(response["failure"]["errors"][0]["code"],
                         "elg.request.invalid")

    def test_api_response_with_none_parameters(self):
        params = None
        payload = create_payload_with_params(self.steady_text, params)
        response = call_api(payload)
        self.assertIn("udpipe/tokens", response["response"]["annotations"])

    def test_api_response_with_empty_parameters(self):
        params = {}
        payload = create_payload_with_params(self.steady_text, params)
        response = call_api(payload)
        self.assertIn("udpipe/tokens", response["response"]["annotations"])


if __name__ == '__main__':
    unittest.main()
