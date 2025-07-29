import os
import pickle
import sqlite3
import sys
import tarfile
import tempfile
import requests
from itertools import chain
from pathlib import Path
from hashlib import md5
from logging import getLogger
from ete4 import Tree
from tqdm import tqdm
from .gtdb import download_gtdb_release
logger = getLogger(__name__)

def load_tree_from_dump(tar):
    parent2child = {}
    name2node = {}
    node2taxname = {}
    synonyms = set()
    name2rank = {}
    node2common = {}
    logger.info("Loading node names...")
    unique_nocase_synonyms = set()
    for line in tar.extractfile("names.dmp"):
        line = str(line.decode())
        fields = [_f.strip() for _f in line.split("|")]
        nodename = fields[0]
        name_type = fields[3].lower()
        taxname = fields[1]

        # Clean up tax names so we make sure the don't include quotes. See https://github.com/etetoolkit/ete/issues/469
        taxname = taxname.rstrip('"').lstrip('"')

        if name_type in ("scientific name", "scientific_name"):
            node2taxname[nodename] = taxname
        if name_type in ("genbank common name", "common_name"):
            node2common[nodename] = taxname
        elif name_type in set(["mnemonic_code", "ncbi_taxid",  "ncbi_organism_name", "genbank equivalent name",
                               "ncbi_genbank_assembly_accession", "anamorph", "genbank synonym", "genbank anamorph",
                               "teleomorph"]):
            if name_type == "ncbi_taxid":
                taxname = f"ncbi_taxid:{taxname}"

            # Keep track synonyms, but ignore duplicate case-insensitive names. See https://github.com/etetoolkit/ete/issues/469
            synonym_key = (nodename, taxname.lower())
            if synonym_key not in unique_nocase_synonyms:
                unique_nocase_synonyms.add(synonym_key)
                synonyms.add((nodename, taxname))

    logger.info(f"{len(node2taxname)} names loaded.")
    logger.info(f"{len(synonyms)} synonyms loaded.")

    logger.info("Loading nodes...")
    for line in tar.extractfile("nodes.dmp"):
        line = str(line.decode())
        fields = line.split("|")
        nodename = fields[0].strip()
        parentname = fields[1].strip()
        n = Tree()
        n.name = nodename
        # n.taxname = node2taxname[nodename]
        n.add_prop('taxname', node2taxname[nodename])
        if nodename in node2common:
            n.add_prop('common_name', node2common[nodename])
        n.add_prop('rank', fields[2].strip())
        if len(fields) > 13:
            n.add_prop("is_ref", fields[13].strip())
        parent2child[nodename] = parentname
        name2node[nodename] = n
    logger.info(f"{len(name2node)} nodes loaded.")

    logger.info("Linking nodes...")
    for node in name2node:
        if node == "1":
            t = name2node[node]
        else:
            parent = parent2child[node]
            parent_node = name2node[parent]
            parent_node.add_child(name2node[node])
    logger.debug("Tree is loaded.")
    return t, synonyms


def generate_table(t, input_folder):
    with open(os.path.join(input_folder, "taxa.tab"), "w") as OUT:
        for j, n in enumerate(t.traverse()):
            if j % 30000 == 0:
                logger.debug(f"{j} generating entries... ")
            temp_node = n
            track = []
            while temp_node:
                temp_rank = temp_node.props.get('rank')
                if temp_rank not in (None, "None"):
                    track.append(temp_node.name)
                temp_node = temp_node.up
            if n.up:
                print('\t'.join(
                    [n.name, n.up.name, n.props.get('taxname', ""),
                     getattr(n, "common_name", n.props.get("common_name", "")),
                     n.props.get('rank', ''),
                     getattr(n, "is_ref", ""),
                     ','.join(track)]
                ), file=OUT)
            else:
                print('\t'.join([n.name, "", n.props.get('taxname', ''),
                                 getattr(n, "common_name", n.props.get("common_name", "")),
                                 n.props.get('rank', ''),
                                 getattr(n, "is_ref", n.props.get('is_ref', '')),
                                 ','.join(track)]
                                ), file=OUT)


