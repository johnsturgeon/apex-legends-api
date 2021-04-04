# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Added custom exception class for handling non 200 return status from the API

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
   - `al_domain` is the module that will contain all of the 'domain' based 
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
