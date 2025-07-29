#!/usr/bin/env python3

import subprocess
import sys
import importlib
import json
from datetime import datetime
import os

# Fonction pour traduire le nom du flavor
def parse_flavor_name(name):
    """
    Parse un nom de flavor du type 'aX-ramY-diskZ-...' et retourne une chaîne lisible + les valeurs numériques.
    Exemple : 'a2-ram8-disk40' → ('2 vCPU / 8 Go RAM / 40 Go disque', 2, 8, 40)
    """
    try:
        parts = name.split('-')
        cpu_part = next((p for p in parts if p.startswith('a') and p[1:].isdigit()), None)
        ram_part = next((p for p in parts if p.startswith('ram') and p[3:].isdigit()), None)
        disk_part = next((p for p in parts if p.startswith('disk') and p[4:].isdigit()), None)

        cpu = int(cpu_part[1:]) if cpu_part else None
        ram = int(ram_part[3:]) if ram_part else None
        disk = int(disk_part[4:]) if disk_part else None

        human_readable = f"{cpu} CPU / {ram} Go RAM / {disk} Go disque"
        return human_readable, cpu, ram, disk
    except Exception:
        # En cas d'échec, retourne le nom original et None pour les valeurs numériques
        print(f"❌ Échec du parsing pour le flavor '{name}' : {str(e)}")
        return name, None, None, None

# Fonction pour charger les identifiants OpenStack
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

from openstack import connection
from dotenv import load_dotenv

# Connexion à OpenStack
creds = load_openstack_credentials()
conn = connection.Connection(**creds)

# Fonction pour afficher les en-têtes
def print_header(header):
    print("\n" + "=" * 50)
    print(header.center(50))
    print("=" * 50 + "\n")

# Fonction pour obtenir les détails d'un projet spécifique
def get_project_details(conn, project_id):
    print_header(f"DÉTAILS DU PROJET AVEC ID: {project_id}")
    project = conn.identity.get_project(project_id)

    if project:
        print(f"ID: {project.id}")
        print(f"Nom: {project.name}")
        print(f"Description: {project.description}")
        print(f"Domaine: {project.domain_id}")
        print(f"Actif: {'Oui' if project.is_enabled else 'Non'}")
    else:
        print(f"Aucun projet trouvé avec l'ID: {project_id}")

# Fonction pour obtenir les détails d'une instance
def get_billing_data_from_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

# Fonction pour calculer le coût d'une instance
def calculate_instance_cost(billing_data, instance_id=None, icu_to_chf=50, icu_to_euro=55.5):
    if not billing_data:
        return 0.0, 0.0

    total_icu = 0.0

    for group in billing_data:
        resources = group.get("Resources", [])
        for resource in resources:
            desc = resource.get("desc", {})
            resource_id = desc.get("id")
            if instance_id and resource_id != instance_id:
                continue  # ignorer les autres

            try:
                price = float(resource.get("rating", 0))
                total_icu += price
            except (TypeError, ValueError):
                continue

    cost_chf = total_icu / icu_to_chf
    cost_euro = total_icu / icu_to_euro

    return cost_chf, cost_euro

# Fonction pour formater la taille
def format_size(size_bytes):
    # Définir les unités et leurs seuils
    units = [
        ('To', 1000000000000),
        ('Go', 1000000000),
        ('Mo', 1000000),
        ('Ko', 1000)
    ]

    # Parcourir les unités pour trouver la plus appropriée
    for unit, threshold in units:
        if size_bytes >= threshold:
            size = size_bytes / threshold
            return f"{size:.2f} {unit}"
    return f"{size_bytes} octets"

# Lister les images privées et partagées
def list_images(conn):
    print_header("LISTE DES IMAGES UTILISEES")
    # Récupérer les images privées et les convertir en liste
    private_images = list(conn.image.images(visibility='private'))
    # Récupérer les images partagées et les convertir en liste
    shared_images = list(conn.image.images(visibility='shared'))
    # Combiner les images privées et partagées
    all_images = private_images + shared_images

    # Afficher les en-têtes du tableau
    print(f"{'ID':<36} {'Nom':<36} {'Visibilité':<20}")
    print("-" * 96) 
    for image in all_images:
        print(f"{image.id:<36} {image.name:<36} {image.visibility:<20}")

