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
from apex_legends_api import ApexLegendsAPI, ALPlatform, ALAction, ALPlayer

api = ApexLegendsAPI(api_key='<api_key>')

player_name = '<PlayerName>'
platform = ALPlatform.PC
action = ALAction.GET

# Example 1:
# straight API calls
basic = api.basic_player_stats(player_name=player_name, platform=platform)
history = api.match_history(player_name=player_name, platform=platform, action=action)
origin_player = api.get_player_origin(player_name=player_name, show_all_hits=True)

print(basic)
print(history)
print(origin_player)

# Example 2:
# retrieve an 'ALPlayer' object
player: ALPlayer = api.get_player(name=player_name, platform=platform)
print(player.origin_info)
print(player.matches_tracked)

```
## Notes
- See https://apexlegendsapi.com for complete documentation.
- See [CHANGELOG.md](CHANGELOG.md) for history of changes