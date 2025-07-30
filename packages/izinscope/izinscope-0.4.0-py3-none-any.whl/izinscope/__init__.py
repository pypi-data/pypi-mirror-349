#!/usr/bin/env python3
import argparse
import ipaddress
import socket
import datetime
import sys
import os
from concurrent.futures import ThreadPoolExecutor
import dns.resolver

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"



def log(msg, logfile=None):
    if not ONLY_DOMAIN:
        print(msg)
    if logfile:
        logfile.write(msg + "\n")

# Résout A/AAAA pour un domaine
def resolve_domain(domain, resolver):
    ips = set()
    for record in ['A', 'AAAA']:
        try:
            answers = resolver.resolve(domain, record)
            for rdata in answers:
                ips.add(rdata.to_text())
        except dns.resolver.NoAnswer:
            continue
        except Exception:
            continue
    return domain, list(ips)

# Charge un fichier de scope et renvoie:
# - liste de tuples (network_obj, entry, filename)
# - dict mapping ip -> list of (entry, filename)
def load_scope(scope_file):
    # Accept both `str` and `pathlib.Path` inputs.  Convert once to a plain
    # string so that internal data structures always contain the same type
    # (this helps comparisons in tests that expect a `str`).
    scope_file_str = os.fspath(scope_file)
    networks = []
    ips_map = {}
    with open(scope_file_str, 'r') as f:
        for line in f:
            entry = line.strip()
            if not entry:
                continue
            try:
                net = ipaddress.ip_network(entry, strict=False)
                networks.append((net, entry, scope_file_str))
            except ValueError:
                try:
                    resolved = socket.gethostbyname_ex(entry)[2]
                    for ip in resolved:
                        ips_map.setdefault(ip, []).append((entry, scope_file_str))
                except Exception as e:
                    log(f"Erreur résolution '{entry}' dans {scope_file_str}: {e}")
    return networks, ips_map

# Vérifie un domaine ou une IP unique
# Affiche détails et fichier source

def single_check(target, networks, ips_map):

    # On vérifie explicitement si la cible est une IP ou un domaine, sans supposer quoi que ce soit en cas d'échec de résolution
    try:
        ipaddress.ip_address(target)
        # Si aucune exception, c'est une IP
        resolved_ips = [target]
    except ValueError:
        # Ce n'est pas une IP, on tente de résoudre comme domaine
        try:
            resolved_ips = socket.gethostbyname_ex(target)[2]
        except socket.gaierror:
            resolved_ips = []

    # Collecte des correspondances
    matches = []
    for ip in resolved_ips:
        ip_obj = ipaddress.ip_address(ip)
        for net, entry, fname in networks:
            if ip_obj in net:
                matches.append((ip, entry, fname))
        if ip in ips_map:
            for entry, fname in ips_map[ip]:
                matches.append((ip, entry, fname))

    # Avant d'afficher , on répond f"{RED}[-]{RESET} {target} : Aucune IP résolue."
    if not matches:
        log(f"{RED}[-]{RESET} {target} : Aucune IP résolue.")
        return
    if matches:
        print(f"{GREEN}[+]{RESET} {target} résout vers:")
        for idx, (ip, entry, fname) in enumerate(matches):
            char = "├─" if idx < len(matches) - 1 else "└─"
            log(f" {char} {ip} -> {entry} ({os.path.basename(fname)})")
    else:
        # Affiche toutes les IPs trouvées en rouge
        red_list = ", ".join([f"{RED}{ip}{RESET}" for ip in resolved_ips])
        log(f"{RED}[-]{RESET} {target} : [{red_list}]")
    return

# Écrit les résultats dans un fichier (txt ou csv)
def write_output(filename, data, csv=False):
    with open(filename, 'w', encoding='utf-8') as f:
        if csv:
            f.write("domain,ip,entry,file\n")
            for domain, matches in data.items():
                for ip, entry, fname in matches:
                    f.write(f"{domain},{ip},{entry},{os.path.basename(fname)}\n")
        else:
            # On écrit le domaine unique par ligne
            for domain, matches in data.items():
                ips_only = [ip for ip, _, _ in matches]
                f.write(domain+ "\n")


