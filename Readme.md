# Program Usage Guide  

This is a basic guide on how to use our program to create, upload, and download torrent files.  

---

## Setting Up the Python Virtual Environment  

First, you need to create a Python virtual environment to install and manage the program's dependencies. You can do this with the following command:  


python3 -m venv myenv


Next, activate the virtual environment using the command:  


source myenv/bin/activate


---

## Running the Program  

1. Navigate to the directory containing the program's source code:  


   cd app


2. Start the tracker using the command:  


   python3 tracker.py


3. Start a peer using the command:  


   python3 peer.py


---

## Main Features  

### Create a Torrent File  

To create a torrent file, use the following command:  


create <path to the file to create a torrent for> <path to the directory to save the torrent file> <tracker HTTP address>


### Upload a Torrent File  

To upload a torrent file, use the following command:  


upload <path to the torrent file> <tracker HTTP address>


### Download a Torrent File  

To download a torrent file, use the following command:  


download <path to the torrent file> <path to the directory to save the downloaded file>


Replace placeholders such as file paths and HTTP addresses with the specific details required for your use case.  

---

We wish you success in using the program! Let us know if you have any questions or need further assistance!"# CN_Assignment1" 
