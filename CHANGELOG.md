# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.3] - 2021-05-09
### Fixed
- Fixed grand soirée kills as being mis-reported and not counted in their categories

## [2.0.2] - 2021-05-06
### Fixed
- Fixed arena kills / damage / wins as being mis-reported and not counted in their categories

## [2.0.1] - 2021-05-04
### Fixed
- Fixed workflow issue

## [2.0.0] - 2021-05-04
### Fixed
EMERGENCY FIX #2: API is breaking with Season 9 release
Turns out that having a tracker with no known value breaks.
That breaks things.

### Changed
- Bumping the min python version to 3.9

## [1.5.1] - 2021-05-04
### Fixed
EMERGENCY FIX: API is breaking with Season 9 release
Turns out that having a rank that was NOT YET CALCULATED tried to convert a string to an int
That breaks things.

## [1.5.0] - 2021-05-01
### Changed
- Changed the `nametouid` method to return just the int result instead of the list

## [1.4.2] - 2021-05-01
### Added
- Added new API for adding a player by UID

## [1.4.1] - 2021-05-01
### Added
- Added new API for getting the players UID for a given name and platform
- Updated to publish on [Read The Docs](https://apex-legends-api.readthedocs.io/)

## [1.4.0]
### Added
- Added api versions for querying users by UID as well as by Name
- Added api for getting a ALPlayer by UID as well.

### Changed
- Updated README to reflect a call by UID

### Removed
- Removed the api for deleting all tracked players

## [1.3.4]
- Fixed the `category` to combine kills for seasons into a `kills` category

## [1.3.3]
### Fixed
- Fixed the `category` to combine wins for seasons into a 'wins' category

## [1.3.2]
### EMERGENCY FIX
- Fixed category to use 'lstrip' instead of 'strip' because it chopped off the wrong thing

## [1.3.1]
### Added
- Added new property `category` to `DataTracker` which strips the 'specialEvent_' from the key.
  The result is that `damage` and `specialEvent_damage` are treated as the same category

## [1.3.0]
### Added
- Added PyPi download badge to README
- Added support for Account level badges
- Added new unit tests for badges

### Changed
- Got rid of class `SelectedLegend` and now just use `Legend` for all legends

### Fixed
- Fixed CHANGELOG headers for the last few releases

## [1.2.1]
### Fixed
-  Fixed version info in `setup.py`
-  Fixed release to publish correctly

## [1.2.0]
### Added
- Added support for new addition to the API for showing Legend Tracker stat ranking.
- Added parameter to API calls (and player creation) to skip stat ranking (can speed up API request)
  * NOTE: `TrackerRank` will still be part of the legend's tracker, but the values will all be '-1'
- New unit tests to support tracker rank

## [1.1.0]
### Added
- Added docstring comments for every single attribute and class so that they are more easily inspected
- Added `events` api (to replace `match_history`) - same signature, just different name to better reflect its usage

### Removed
- Deprecated `match_history` api (in favor of `events`)

## [1.0.2]
### Added
- Added custom exception class for handling non 200 return status from the API
- Added type hints to EVERYTHING.  This will make working with the API much easier

### Fixed
- Throws exception if API request fails (#9)
- [internal] Changed query arguments from f-strings to request params (#34)

## [1.0.1]
### Added
- Added ranked progression event to list of Events tracked (thanks @CondensedTea)

## [1.0.0] First Major release
### Summary of changes
This release represents the biggest change for the API to date.  Essentially, all interaction
can now be done through the `ALPlayer` class.  See the README.md for usage.

### Added
- `ALPlayer` class now pulls all the data including events if the player is being tracked.
- New convenience method `print_description` for dumping a player class to a readable format
- `ALPlayer` is structured to match the json response from the API

### Changed
- Player history is automatically added to the player class when created by the API
- Arrow library is now required for timestamp parsing

### Fixed
- Response for non-tracked player no longer throws an uncaught exception

## [0.3.0]
### Changed
- Re-arranged module files and imports
  - `al_base` is where utility / base classes will go that are shared across modules
  - `al_api` is the core API interface class
  - `al_domain` is the module that will contain all the 'domain' based
    classes such as `ALPlayer` (eventually 'matches', etc...)
- Class renames (which will change the API).  Now all classes are prefixed with `AL` (Apex Legends)
- Updated README.md to reflect the changes

### Added
- Added 'Player' class
- Added new method to the API to delete all tracked players

## [0.2.1]
### Changed
- the module is now exporting all the classes through the `__init__.py` which will make importing
  simpler
- Moved `ApexLegendsAPI` class to its own file

## Fixed
- Removed debug code that dumped the response json to a file

## [0.2.0]
### Fixed
- Fixed return types from all api calls to be consistent (list)

### Changed
- Changed return types from dict to list
- Changed the `get_player_origin` api to no longer pass the (unused) platform parameter
- Added `show_all_hits` to the `get_player_origin` api to allow for searching the origin for users

## [0.1.13]
### Changed
- `setup.py` now imports the requirements from requirement.txt

### Added
- added a manifest for setup.py distribution packaging

## [0.1.12]
### Fixed
- Fixed the version number for requests package in [setup.py](setup.py)

## [0.1.11]
### Added
- Added this changelog

### Changed
- Updated [README.md](README.md) to point to this changelog

## [0.1.10] - 2021-03-14
### Fixed
- Fixed a typo in [README.md](README.md)

## [0.1.9] - 2021-03-14
### Added
- All basic functionality (documented in the [README.md](README.md))

### Changed
- Initial checkin

### Removed
- n/a
