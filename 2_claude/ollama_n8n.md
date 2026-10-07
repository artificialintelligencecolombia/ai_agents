# Ollama integration with n8n

- n8n lives in the cloud, self hosted in a docker container.
- Ollama is a local LLM.
- ip address of the n8n server is unknown
- Ollama listens on 127.0.0.1:11434
- server has a reverse proxy, n8n is not accessible from the internet
- tailscale is installed in both the n8n server and the Ollama server, so they can communicate with each other over a tailscale network.