def update_db(dbfile, targz_file, remove_tarball=None):
    os.makedirs(os.path.dirname(dbfile), exist_ok=True)
    os.makedirs(os.path.dirname(targz_file), exist_ok=True)
    if not os.path.exists(targz_file):
        build_combined_tarball(targz_file)
        if remove_tarball is None:
            remove_tarball = True
    try:
        tar = tarfile.open(targz_file, 'r')
    except:
        raise ValueError("Please provide taxa dump tar.gz file")

    t, synonyms = load_tree_from_dump(tar)

    prepostorder_lineage = [int(node.name) for post, node in t.iter_prepostorder() if node.props.get('rank') not in (None, "None")]
    with open(dbfile + ".traverse.pkl", "wb") as fh:
        pickle.dump(prepostorder_lineage, fh, 5)

    logger.info("Updating database: %s ..." % dbfile)
    with tempfile.TemporaryDirectory() as tab_dir:
        generate_table(t, tab_dir)

        with open(os.path.join(tab_dir, "syn.tab"), "w") as SYN:
            SYN.write('\n'.join(["%s\t%s" %(v[0],v[1]) for v in synonyms]))

        with open(os.path.join(tab_dir, "merged.tab"), "w") as merged:
            for line in tar.extractfile("merged.dmp"):
                line = str(line.decode())
                out_line = '\t'.join([_f.strip() for _f in line.split('|')[:2]])
                merged.write(out_line+'\n')
        try:
            upload_data(dbfile, tab_dir)
        except:
            raise

    if remove_tarball:
        os.remove(targz_file)


def download_file(url, filepath, chunk_size=8192):
    if filepath is None:
        filepath = url.rsplit('/', 1)[1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, 'wb') as fh:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fh.write(chunk)


