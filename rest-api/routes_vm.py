import logging
import json
from rabbitmq_publisher import example
from flask import Blueprint, request, Response
import requests
import os

routes_vm = Blueprint('routes_vm', __name__)

LOGGER = logging.getLogger(__name__) 

@routes_vm.before_request
def before_request():
      LOGGER.info('before request in vm')
      headers = {'X-Auth-Token': '7a04a385b907caca141f'}
      
      token = request.json.get('token')
      url = 'http://'+os.environ['AUTH_KEYSTONE']+':35357/v2.0/tokens/'+token

      LOGGER.info(url)

      resp = requests.get(url, headers=headers)
      LOGGER.info(resp)

      if(200 <= resp.status_code < 300):
        LOGGER.info(resp.text)
        return
      else:
        LOGGER.info(resp.text)
        return Response(status_code=401,status=resp.text)
      

@routes_vm.route('/', methods=['POST'])
def vm_create():
      """
      Route to create vm
      This API is made with Flask and send data to RabbitMQ
      ---
      parameters:
        - name: body
          in: body
          required: true
          schema:
            id: data_create_vm
            properties:
              token:
                type: string
              app_env:
                type: string
                enum:
                  - DEV
                  - HML
                  - PRD
              app_trigram:
                type: string
              vm_hostname:
                type: string
              vm_desc:
                type: string
              vm_profile:
                type: string
                enum:
                  - Micro
                  - Medium
                  - Large
              vm_region:
                type: string
                enum: 
                  - GreaterParis
                  - North
      responses:
        200:
          description: VM create command receive, wait for it
        400:
          description: Erreur dans la requete
        500:
          description: too bad error
      """
      vm_hostname = request.json.get('vm_hostname')
      msg = {'status': 'OK'}
      code_return = 200

      if "lx" in vm_hostname:
      
        message = request.json

        LOGGER.info(message)  
        example.publish_message(message, 'vm_create')
      else:
        LOGGER.info("VM Hostname non conforme")  
        msg = {'request_error': 'bad hostname'}
        code_return = 400
      
      return json.dumps(msg), code_return

@routes_vm.route('/', methods=['DELETE'])
def vm_delete():
      """
      Route to delete vm
      This API is made with Flask and send data to RabbitMQ
      ---
      parameters:
        - name: body
          in: body
          required: true
          schema:
            id: data_delete_vm
            properties:
              token:
                type: string
              vm_hostname:
                type: string

      responses:
        200:
          description: VM delete command receive, wait for it
        400:
          description: Erreur dans la requete
        500:
          description: too bad error
      """
      vm_hostname = request.json.get('vm_hostname')
      msg = {'status': 'OK'}
      code_return = 200

      if "lx" in vm_hostname:
      
        message = request.json

        LOGGER.info(message)  
        example.publish_message(message, 'vm_delete')
      else:
        LOGGER.info("VM Hostname non conforme")  
        msg = {'request_error': 'bad hostname'}
        code_return = 400
      
      return json.dumps(msg), code_return