def main():
    parser = argparse.ArgumentParser(description="Izinscope : Check IP/domain vs scope")
    parser.add_argument(
        "-s", "--scope", required=True,
        action='append',
        help="Fichier ou dossier de scope (CIDR/IP/domaines). Peut être utilisé plusieurs fois"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--domains-to-check", help="Fichier domaines à vérifier")
    group.add_argument("-i", "--single-check", help="Domaine ou IP unique à vérifier")
    parser.add_argument("--debug", action="store_true", help="Mode debug (logs détaillés)")
    parser.add_argument("-oT", "--output-txt", help="Sortie txt (domaines uniquement)")
    parser.add_argument("-oC", "--output-csv", help="Sortie csv (domaine,ip,entry,file)")
    parser.add_argument("-V",'--version', action='version', version='izinscope 0.4.0')
    # stdout options for only domain --only-domain
    parser.add_argument("-od",'--only-domain', action='store_true', help="Afficher uniquement les domaines dans la sortie")

    

    args = parser.parse_args()
    global ONLY_DOMAIN
    ONLY_DOMAIN = args.only_domain
    # Expansion des scopes: fichiers et dossiers
    scope_files = []
    for path in args.scope:
        if os.path.isdir(path):
            for entry in sorted(os.listdir(path)):
                full = os.path.join(path, entry)
                if os.path.isfile(full):
                    scope_files.append(full)
        else:
            scope_files.append(path)

    # Charger et cumuler tous les scopes
    allowed_networks = []
    allowed_ips_map = {}
    for scope_file in scope_files:
        nets, ips = load_scope(scope_file)
        allowed_networks.extend(nets)
        for ip, entries in ips.items():
            allowed_ips_map.setdefault(ip, []).extend(entries)

    logfile = None
    if args.debug:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        logfile = open(f"log_izinscope_{timestamp}.log", 'w', encoding='utf-8')

    resolver = dns.resolver.Resolver()
    resolver.timeout = 3
    resolver.lifetime = 3

    if args.single_check:
        single_check(args.single_check, allowed_networks, allowed_ips_map)
        return

    with open(args.domains_to_check, 'r', encoding='utf-8') as f:
        targets = [l.strip() for l in f if l.strip()]

    inscope_results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        for domain, ips in executor.map(lambda d: resolve_domain(d, resolver), targets):
            if not ips:
                log(f"{RED}[-]{RESET} {domain} : Aucune IP résolue.", logfile)
                continue

            matches_for_domain = []
            colored_ips = []
            for ip in ips:
                ip_obj = ipaddress.ip_address(ip)
                descs = []
                for net, entry, fname in allowed_networks:
                    if ip_obj in net:
                        descs.append((ip, entry, fname))
                if ip in allowed_ips_map:
                    for entry, fname in allowed_ips_map[ip]:
                        descs.append((ip, entry, fname))
                if descs:
                    colored_ips.append(f"{GREEN}{ip}{RESET}")
                    matches_for_domain.extend(descs)
                else:
                    colored_ips.append(f"{RED}{ip}{RESET}")

            prefix = f"{GREEN}[+]{RESET}" if matches_for_domain else f"{RED}[-]{RESET}"
            log(f"{prefix} {domain} : [{', '.join(colored_ips)}]", logfile)

            # Affichage détaillé pour -d comme pour -i
            if matches_for_domain:
                for idx, (ip, entry, fname) in enumerate(matches_for_domain):
                    char = "├─" if idx < len(matches_for_domain) - 1 else "└─"
                    log(f" {char} {ip} -> {entry} ({os.path.basename(fname)})")
                inscope_results[domain] = matches_for_domain
            else:
                # Affiche toutes les IPs trouvées en rouge
                red_list = ", ".join([f"{RED}{ip}{RESET}" for ip in ips])
                log(f"{RED}[-]{RESET} {domain} : [{red_list}]")

    # Sortie CSV : domaine,ip,entry,file
    if args.output_csv:
        write_output(args.output_csv, inscope_results, csv=True)
        log(f"Fichier CSV '{args.output_csv}' créé.", logfile)

    # Sortie TXT : domaines uniques
    if args.output_txt:
        write_output(args.output_txt, inscope_results, csv=False)
        log(f"Fichier TXT '{args.output_txt}' créé.", logfile)

    if args.only_domain:
        for domain, matches in inscope_results.items():
            print(domain)

    if logfile:
        logfile.close()

if __name__ == "__main__":
    main()
