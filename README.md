# Chat Application with GUI over TCP/IP Developed in Python using PyQt5

Hello friends,

This is a personal project I created about 3-4 years ago as a way for me to practice PyQt5, Socket, Threading, and a little bit of networking. The application is composed of three main files:

* **server.py:** This file should be running on the server-side. It opens a connection to a port of your choosing and then waits for and handles client connections.
* **welcome.py:** This is the first file run by users wanting to access the chat app. It asks the user for the host and port they're trying to connect to, as well as their name.
* **chat.py:** Once the client has entered the necessary information in welcome.py, the welcome window hides, and the chat window appears.

ℹ **welcome2.py** is used to simulate two different clients.  
ℹ The **resources** folder contains pictures and audio files used.

## Server Functionalities

* Send broadcast messages to all users at any given time.
* Send client connectivity update messages to all users.

## Client Functionalities

* See an updated list of currently connected clients.
* Ring a client of your choosing.
* Ring all clients.
* Use custom emojis.
* Send private messages.
* See a list of all available commands using `/h`.

## Some Screenshots
### Welcome.py
<img src="1.png" alt="Screenshot" width="50%">

### Server and Client example
<img src="2.png" alt="Screenshot" width="50%">

#### Bonus
You can see all of my to-dos in code, which are the tasks I envisioned completing, such as opening a private messaging tab.  
