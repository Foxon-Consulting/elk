#!/usr/bin/env python3
"""
Script de test pour vérifier le champ log_level
"""

import socket
import time
from datetime import datetime, timedelta

def generate_iso8601_timestamp(offset_seconds=0):
    """
    Génère un timestamp au format ISO8601 avec un offset optionnel
    
    Args:
        offset_seconds (int): Délai en secondes à ajouter à la date actuelle
    
    Returns:
        str: Timestamp au format ISO8601 (YYYY-MM-DDTHH:mm:ssZ)
    """
    now = datetime.now() + timedelta(seconds=offset_seconds)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")

def test_log_level():
    """Test d'envoi de logs pour vérifier le champ log_level"""
    try:
        # Créer un socket TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        # Se connecter à Logstash
        print("Tentative de connexion à Logstash sur localhost:50000...")
        sock.connect(('localhost', 50000))
        print("✅ Connexion TCP réussie !")
        
        # Envoyer des logs de test avec différents niveaux
        # Format TIMESTAMP_ISO8601 : YYYY-MM-DDTHH:mm:ssZ
        test_logs = [
            f"{generate_iso8601_timestamp(0)}: [INFO] Babylove parle de manger\n",
            f"{generate_iso8601_timestamp(1)}: [DEBUG] Babylove ne dit rien\n",
            f"{generate_iso8601_timestamp(2)}: [WARN] Babylove râle\n",
            f"{generate_iso8601_timestamp(3)}: [ERROR] Babylove pleure\n"
        ]
        
        for i, log in enumerate(test_logs, 1):
            sock.send(log.encode('utf-8'))
            print(f"✅ Log {i} envoyé: {log.strip()}")
            time.sleep(0.5)  # Délai entre les messages
        
        # Fermer la connexion
        sock.close()
        print("✅ Test terminé avec succès")
        
    except socket.timeout:
        print("❌ Timeout de connexion")
    except ConnectionRefusedError:
        print("❌ Connexion refusée - Logstash n'écoute pas sur le port 50000")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_log_level()