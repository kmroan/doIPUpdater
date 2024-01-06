# doIPUpdater

Update a Digital Ocean firewall with my public IP address to allow inbound SSH connections. 

## To-do:  

- Error handling
- Preserve existing firewall rules (if they exist) - currently this discards all rules and only recreates the SSH rule. 
- Use the schedule module to run hourly (or whatever, set schedule with an env var)
- finish docker image and deploy to Nomad