# Lister les instances
def list_instances(conn, billing_data):
    print_header("LISTE DES INSTANCES")
    if not billing_data:
        print("❌ Aucune donnée de facturation disponible (indisponible ou trop faible) — les coûts affichés seront à 0.\n")

    # Récupérer les instances
    instances = list(conn.compute.servers())  

    # Taux de conversion ICU vers monnaies
    icu_to_chf = 50  # Taux de conversion ICU vers CHF
    icu_to_euro = 55.5  # Taux de conversion ICU vers EUR

    # Calculer le coût total des ressources consommées
    total_cost_chf = 0.0
    total_cost_euro = 0.0
    for instance in instances:
        cost_chf, cost_euro = calculate_instance_cost(billing_data, instance_id=instance.id, icu_to_chf=icu_to_chf, icu_to_euro=icu_to_euro)
        total_cost_chf += cost_chf
        total_cost_euro += cost_euro
    
    # Calculer le coût horaire moyen global à partir des données
    rate_values = []
    for group in billing_data:
        for resource in group.get("Resources", []):
            rate = resource.get("rate_value")
            if rate is not None:
                try:
                    rate_values.append(float(rate))
                except ValueError:
                    continue

    if rate_values:
        avg_rate_icu = sum(rate_values) / len(rate_values)
        avg_rate_eur = avg_rate_icu / icu_to_euro
        avg_rate_chf = avg_rate_icu / icu_to_chf

    # Initialiser les totaux
    total_vcpus = 0
    total_ram_go = 0
    total_disk_go = 0

    # Afficher le tableau des instances...
    print(f"{'État':<3} {'ID':<36} {'Nom':<20} {'Flavor ID':<20} {'Uptime':<20} {'Coût (CHF)':>13} {'Coût (EUR)':>13}")
    print("-" * 130)

    for instance in instances:
        try:
            flavor_id = instance.flavor['id']  
            _, cpu, ram, disk = parse_flavor_name(flavor_id)
            
            # Additionner les ressources
            total_vcpus += cpu if cpu else 0
            total_ram_go += ram if ram else 0
            total_disk_go += disk if disk else 0

            # ...reste du code pour l'affichage...
            created_at = datetime.strptime(instance.created_at, "%Y-%m-%dT%H:%M:%SZ")
            uptime = datetime.now() - created_at
            uptime_str = str(uptime).split('.')[0]

            cost_chf, cost_euro = calculate_instance_cost(billing_data, instance_id=instance.id)
            state = instance.status.lower()
            emoji = "🟢" if state == "active" else "🔴"
            
            print(f"{emoji:<3} {instance.id:<36} {instance.name:<20} {flavor_id:<20} {uptime_str:<20} {cost_chf:>13.2f} {cost_euro:>13.2f}")
        
        except Exception as e:
            print(f"❌ Erreur lors du traitement de l'instance '{instance.name}' : {str(e)}")
            continue

    # 4. Afficher le total
    print(f"\n📊 Total des ressources consommées : {total_vcpus} CPU, {total_ram_go} Go de RAM, {total_disk_go} Go de stockage")

    # Afficher le coût total des ressources consommées
    print(f"\n💰 Coût total des ressources consommées : {total_cost_chf:.2f} CHF, {total_cost_euro:.2f} EUR")

    if rate_values:
        print(f"\n💸 Coût horaire moyen : {avg_rate_chf:.5f} CHF, {avg_rate_eur:.5f} EUR")
    else:
        print("\n💸 Coût horaire moyen : Données insuffisantes")

