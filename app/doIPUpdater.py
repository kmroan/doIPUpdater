# source .venv/bin/activate
import os,requests
from pydo import Client
from dotenv import load_dotenv
from .config import logger

# Get/set environment vars from .env
load_dotenv()

client = Client(token=os.getenv("DO_TOKEN"))

# get the public IP address
ipUrl = "https://ifconfig.co/json"
headers = {"Content-Type":"application/json"}
response = requests.get(ipUrl,headers=headers)
pubIP = data = (response.json())['ip']

# Get the IP currently configured for for DO_FIREWALL_ID
response = client.firewalls.get(firewall_id=os.getenv("DO_FIREWALL_ID"))
firewall = response['firewall']

for i in firewall['inbound_rules']:
    if i['ports'] == "22":
        # get the IP for comparison, ignore subnet mask. 
        fwIp = ((i['sources']['addresses'][0]).split('/'))[0]
        if fwIp == pubIP:
            print(f"Configured IP {fwIp} matches current public IP {pubIP}")
            logger.info(f"Configured IP {fwIp} matches current public IP {pubIP}")
        else:
            print(f"IP Mismatch, DO: {fwIp}, public IP: {pubIP}")
            logger.info(f"IP Mismatch, DO: {fwIp}, public IP: {pubIP}")
            logger.info(f"...Updating DigitalOcean IP to {pubIP}")
            newIP = f"{pubIP}/32"
            req = {
                "name": firewall['name'],
                "inbound_rules": [
                    {
                    "protocol": "tcp",
                    "ports": "22",
                    "sources": {
                        "tags": [],
                        "addresses": [
                        newIP
                        ]
                    }
                    },
                    {
                        "protocol": "tcp",
                        "ports": "443",
                        "sources": {
                            "addresses":  ['0.0.0.0/0', '::/0']
                        }
                    },
                    {
                        "protocol": "tcp",
                        "ports": "80",
                        "sources": {
                            "addresses":  ['0.0.0.0/0', '::/0']
                        }
                    },

                ],
                "outbound_rules": [
                    {
                    "protocol": "tcp",
                    "ports": "0",
                    "destinations": {
                        "addresses": [
                        "0.0.0.0/0",
                        "::/0"
                        ]
                    }
                    },
                                        {
                    "protocol": "udp",
                    "ports": "0",
                    "destinations": {
                        "addresses": [
                        "0.0.0.0/0",
                        "::/0"
                        ]
                    }
                    }
                ],
                "droplet_ids": [
                    firewall['droplet_ids'][0]
                ],
                "tags": []
            }
            response = client.firewalls.update(firewall_id=firewall['id'],body = req)


