import logging
from flask import Blueprint, request

routes_main = Blueprint('routes_main', __name__)

LOGGER = logging.getLogger(__name__)    

@routes_main.route('/')
def hello_world():
      """
      Micro Service Based on Flask
      Base route test for hello_world
      ---
      responses:
        200:
          description: Flask in Docker
        500:
          description: Bad error 
      """
      return "{'hello': 'world'}"