# Lister les snapshots
def list_snapshots(conn):
    print_header("LISTE DES SNAPSHOTS")
    # Récupérer les snapshots
    snapshots = list(conn.block_storage.snapshots())

    # Afficher les en-têtes du tableau
    print(f"{'ID':<36} {'Nom':<20} {'Volume associé':<20}")
    print("-" * 96)
    for snapshot in snapshots:
        print(f"{snapshot.id:<36} {snapshot.name:<20} {snapshot.volume_id:<20}")

# Lister les backups
def list_backups(conn):
    print_header("LISTE DES BACKUPS")
    # Récupérer les backups
    backups = list(conn.block_storage.backups())

    # Afficher les en-têtes du tableau
    print(f"{'ID':<36} {'Nom':<20} {'Volume associé':<20}")
    print("-" * 96)
    for backup in backups:
        print(f"{backup.id:<36} {backup.name:<20} {backup.volume_id:<20}")

# Lister les volumes 
def list_volumes(conn):
    print_header("LISTE DES VOLUMES")
    # Récupérer les volumes
    volumes = list(conn.block_storage.volumes())

    # Afficher les en-têtes du tableau
    print(f"{'ID':<36} {'Nom':<20} {'Taille':>4} {'Type':<10} {'Attaché':<5} {'Snapshot':<12}")
    print("-" * 96)
    for volume in volumes:
        attached = "Oui" if volume.attachments else "Non"
        # Remplacer None par une chaîne vide pour snapshot_id
        snapshot_id = volume.snapshot_id[:6] if volume.snapshot_id else 'Aucun'
        print(f"{volume.id:<36} {volume.name:<20} {volume.size:>4} {volume.volume_type:<10} {attached:<5} {snapshot_id:<12}")

# Récupérer les volumes attachés aux instances
def mounted_volumes(conn):
    instances = conn.compute.servers()
    volumes = conn.block_storage.volumes()
    instance_volumes = {}

    for volume in volumes:
        if volume.attachments:
            for attachment in volume.attachments:
                instance_id = attachment['server_id']
                if instance_id not in instance_volumes:
                    instance_volumes[instance_id] = []
                instance_volumes[instance_id].append(volume)

    tree = {}
    for instance in instances:
        instance_id = instance.id
        instance_name = instance.name
        if instance_id in instance_volumes:
            tree[instance_name] = [volume.name for volume in instance_volumes[instance_id]]
        else:
            tree[instance_name] = []

    return tree

# Afficher l'arborescence
def print_tree(tree):
    for instance, volumes in tree.items():
        print(f"Instance: {instance}")
        for volume in volumes:
            print(f"  Volume: {volume}")

# Lister les IP flottantes
def list_floating_ips(conn):
    print_header("LISTE DES FLOATING IPs")
    # Récupérer les adresses IP flottantes
    floating_ips = list(conn.network.ips())

    # Afficher les en-têtes du tableau
    print(f"{'ID':<36} {'IP':<20} {'Statut':<20}")
    print("-" * 96)
    for ip in floating_ips:
        print(f"{ip.id:<36} {ip.floating_ip_address:<20} {ip.status:<20}")

# Lister les containers
def list_containers(conn):
    print_header("LISTE DES CONTAINERS")
    # Récupérer les containers
    containers = list(conn.object_store.containers())

    # Afficher les en-têtes du tableau
    print(f"{'Nom':<20} {'Taille totale':<20}")
    print("-" * 40)
    for container in containers:
        size_formatted = format_size(container.bytes)
        print(f"{container.name:<20} {size_formatted:<20}")

# Fonction principale
def main():
    # Test de connection à OpenStack
    if not conn.authorize():
        print("❌ Échec de la connexion à OpenStack")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    billing_path = os.path.join(script_dir, 'billing.json')
    billing_data = get_billing_data_from_file(billing_path)

    # Lister les ressources
    list_images(conn)
    list_instances(conn, billing_data)
    list_snapshots(conn)
    list_backups(conn)
    list_volumes(conn)
    print_header("ARBORESCENCE DES VOLUMES")
    tree = mounted_volumes(conn)
    print_tree(tree)
    list_floating_ips(conn)
    list_containers(conn)

if __name__ == "__main__":
    main()