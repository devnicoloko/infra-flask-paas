import logging
import json
from flask import Blueprint, request
import requests

routes_connect = Blueprint('routes_connect', __name__)

LOGGER = logging.getLogger(__name__)    

@routes_connect.route('/testtoken', methods=['POST'])
def test_token():
      """
      Route to test Keystone token
      This API is made with Flask and send data to Keystone
      ---
      parameters:
        - name: body
          in: body
          required: true
          schema:
            id: token_test
            properties:
              token:
                type: string

      responses:
        200:
          description: connect command receive, have the token
        400:
          description: Erreur dans la requete
        500:
          description: too bad error
      """
      # curl -H "X-Auth-Token:7a04a385b907caca141f" http://localhost:35357/v2.0/tokens/<AUTH_TOKEN>
      headers = {'X-Auth-Token': '7a04a385b907caca141f', }
      
      
      token = request.json.get('token')
      url = 'http://dk-keystone:35357/v2.0/tokens/'+token

      LOGGER.info(url)
      LOGGER.info(headers)

      resp = requests.get(url, headers=headers)

      LOGGER.info(resp.request.headers)

      return json.dumps(resp.json()), resp.status_code
      

@routes_connect.route('/connect', methods=['POST'])
def keystone_connect():
      """
      Route to get Keystone token
      This API is made with Flask and send data to Keystone
      ---
      parameters:
        - name: body
          in: body
          required: true
          schema:
            id: data_connect
            properties:
              login:
                type: string
              password:
                type: string

      responses:
        200:
          description: connect command receive, have the token
        400:
          description: Erreur dans la requete
        500:
          description: too bad error
      """
      code_return = 200


      login = request.json.get('login')
      passwd = request.json.get('password')

      headers = {'Content-type': 'application/json'}
      post_data = {'auth':{'passwordCredentials':{'username': login, 'password': passwd}}}


      LOGGER.info(post_data)

      resp = requests.post('http://dk-keystone:35357/v2.0/tokens', data = json.dumps(post_data), headers = headers)
      # curl -d '{"auth":{"passwordCredentials":{"username": "Joe", "password": "1234"}}}'  \
      # -H "Content-type: application/json" \
      # http://localhost:35357/v2.0/tokens

      LOGGER.info(resp)        
      
      return json.dumps(resp.json()), resp.status_code
