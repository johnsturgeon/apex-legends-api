apex-legends-api
================

Python wrapper for https://apexlegendsapi.com

|Downloads|

Installation
============

You can install it from source, or pip (recommended)

Requirements
============

``python >= 3.6``

Source installation
-------------------

``python ./setup.py install``

Pip installation
----------------

``pip install apex-legends-api``

Usage
=====

-  Register for an API Key at `Apex Legends
   API <https://apexlegendsapi.com>`__
-  Here’s a quick snippet to get started
-  All method calls return a dictionary representing the JSON in the
   response.

.. code:: python

   import sys
   from apex_legends_api import ApexLegendsAPI,\
       ALPlatform,\
       ALPlayer,\
       ALAction,\
       ALHTTPExceptionFromResponse
   from apex_legends_api.al_base import print_description

   api = ApexLegendsAPI(api_key='<api_key>')

   player_name = str("PlayerName")
   player_uid = str("1234567890")
   platform = ALPlatform.PC
   action = ALAction.GET

   # Example 1:
   # straight API calls
   try:
       basic = api.basic_player_stats(player_name=player_name, platform=platform)
       # or query by UID
       # basic = api.basic_player_stats_by_uid(uid=player_uid, platform=platform)
       history = api.events(player_name=player_name, platform=platform, action=action)
       origin_player = api.get_player_origin(player_name=player_name, show_all_hits=True)
   except ALHTTPExceptionFromResponse as exception:
       print(exception)
       sys.exit()

   print(basic)
   print(history)
   print(origin_player)

   # Example 2:
   # retrieve an 'ALPlayer' object
   player: ALPlayer = api.get_player(name=player_name, platform=platform)
   print_description(player)

Notes
-----

-  See https://apexlegendsapi.com for complete documentation.
-  See
   `CHANGELOG.md <https://github.com/johnsturgeon/apex-legends-api/blob/main/CHANGELOG.md>`__
   for history of changes

.. |Downloads| image:: https://pepy.tech/badge/apex-legends-api/week
   :target: https://pepy.tech/project/apex-legends-api
