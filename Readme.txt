Final Project for CS50

VIDEO DESCRIPTION: https://www.youtube.com/watch?v=PM2yk-WaZJA

Complete web api including server and client side code.
Usage
1. Install node.js from main website or using 
	$ sudo apt install nodejs

2. Install MongoDB from main website and add folder with mongo.exe to path
	https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
	sudo systemctl start mongod

3. once node.js is installed, cd into /react-flask-stt/client and run npm install, this may take a while 
	after node modules are installed run npm start to open React front end

	$ cd react-flask-stt
	$ npm install
	$ npm start

4. run MongoDB by typing mongo in terminal
	$ mongo

5. cd into the server and run python app.py to start flask backend

	$ pip install -r requirements.txt
	$ python summarizer.py --install
	$ python app.py

7. React app should be responsive now and try to test audio file, text files and recorder

Note: Incase "Transcribed files" show "Loading" that means the database is not started or installed. Make sure mongo is running in a terminal
Note: after uploading a file the terminal running app.py shows the summaries being generated, while React app shows "Processing"