def upload_data(dbfile, input_folder):
    from .query import DB_VERSION

    logger.info('Uploading to', dbfile)
    basepath = os.path.split(dbfile)[0]
    if basepath and not os.path.exists(basepath):
        os.mkdir(basepath)

    db = sqlite3.connect(dbfile)

    create_cmd = """
    DROP TABLE IF EXISTS stats;
    DROP TABLE IF EXISTS species;
    DROP TABLE IF EXISTS synonym;
    DROP TABLE IF EXISTS merged;
    CREATE TABLE stats (version INT PRIMARY KEY);
    CREATE TABLE species (taxid INT PRIMARY KEY, 
                          parent INT, 
                          spname VARCHAR(50) COLLATE NOCASE, 
                          common VARCHAR(50) COLLATE NOCASE, 
                          rank VARCHAR(50),
                          mnemonic VARCHAR(5),
                          is_reference BOOLEAN, 
                          track TEXT);
    CREATE TABLE synonym (taxid INT, 
                          spname VARCHAR(50) COLLATE NOCASE, 
                          PRIMARY KEY (spname, taxid));
    CREATE TABLE merged (taxid_old INT, taxid_new INT);
    CREATE INDEX spname1 ON species (spname COLLATE NOCASE);
    CREATE INDEX spname2 ON synonym (spname COLLATE NOCASE);
    CREATE INDEX mnemonic ON species (mnemonic);
    """
    for cmd in create_cmd.split(';'):
        db.execute(cmd)

    db.execute("INSERT INTO stats (version) VALUES (%d);" % DB_VERSION)
    db.commit()

    try:
        with open(os.path.join(input_folder, "syn.tab"), 'rt') as fh:
            for i, line in tqdm(enumerate(fh), desc="inserting synonymes"):
                taxid, spname = line.strip('\n').split('\t')
                db.execute("INSERT INTO synonym (taxid, spname) VALUES (?, ?);", (taxid, spname))
        db.commit()
    except FileNotFoundError:
        logger.warning("no synonym table found. skipping")

    try:
        with open(os.path.join(input_folder, "merged.tab"), "rt") as fh:
            for i, line in tqdm(enumerate(fh), desc="inserting taxid merges"):
                taxid_old, taxid_new = line.strip('\n').split('\t')
                db.execute("INSERT INTO merged (taxid_old, taxid_new) VALUES (?, ?);", (taxid_old, taxid_new))
        db.commit()
    except FileNotFoundError:
        logger.warning("no merged.tab found. skipping")

    with open(os.path.join(input_folder, "taxa.tab"), "rt") as fh:
        for i, line in tqdm(enumerate(fh), desc="inserting taxids"):
            taxid, parentid, spname, common, rank, is_ref, lineage = line.strip('\n').split('\t')
            db.execute("INSERT INTO species (taxid, parent, spname, common, rank, mnemonic, is_reference, track) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                       (taxid, parentid, spname, common, rank, "", is_ref, lineage))
    db.commit()
    update_mnemonic_codes(db)
    logger.info("database created")


def update_mnemonic_codes(db, speclist=None, extra_file=None):
    from omataxonomy.mnemonic import iter_mnemonic_species_codes, iter_extra_mnemonic_species_codes
    db.execute("UPDATE species set mnemonic = ''")
    try:
        for i, (os_code, taxid) in tqdm(enumerate(chain(iter_mnemonic_species_codes(speclist),
                                                  iter_extra_mnemonic_species_codes(extra_file))),
                                        desc="inserting mnemonic codes"):
            try:
                taxid = int(taxid)
                result = db.execute("SELECT syn.taxid FROM synonym as syn JOIN species as sp ON syn.taxid = sp.taxid WHERE syn.spname=? ORDER BY sp.is_reference DESC, syn.taxid DESC", (f"ncbi_taxid:{taxid}",))
                e = result.fetchone()
                if e is not None:
                    taxid = e[0]
                db.execute("UPDATE species SET mnemonic = ? WHERE taxid = ?", (os_code, taxid))
            except ValueError:
                db.execute("UPDATE species SET mnemonic = ? where spname like ?", (os_code, f"%{taxid}%"))
        db.commit()
    except Exception as e:
        logger.exception("update mnemoinc codes failed")
        db.rollback()


def download_ncbi_taxonomy():
    md5_file = "taxdump.tar.gz.md5"
    res = requests.get("https://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz.md5")
    res.raise_for_status()
    md5_check = res.text.split()[0]

    targz_file = Path("taxdump.tar.gz")
    if targz_file.exists():
        with open(targz_file, 'rb') as fh:
            local_md5 = md5()
            while chunk := fh.read(8192):
                local_md5.update(chunk)
        if local_md5.hexdigest() != md5_check:
            download_file("http://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz", targz_file)
    else:
        download_file("http://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz", targz_file)
    return targz_file


def build_combined_tarball(target):
    from . import cwd
    with tempfile.TemporaryDirectory() as dwnfolder:
        with cwd(dwnfolder):
            ncbi_tar = download_ncbi_taxonomy()
            download_gtdb_release(target_folder=dwnfolder)
            with tarfile.open(ncbi_tar, 'r') as tarfh:
                with open(os.path.join(dwnfolder, "names.dmp"), 'wb') as names_fh, \
                     open(os.path.join(dwnfolder, "gtdbnames.dmp"), 'rb') as gtdb_fh:
                    names_fh.write(tarfh.extractfile("names.dmp").read())
                    names_fh.write(gtdb_fh.read())
                with open(os.path.join(dwnfolder, "nodes.dmp"), "wb") as nodes_fh, \
                     open(os.path.join(dwnfolder, "gtdbnodes.dmp"), "rb") as gtdb_fh:
                    nodes_fh.write(tarfh.extractfile("nodes.dmp").read())
                    nodes_fh.write(gtdb_fh.read())
                merged_tinfo = [i for i in tarfh.getmembers() if i.name == "merged.dmp"]
                tarfh.extractall(members=merged_tinfo, path=dwnfolder)

                with tarfile.open(target, 'w:gz') as tarout:
                    tarout.add(os.path.join(dwnfolder, "nodes.dmp"), arcname="nodes.dmp")
                    tarout.add(os.path.join(dwnfolder, "names.dmp"), arcname="names.dmp")
                    tarout.add(os.path.join(dwnfolder, "merged.dmp"), arcname="merged.dmp")
