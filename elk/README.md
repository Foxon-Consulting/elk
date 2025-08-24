# Stack ELK (Elasticsearch, Logstash, Kibana)

Ce projet contient une stack ELK complète et fonctionnelle pour la collecte, le traitement et la visualisation de logs.

## 🏗️ Structure du projet

```
elk/
├── docker-compose.yml          # Configuration Docker Compose
├── elasticsearch/              # Configuration Elasticsearch
├── kibana/                     # Configuration Kibana
├── logstash/                   # Configuration Logstash
├── test_level.py               # Script de test pour Logstash
├── postman.http                # Collection Postman pour tests API
└── README.md                   # Ce fichier
```

## 🚀 Démarrage rapide

### 1. Démarrer la stack
```bash
cd elk
docker-compose up -d
```

### 2. Vérifier les services
```bash
docker-compose ps
```

### 3. Accéder aux interfaces
- **Kibana** : http://localhost:5601
- **Elasticsearch** : http://localhost:9200
- **Logstash API** : http://localhost:9600

## 🔧 Configuration

### Logstash
- **Port Beats** : 5044 (pour Filebeat)
- **Port TCP** : 50000 (pour logs directs)
- **Port API** : 9600 (pour monitoring)

### Pipeline de traitement
- Parse automatiquement les logs au format : `YYYY-MM-DD HH:mm:ss: [LEVEL] Message`
- Extrait le niveau de log dans le champ `log_level`
- Ajoute des champs personnalisés : `environment`, `service`, `pipeline_version`
- Logique spéciale "Babylove" : WARN = "crazy", autres = "contente"

## 🧪 Tests

### Tester Logstash
```bash
python test_level.py
```

### Tester Elasticsearch
```bash
curl http://localhost:9200/_cluster/health
```

## 📊 Visualisation

1. Ouvrir Kibana sur http://localhost:5601
2. Créer un index pattern pour `logs-*`
3. Utiliser Discover pour explorer les logs
4. Créer des dashboards avec le champ `log_level`

## 🛠️ Maintenance

### Redémarrer un service
```bash
docker-compose restart [service_name]
```

### Voir les logs
```bash
docker-compose logs [service_name]
```

### Arrêter la stack
```bash
docker-compose down
```

## 🔍 Dépannage

### Vérifier l'état des services
```bash
docker-compose ps
curl http://localhost:9600/_node  # Logstash
curl http://localhost:9200/_cluster/health  # Elasticsearch
```

### Problèmes courants
- **Logstash ne démarre pas** : Vérifier la syntaxe du pipeline
- **Grok parsing échoue** : Vérifier le format des messages
- **Connexion refusée** : Vérifier que les ports sont ouverts 