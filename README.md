

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
    <h3>Restart the bot</h3>
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


</hr>
 <h1>🎮 FreeGamesBot-for-Telegram</h1>
  <p>Un bot de Telegram que te avisa cuando hay nuevos <strong>juegos gratis para PC</strong>.</p>

  <hr />

  <div class="card">
    <h2>✅ Requisitos</h2>
    <p>Antes de empezar, asegúrate de tener:</p>
    <ul>
      <li><strong>Telegram</strong> instalado en tu móvil/dispositivo</li>
      <li><strong>Docker Desktop</strong> instalado en tu PC</li>
    </ul>
    <p>Descarga Docker aquí: <a href="https://www.docker.com/" target="_blank" rel="noopener">https://www.docker.com/</a></p>
  </div>

  <div class="card">
    <h2>🤖 Crear tu bot de Telegram</h2>
    <ol>
      <li>Abre Telegram y busca <strong>BotFather</strong></li>
      <li>Inicia el chat y escribe:
        <ul>
          <li><code>/start</code></li>
          <li><code>/newbot</code></li>
        </ul>
      </li>
      <li>Elige un nombre para tu bot</li>
      <li>BotFather generará un token para acceder a la API HTTP de Telegram</li>
    </ol>

  <div class="warn">
      <strong>⚠️ Importante:</strong> Mantén este token en privado y guárdalo de forma segura.
    </div>
  </div>

  <div class="card">
    <h2>⚙️ Configuración</h2>
    <ol>
      <li>Abre el archivo <code>docker-compose.yml</code> usando <strong>Visual Studio Code</strong></li>
      <li>Busca esta línea:</li>
    </ol>
    <pre><code>BOT_TOKEN=</code></pre>
    <p>Pega tu token después del <code>=</code>:</p>
    <pre><code>BOT_TOKEN=TU_TOKEN_AQUI</code></pre>
  </div>

  <div class="card">
    <h2>📁 Preparación del proyecto</h2>
    <ol>
      <li>Crea una carpeta nueva en tu PC</li>
      <li>Copia los siguientes archivos dentro de esa carpeta:</li>
    </ol>
    <ul>
      <li><code>bot.py</code></li>
      <li><code>docker-compose.yml</code> (con tu token ya añadido)</li>
      <li><code>Dockerfile</code></li>
      <li><code>requirements.txt</code></li>
    </ul>
  </div>

  <div class="card">
    <h2>🚀 Ejecutar el bot (Docker)</h2>
    <ol>
      <li>Inicia <strong>Docker Desktop</strong></li>
      <li>Abre <strong>PowerShell</strong> dentro de la carpeta del proyecto</li>
      <li>Ejecuta este comando:</li>
    </ol>
    <pre><code>docker compose up -d --build</code></pre>
    <p>✅ Tu bot funcionará mientras Docker esté encendido.</p>
  </div>

  <div class="card">
    <h2>🛑 Parar / Reiniciar</h2>

  <h3>Parar el bot</h3>
    <pre><code>docker compose down</code></pre>

  <h3>Reiniciar el bot</h3>
    <pre><code>docker compose up -d --build</code></pre>
  </div>

  <div class="card">
    <h2>📝 Notas</h2>
    <ul>
      <li>Si modificas el código, vuelve a reconstruir el contenedor con:</li>
    </ul>
    <pre><code>docker compose up -d --build</code></pre>
    <p class="muted">Asegúrate de no compartir nunca tu token del bot públicamente.</p>
  </div>

  <p><strong>¡Disfruta de tus notificaciones de juegos gratis! 🎁🔥</strong></p>

  <footer style="margin-top: 24px; text-align:center; color:#6b7280;">
    Hecho con ❤️ por Verrase
  </footer>

</body>
</html>
