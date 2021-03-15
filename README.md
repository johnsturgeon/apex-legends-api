# apex-legends-api
Python wrapper for https://apexlegendsapi.com

# Installation
You can install it from source, or pip (recommended)
# Requirements
`python >= 3.6`
### Source installation
`python ./setup.py install`
### Pip installation
`pip install apex-legends-api`

# Usage
* Register for an API Key at [Apex Legends API](https://apexlegendsapi.com)
* Here's a quick snippet to get started
* All method calls return a dictionary representing the JSON in the response.

```python
from apex_legends_api.base_api import ApexLegendsAPI
from apex_legends_api.base_api import Platform
from apex_legends_api.base_api import Action

api = ApexLegendsAPI(api_key='<api_key>')

player = '<PlayerName>'
platform = Platform.PC
action = Action.GET

basic = api.basic_player_stats(player_name=player, platform=platform)
history = api.match_history(player_name=player, platform=platform, action=action)
player = api.get_player_origin(player_name=player, show_all_hits=True)

```
## Notes
- See https://apexlegendsapi.com for complete documentation.
- See [CHANGELOG.md](CHANGELOG.md) for history of changes