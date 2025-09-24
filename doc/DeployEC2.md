# Deploy BackEnd EC2

## 1.- Verificar en qué rama estás (debe ser master)

<pre>
sudo -u myportfolio -H git -C /opt/myportfolio rev-parse --abbrev-ref HEAD
</pre>

## 2.- Traer lo último del remoto

<pre>
sudo -u myportfolio -H git -C /opt/myportfolio fetch --all
</pre>

## 3.- Comparar último commit local vs remoto

<pre>
sudo -u myportfolio -H git -C /opt/myportfolio log -1 --oneline
sudo -u myportfolio -H git -C /opt/myportfolio log -1 --oneline origin/master
</pre>

## 4.- Si ves diferencias, actualiza

<pre>
sudo -u myportfolio -H git -C /opt/myportfolio pull --rebase
</pre>

## 5.- (Opcional) Actualiza dependencias si cambió requirements.txt

<pre>
source /opt/myportfolio/.venv/bin/activate
pip install -U -r /opt/myportfolio/requirements.txt
deactivate
</pre>

## 6.- Reinicia tu servicio systemd y Apache

<pre>
# Reinicia el backend
sudo systemctl restart myportfolio
sudo systemctl status myportfolio --no-pager

# Recarga Apache (proxy reverso)
sudo systemctl reload apache2

</pre>

# 7.- Logs del servicio (systemd → Uvicorn/Gunicorn)

<pre>
# Estado + últimas líneas
sudo systemctl status myportfolio --no-pager

# Seguir el log en vivo
journalctl -u myportfolio -f --no-pager

# Últimos 200 registros desde el último arranque
journalctl -u myportfolio -b -n 200 --no-pager

# Buscar errores/tracebacks
journalctl -u myportfolio --since "15 min ago" | sudo grep -E "ERROR|Traceback"
</pre>

# 8.- Logs Apache

<pre>
# Errores de Apache
sudo tail -n 200 /var/log/apache2/error.log
sudo tail -f /var/log/apache2/error.log

# Accesos (para ver códigos 4xx/5xx)
sudo tail -n 200 /var/log/apache2/access.log

</pre>
