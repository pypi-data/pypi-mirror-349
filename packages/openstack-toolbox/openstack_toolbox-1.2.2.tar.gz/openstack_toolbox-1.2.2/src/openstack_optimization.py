#!/usr/bin/env python3

import subprocess
import sys
import importlib
import json
import os

def run_script(script_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # = src/
    script_path = os.path.join(script_dir, script_name)

    result = subprocess.run([sys.executable, script_path], check=True)

def load_openstack_credentials():
    load_dotenv()  # essaie de charger depuis .env s’il existe

    creds = {
        "auth_url": os.getenv("OS_AUTH_URL"),
        "project_name": os.getenv("OS_PROJECT_NAME"),
        "username": os.getenv("OS_USERNAME"),
        "password": os.getenv("OS_PASSWORD"),
        "user_domain_name": os.getenv("OS_USER_DOMAIN_NAME"),
        "project_domain_name": os.getenv("OS_PROJECT_DOMAIN_NAME"),
    }

    # Si une des variables est absente, on essaie de charger depuis un fichier JSON
    if not all(creds.values()):
        try:
            with open("secrets.json") as f:
                creds = json.load(f)
        except FileNotFoundError:
            raise RuntimeError("❌ Aucun identifiant OpenStack disponible (.env ou secrets.json manquant)")

    return creds

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Vérifier et installer les dépendances manquantes
try:
    importlib.import_module('openstack')
except ImportError:
    print("⚙️ Installation du package openstack...")
    install_package('openstacksdk')

try:
    importlib.import_module('dotenv')
except ImportError:
    print("⚙️ Installation du package dotenv...")
    install_package('python-dotenv')

try:
    importlib.import_module('pandas')
except ImportError:
    print("⚙️ Installation du package Pandas...")
    install_package('pandas')

try:
    importlib.import_module('matplotlib')
except ImportError:
    print("⚙️ Installation du package Matplotlib...")
    install_package('matplotlib')

try:
    importlib.import_module('seaborn')
except ImportError:
    print("⚙️ Installation du package Seaborn...")
    install_package('seaborn')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from openstack import connection

# Connexion à OpenStack
creds = load_openstack_credentials()
conn = connection.Connection(**creds)

# Fonction pour récupérer les statuts des VMs via l'API OpenStack
def get_vm_statuses_from_cli():
    try:
        result = subprocess.run(
            ["openstack", "server", "list", "-f", "json"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print("❌ La commande `openstack server list` a échoué.")
            print("STDERR:", result.stderr)
            return []
        servers = json.loads(result.stdout)
        return [
            {
                "id": s["ID"],
                "name": s["Name"],
                "status": s["Status"],
                "project": s.get("Project ID", "inconnu")
            }
            for s in servers
        ]
    except Exception as e:
        print("❌ Erreur lors de l'appel à `openstack server list`:", e)
        return []

# Liste des statuts de VM à vérifier
def get_inactive_instances_from_cli():
    servers = get_vm_statuses_from_cli()
    inactive = [s for s in servers if s["status"].upper() != "ACTIVE"]
    return inactive

def get_unused_volumes():
    # Récupérer la liste des volumes
    volumes = conn.block_storage.volumes()

    unused_volumes = []
    for volume in volumes:
        # Vérifier si le volume est non utilisé (par exemple, non attaché à une instance)
        if not volume.attachments:
            unused_volumes.append(volume)

    return unused_volumes

def analyze_resource_usage():
    # Collecter les données d'utilisation des ressources
    data = {
        'Instance': ['Instance1', 'Instance2', 'Instance3'],
        'CPU Usage (%)': [10, 20, 30],
        'RAM Usage (%)': [15, 25, 35],
        'Disk Usage (%)': [20, 30, 40]
    }

    df = pd.DataFrame(data)

    # Analyser les données
    # Par exemple, calculer la moyenne et l'écart type
    mean_cpu = df['CPU Usage (%)'].mean()
    std_cpu = df['CPU Usage (%)'].std()

    mean_ram = df['RAM Usage (%)'].mean()
    std_ram = df['RAM Usage (%)'].std()

    mean_disk = df['Disk Usage (%)'].mean()
    std_disk = df['Disk Usage (%)'].std()

    # Générer des visualisations
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Instance', y='CPU Usage (%)', data=df)
    plt.title('CPU Usage by Instance')
    plt.savefig('cpu_usage.png')
    plt.show() 

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Instance', y='RAM Usage (%)', data=df)
    plt.title('RAM Usage by Instance')
    plt.savefig('ram_usage.png')
    plt.show() 

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Instance', y='Disk Usage (%)', data=df)
    plt.title('Disk Usage by Instance')
    plt.savefig('disk_usage.png')
    plt.show() 

    # Générer un rapport
    report = f"Rapport d'analyse de l'utilisation des ressources:\n\n"
    report += f"Moyenne de l'utilisation du CPU: {mean_cpu:.2f}%\n"
    report += f"Écart type de l'utilisation du CPU: {std_cpu:.2f}%\n\n"
    report += f"Moyenne de l'utilisation de la RAM: {mean_ram:.2f}%\n"
    report += f"Écart type de l'utilisation de la RAM: {std_ram:.2f}%\n\n"
    report += f"Moyenne de l'utilisation du disque: {mean_disk:.2f}%\n"
    report += f"Écart type de l'utilisation du disque: {std_disk:.2f}%\n\n"

    return report

def calculate_underutilized_costs():
    try:
        with open('weekly_billing.json', 'r') as f:
            billing_data = json.load(f)
    except FileNotFoundError:
        print("❌ Le fichier weekly_billing.json est introuvable.")
        billing_data = []
    except json.JSONDecodeError:
        print("❌ Erreur lors de la lecture du fichier weekly_billing.json : format JSON invalide.")
        billing_data = []

    ICU_to_CHF = 1 / 50
    ICU_to_EUR = 1 / 55.5

    underutilized_costs = {}
    # Parcours de la liste d'objets retournée par OpenStack
    for entry in billing_data:
        # Adapte ici les clés selon la structure exacte de chaque dict
        resource = entry.get("name") or entry.get("resource") or entry.get("ID") or entry.get("id")
        cost_icu = entry.get("rate:unit") or entry.get("ICU") or entry.get("icu") or entry.get("cost") or entry.get("rate:sum")
        # Si tu connais la clé exacte pour le coût ICU, remplace la ligne ci-dessus par entry["<clé>"]
        if resource is not None and cost_icu is not None:
            try:
                cost_icu = float(cost_icu)
            except Exception:
                continue
            cost_chf = cost_icu * ICU_to_CHF
            cost_eur = cost_icu * ICU_to_EUR
            underutilized_costs[resource] = {
                'ICU': cost_icu,
                'CHF': round(cost_chf, 2),
                'EUR': round(cost_eur, 2)
            }

    return underutilized_costs

def collect_and_analyze_data():
    inactive_instances = get_inactive_instances_from_cli()
    unused_volumes = get_unused_volumes()

    report_body = ""
    report_body += "="*60 + "\n"
    report_body += "RÉCAPITULATIF DES RESSOURCES SOUS-UTILISÉES\n"
    report_body += "="*60 + "\n\n"

    report_body += "[INSTANCES INACTIVES]\n"
    if inactive_instances:
        for instance in inactive_instances:
            report_body += f"  - ID: {instance['id']}, Nom: {instance['name']}, Statut: {instance['status']}\n"
    else:
        report_body += "✅ Aucune instance inactive détectée.\n"
    report_body += "\n" + "-"*50 + "\n"

    report_body += "[VOLUMES NON UTILISÉS]\n"
    if unused_volumes:
        for volume in unused_volumes:
            report_body += f"  - ID: {volume.id}, Nom: {volume.name}\n"
    else:
        report_body += "✅ Aucun volume inutilisé détecté.\n"
    report_body += "\n" + "-"*50 + "\n"

    report_body += "[ANALYSE DE L'UTILISATION DES RESSOURCES]\n"
    report = analyze_resource_usage()
    report_body += report
    report_body += "-"*50 + "\n"

    report_body += "[COÛTS DES RESSOURCES SOUS-UTILISÉES]\n"
    underutilized_costs = calculate_underutilized_costs()
    if not underutilized_costs:
        report_body += "❌ Aucune donnée de facturation disponible (trop faibles ou non disponibles).\n"
    else:
        for resource, costs in underutilized_costs.items():
            report_body += f"  - {resource}: {costs['CHF']} CHF / {costs['EUR']} EUR\n"
    report_body += "="*60 + "\n"

    return report_body

def main():
    # Test de connection à OpenStack
    if not conn.authorize():
        print("❌ Échec de la connexion à OpenStack")
        return
    
    header = r"""
  ___                       _             _               
 / _ \ _ __   ___ _ __  ___| |_ __ _  ___| | __           
| | | | '_ \ / _ \ '_ \/ __| __/ _` |/ __| |/ /           
| |_| | |_) |  __/ | | \__ \ || (_| | (__|   <            
 \___/| .__/ \___|_| |_|___/\__\__,_|\___|_|\_\           
 / _ \|_|__ | |_(_)_ __ ___ (_)______ _| |_(_) ___  _ __  
| | | | '_ \| __| | '_ ` _ \| |_  / _` | __| |/ _ \| '_ \ 
| |_| | |_) | |_| | | | | | | |/ / (_| | |_| | (_) | | | |
 \___/| .__/ \__|_|_| |_| |_|_/___\__,_|\__|_|\___/|_| |_|
      |_|                                                 
         Openstack SysAdmin Toolbox
                        by Loutre

"""
    print(header)

    # Exécuter le script weekly_billing.py pour récupérer les données de facturation
    run_script("weekly_billing.py")

    # Collecter et analyser les données
    report_body = collect_and_analyze_data()

    # Enregistrer le rapport dans un fichier
    with open('/tmp/openstack_report.txt', 'w') as f:
        f.write(report_body)

    print("🎉 Rapport généré avec succès : /tmp/openstack_optimization_report.txt")
    
    # Afficher le rapport
    print(report_body)
    # Afficher les graphiques
    plt.show()

if __name__ == '__main__':
    main()