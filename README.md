# final-project
302 final project (group 9)

UNAMED: Bot for NPC gaming experience
- frontend: game experience, running in unity
- backend: http server communitcating both ways with homebrewed language model and user

backend install:
  - ollama setup, see https://ollama.com/; I have it in running a docker
  - run 'ollama pull llama3.2:1b'
  - run 'python3 httpserver.py'
    - I am running this remotely on my machine, to interact with this on the WAN I am also portforwarding the httpserver script
    - to interact with the httpserver: 'curl -v -http0.9 <IP>:80 -d "{'prompt':'<request prompt>'}"'
    - to reset context for llama: 'curl -v -http0.9 <IP>:80 -d "{'prompt':'rs'}"'
