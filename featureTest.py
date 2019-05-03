from flask import Flask, render_template, request, jsonify
# import requests
import unittest
import index


class Testform(unittest.TestCase):
	def demoFunction(self):
		json_data = {
				  			"title": "test title",
			  				"description": "test description",
			  				"targetDate": "2010/09/09",
			  				"clientPriority": 3,
			  				"selectClient": 2,
			  				"productArea": 2
  						}
  		resp = request.post("http://127.0.0.1:5000/index", json=json_data)
  		resp = resp.json()
  		self.assertTrue(resp['success'])
        self.assertListEqual(resp['messages'], [])

if __name__ == '__main__':
    unittest.main()