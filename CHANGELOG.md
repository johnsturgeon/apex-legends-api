# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Modify the API usage so that it returns first class Objects instead of just a list

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
