# Add/drop camper

Helps camp for modules during add/drop for studies

## Instructions

Create a `pwd.yaml` file with `echo "username:<user>\npassword:<pass>\nSITE_URL:<url>\nLOGIN_URL:<url>\nCRAWL_URL:<url>" > pwd.yaml`, and replace with relevant information.

## Installation

Install necessary packages
`pip install selenium`
`pip install beautifulsoup4`
`pip install pyyaml`

Install geckodriver and set permissions
`wget https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux32.tar.gz`
`tar -xvzf geckodriver-v0.28.0-linux32.tar.gz`

`chmod +x geckodriver`

Add path of geckodriver
`export PATH=$PATH:/path-to-extracted-file/`
