# Add/drop camper

Helps camp for modules during add/drop for studies. 

Uses Selenium together with Chrome or Firefox to periodically check for updates on the target site. 
Does not typically work out of the box, as the relevant links and beautifulsoup searches will have to be heavily modified for the program to work.
Program will run until target module is obtained.

## Instructions

#### Step 1. Create a `pwd.yaml` file and replace with relevant information

`printf "username:<user>\npassword:<pass>\nSITE_URL:<url>" > pwd.yaml`

If you already have an existing `pwd.yaml`, you can upload using ssh through

`scp pwd.yaml root@<IP addr>:<target_directory>`

#### Step 2. Install relevant python packages

*Note that most OSX and Ubuntu comes pre-installed with Python, 
however if yours does not, you will need to install Python and Pip before doing this step***

If pip is not installed

`sudo apt update`

`sudo apt install python3-pip`

Then run: 

`pip3 install selenium beautifulsoup4 pyyaml`

## Option 1: Running using Docker with Selenium and Chrome

This method is less dependent on the environment, which the author's experience is that you may encounter problems when trying to install or run Firefox or geckodriver. Hence would recommend this method if you are running off DigitalOcean, AWS or Google Cloud

#### Step 3. Install [Docker](https://docs.docker.com/engine/install/ubuntu/)

`sudo apt-get update`

`sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common`

`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`

```sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"```
   
`sudo apt-get install docker-ce docker-ce-cli containerd.io`

#### Step 4. Test Docker

`sudo docker run hello-world`

#### Step 5. Download required Docker image (using docker run automatically downloads image)

`docker run -d -p 4444:4444 selenium/standalone-chrome`

#### Step 6. Check code in `scrape.py`, and ensure option 1 is uncommented, while option 2 is commented

```python:
# Option 1
driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)
```

#### Step 7. Run code

`python3 scrape.py`

To run in background, so it continues after ssh is disconnected

`nohup python3 scrape.py &`

## Option 2: Running on local installation of Firefox and geckodriver

#### Step 3. Install Firefox (if not already installed)

`sudo apt-get update`

`sudo apt install firefox`

#### Step 4. Install geckodriver and set permissions

`wget https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux32.tar.gz`

`tar -xvzf geckodriver-v0.28.0-linux32.tar.gz`

`chmod +x geckodriver`

#### Step 5. Move geckodriver to somewhere in PATH

Check directories in PATH by running `echo \$PATH`, but typically `/usr/local/bin` should be in PATH by default

`mv geckodriver /usr/local/bin/`

#### Step 6. Check `scrape.py` that option 2 is uncommented while option 1 is commented

```python:
# Option 2: Run locally on Mac/PC with Firefox 
options = Options()
options.headless = True   
driver = webdriver.Firefox(options=options)
```

