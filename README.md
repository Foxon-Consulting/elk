# 🐘 ELK Stack - Docker Compose Setup

Un environnement de développement complet pour la stack ELK (Elasticsearch, Logstash, Kibana) avec une application de test intégrée et des options de configuration flexibles.

## 🏗️ Architecture du Projet

```
docker-elk/
├── elk/                    # Stack ELK principal
│   ├── elasticsearch/      # Configuration Elasticsearch
│   ├── logstash/          # Configuration Logstash
│   ├── kibana/            # Configuration Kibana
│   ├── docker-compose.yml # Orchestration des services ELK
│   └── test_logs.py       # Script de test des logs
├── test-app/              # Application de test avec sidecar
│   ├── docker-compose.yml # Orchestration de l'app de test
│   ├── filebeat-config/   # Configuration Filebeat
│   ├── metricbeat-config/ # Configuration Metricbeat
│   └── logs/              # Volume partagé des logs
└── README.md              # Ce fichier
```

## 🚀 Démarrage Rapide

### 1. Configuration Initiale d'Elasticsearch

```bash
# Démarrer le service de configuration initiale
cd elk
docker-compose --profile=setup up -d setup
```

**⚠️ Important :** Ce service ne doit être exécuté qu'une seule fois lors de la première initialisation. Il configure les utilisateurs et rôles de base.

### 2. Démarrage de la Stack ELK

```bash
# Démarrer Elasticsearch, Logstash et Kibana
docker-compose up -d
```

### 3. Accès à Kibana

Ouvrez votre navigateur et allez sur : **https://localhost:5601**

## 🧪 Application de Test

### Démarrage de l'Application de Test

```bash
# Aller dans le répertoire test-app
cd test-app

# Démarrer l'application de test avec Filebeat
docker-compose up -d
```

L'application de test :
- 🕐 Génère des logs en continu avec la bonne timezone (Europe/Paris)
- 📝 Crée des logs avec différents niveaux (INFO, DEBUG, WARN, ERROR)
- 🔄 Met à jour le fichier `logs/app.log` toutes les 3 secondes
- 🐳 Utilise un sidecar Filebeat pour collecter les logs

### Structure des Logs Générés

```
2025-08-24 19:36:37: [INFO] Application de test démarrée
2025-08-24 19:36:37: [DEBUG] Génération de logs de test
2025-08-24 19:36:37: [INFO] Test de performance en cours...
2025-08-24 19:36:37: [WARN] Attention: log de test
```

## 🔧 Configuration

### Configuration Filebeat

Le sidecar Filebeat est configuré pour :
- 📁 Surveiller le répertoire `/var/log/app/*.log`
- 🏷️ Ajouter des champs personnalisés :
  - `app: "test-app"`
  - `environment: "development"`
  - `component: "application"`
  - `log_type: "app"`
- 📤 Envoyer les logs vers Logstash sur le port 5044

### Configuration Logstash

Logstash traite les logs avec :
- 🔍 **Parsing Grok** : Extraction des timestamps et niveaux de log
- 🕐 **Conversion de timezone** : Support ISO8601
- 🏷️ **Enrichissement** : Ajout de métadonnées et champs personnalisés
- 🎯 **Logique métier** : Champs "babylove" basés sur le niveau de log
- 📊 **Sortie** : Indexation dans Elasticsearch + debug stdout

## 🎯 Options de Configuration Avancées

### Alternative : Pipeline d'Ingestion Elasticsearch

Au lieu d'utiliser Logstash, vous pouvez configurer Filebeat pour envoyer directement vers Elasticsearch avec un pipeline d'ingestion personnalisé :

1. **Créer le pipeline d'ingestion** :
   ```bash
   # Utiliser le fichier ingest-pipeline.http avec Postman
   # ou curl pour créer le pipeline dans Elasticsearch
   ```

2. **Modifier la configuration Filebeat** :
   ```yaml
   # Commenter la section Logstash
   # output.logstash:
   #   hosts: ["elk-logstash:5044"]

   # Décommenter la section Elasticsearch
   output.elasticsearch:
     hosts: ["http://elasticsearch:9200"]
     username: "elastic"
     password: "changeme"
     ssl.verification_mode: none
     pipeline: "custom_timestamp_pipeline"
   ```

## 🧪 Tests et Validation

### Test des Logs

```bash
# Tester l'envoi de logs via TCP vers Logstash
cd elk
python test_logs.py
```

### Vérification des Données

```bash
# Vérifier le nombre de documents indexés
curl "http://localhost:9200/logs-*/_count?pretty"

# Rechercher des logs spécifiques
curl "http://localhost:9200/logs-*/_search?q=app:test-app&pretty"
```

## 🌐 Ports et Accès

| Service | Port | Description |
|---------|------|-------------|
| Elasticsearch | 9200 | API REST |
| Elasticsearch | 9300 | Transport |
| Logstash | 5044 | Beats Input |
| Logstash | 50000 | TCP Input |
| Logstash | 9600 | API HTTP |
| Kibana | 5601 | Interface Web |

## 🔍 Monitoring et Debug

### Logs des Services

```bash
# Logs Logstash
docker-compose logs logstash

# Logs Filebeat
cd test-app
docker-compose logs filebeat-sidecar

# Logs de l'application de test
docker-compose logs test-app
```

### Vérification de la Connectivité

```bash
# Test de la connexion Elasticsearch
curl "http://localhost:9200/_cluster/health?pretty"

# Test de la connexion Kibana
curl "http://localhost:5601/api/status"
```

## 🚨 Dépannage

### Problèmes Courants

1. **Filebeat ne peut pas se connecter à Logstash** :
   - Vérifier que les deux services utilisent le même réseau Docker
   - Utiliser `elk-logstash:5044` comme nom d'hôte

2. **Problèmes de timezone** :
   - Vérifier la variable `TZ=Europe/Paris` dans docker-compose.yml
   - Redémarrer les conteneurs après modification

3. **Elasticsearch ne démarre pas** :
   - Vérifier l'espace disque disponible
   - Vérifier les permissions des volumes

## 📚 Ressources

- [Documentation Elasticsearch](https://www.elastic.co/guide/index.html)
- [Documentation Logstash](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Documentation Kibana](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Documentation Filebeat](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)

## 🤝 Contribution

Ce projet est configuré pour un environnement de développement. Pour la production, assurez-vous de :
- 🔐 Configurer la sécurité Elasticsearch
- 📊 Ajuster les paramètres de performance
- 🚀 Configurer la persistance des données
- 📝 Documenter les procédures de sauvegarde

---

**Note** : Ce projet utilise Docker Compose pour la simplicité. Pour un environnement Podman, remplacez `docker-compose` par `podman-compose` dans toutes les commandes.
