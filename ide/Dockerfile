FROM codercom/code-server:latest

# Install Python and pip inside the container
RUN sudo apt-get update && \
    sudo apt-get install -y python3 python3-pip git && \
    sudo apt-get clean

# Set default password (use env var for better security)
ENV PASSWORD=1234

# Expose code-server port
EXPOSE 8080
