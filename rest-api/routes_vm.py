import logging
import json
from rabbitmq_publisher import example
from flask import Blueprint, request, Response
import requests
import os
import uuid
from redisclass import DBRedis

routes_vm = Blueprint('routes_vm', __name__)

LOGGER = logging.getLogger(__name__) 

redis = DBRedis()

user_name = ""

@routes_vm.before_request
def before_request():
      LOGGER.info('before request in vm')
      headers = {'X-Auth-Token': '7a04a385b907caca141f'}
      
      token = request.headers.get('X-TOKEN')
      url = 'http://'+os.environ['AUTH_KEYSTONE']+':35357/v2.0/tokens/'+token

      resp = requests.get(url, headers=headers)

      if(200 <= resp.status_code < 300):
        LOGGER.info('user_id: '+resp.json()['access']['user']['id'])
        user_name=resp.json()['access']['user']['id']
        return
      else:
        return Response(status_code=401,status=resp.text)
      

@routes_vm.route('/', methods=['POST'])
def vm_create():
      """
      Route to create vm
      This API is made with Flask and send data to RabbitMQ
      ---
      tags:
          - vmmanagement
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
        - name: X-TOKEN
          in: header
          required: True
          type: string
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
        message['uuid']= str(uuid.uuid4())
        message['owner']=user_name
        message['state']='INPROGRESS'

        msg['uuid']=message['uuid']

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
      tags:
          - vmmanagement
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
        - name: X-TOKEN
          in: header
          required: True
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

@routes_vm.route('/<string:vmuuid>', methods=['GET'])
def vm_state(vmuuid):
      """
      Route to delete vm
      This API is made with Flask and send data to RabbitMQ
      ---
      tags:
          - vmmanagement
      parameters:
        - name: vmuuid
          in: path
          required: true
          type: string
        - name: X-TOKEN
          in: header
          required: True
          type: string
      responses:
        200:
          description: VM state command
          schema:
            id: data_create_vm
        400:
          description: Erreur dans la requete
        500:
          description: too bad error
      """
      code_return = 200

      msg = redis.get_json(vmuuid)
      
      LOGGER.info(msg)
      return msg, code_return
