

  <h1>🎮 FreeGamesBot-for-Telegram</h1>
  <p>A Telegram bot that notifies you about newly available <strong>free PC games</strong>.</p>

  <hr />

  <div class="card">
    <h2>✅ Requirements</h2>
    <p>Before starting, make sure you have:</p>
    <ul>
      <li><strong>Telegram</strong> installed on your phone/device</li>
      <li><strong>Docker Desktop</strong> installed on your PC</li>
    </ul>
    <p>Download Docker here: <a href="https://www.docker.com/" target="_blank" rel="noopener">https://www.docker.com/</a></p>
  </div>

  <div class="card">
    <h2>🤖 Create your Telegram Bot</h2>
    <ol>
      <li>Open Telegram and search for <strong>BotFather</strong></li>
      <li>Start the chat and type:
        <ul>
          <li><code>/start</code></li>
          <li><code>/newbot</code></li>
        </ul>
      </li>
      <li>Choose a name for your bot</li>
      <li>BotFather will generate a token to access the Telegram HTTP API</li>
    </ol>

    <div class="warn">
      <strong>⚠️ Important:</strong> Keep this token private and store it safely.
    </div>
  </div>

  <div class="card">
    <h2>⚙️ Configuration</h2>
    <ol>
      <li>Open <code>docker-compose.yml</code> using <strong>Visual Studio Code</strong></li>
      <li>Find this line:</li>
    </ol>
    <pre><code>BOT_TOKEN=</code></pre>
    <p>Paste your token after the <code>=</code>:</p>
    <pre><code>BOT_TOKEN=YOUR_TOKEN_HERE</code></pre>
  </div>

  <div class="card">
    <h2>📁 Project Setup</h2>
    <ol>
      <li>Create a new folder on your PC</li>
      <li>Copy the following files into the folder:</li>
    </ol>
    <ul>
      <li><code>bot.py</code></li>
      <li><code>docker-compose.yml</code> (with your token already added)</li>
      <li><code>Dockerfile</code></li>
      <li><code>requirements.txt</code></li>
    </ul>
  </div>

  <div class="card">
    <h2>🚀 Run the Bot (Docker)</h2>
    <ol>
      <li>Start <strong>Docker Desktop</strong></li>
      <li>Open <strong>PowerShell</strong> inside the project folder</li>
      <li>Run the following command:</li>
    </ol>
    <pre><code>docker compose up -d --build</code></pre>
    <p>✅ Your bot will run as long as Docker is running.</p>
  </div>

  <div class="card">
    <h2>🛑 Stop / Restart</h2>
    <h3>Stop the bot</h3>
    <pre><code>docker compose down</code></pre>
    <h3>Restart the bor</h3>
    <pre><code>docker compose up -d --build</code></pre>

  </div>

  <div class="card">
    <h2>📝 Notes</h2>
    <ul>
      <li>If you modify the code, rebuild the container using:</li>
    </ul>
    <pre><code>docker compose up -d --build</code></pre>
    <p class="muted">Make sure your bot token is never shared publicly.</p>
  </div>

  <p><strong>Enjoy your free games notifications! 🎁🔥</strong></p>
  <footer style="margin-top: 24px; text-align:center; color:#6b7280;">
  Made with ❤️ by Verrase
</footer>


</body>
</html>



