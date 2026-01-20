# FreeGamesBot-for-Telegram
<h2>A Bot that informs you the new free games available for PC </h2>
<p>The first step is to Install telegram to your device phone.</p>
<p>The Second step is to install Docker from <a href="https://www.docker.com/">here</a>.</p>
<p>The third step, search BotFather in Telegram , type in BotFather chat the command /start , /newbot ,  name your bot and the BotFather willl gives you a token to acces the HTTP API , keep your token secure and store it safely.</p>
<p>The next step is to Edit the document called docker-compose.yml in visual studio putting the token thats had given to you by de BotFather, you must copy the token and paste next to BOT_TOKEN=</p>
<p>Copy all the documents (bot.py,docker-compose.yml with the modification of your token,Dockerfile and requirements.txt) and paste it on your PC in a new folder</p>
<p>Then start the app Docker </p>
<p>To turn on the bot, open power shell in the nwe folder and copy this command : docker compose up -d --build </p>
<p>Now you can use the telegram will be running while docker is turn on</p>
<p>For turn off just opne powershell on the folder and type docker compose down for restart docker compose up -d --build</p>


