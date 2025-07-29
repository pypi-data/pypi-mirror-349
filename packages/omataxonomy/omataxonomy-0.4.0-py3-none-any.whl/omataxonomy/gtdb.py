import numpy
import csv
import re
import gzip
import logging
from hashlib import md5

logger = logging.getLogger(__name__)

GTDB_DOWNLOAD_BASE_URL = "https://data.ace.uq.edu.au/public/gtdb/data/releases"
PREFIX_2_RANK = {"d__": "superkingdom", "p__": "phylum", "c__": "class", "o__": "order",
                 "f__": "family", "g__": "genus", "s__": "species"}


def _load_meta(fn):
    _open = gzip.open if fn.endswith('.gz') else open
    with _open(fn, 'rt', newline="") as fh:
        reader = csv.DictReader(fh, dialect="excel-tab")
        meta = {row['accession']: row for row in reader}
    return meta


def build_tax_dump(meta_fn):
    meta = _load_meta(meta_fn)
    with open("gtdbnodes.dmp", "at") as nodes_dump, open("gtdbnames.dmp", "at") as names_dump:
        write_dump_files(meta, nodes_dump, names_dump)


def hash_to_int(val):
    h = md5(str(val).encode('utf-8'))
    return -abs(int(numpy.frombuffer(h.digest()[:4], dtype='i4')[0]))


def write_dump_files(meta, node_dump, names_dump):

    def write_node(taxid, parent_taxid, rank, is_ref=False):
        # tax_id					-- node id in GenBank omataxonomy database
        # parent tax_id				-- parent node id in GenBank omataxonomy database
        # rank					-- rank of this node (superkingdom, kingdom, ...)
        # embl code				-- locus-name prefix; not unique
        # division id				-- see division.dmp file
        # inherited div flag  (1 or 0)		-- 1 if node inherits division from parent
        # genetic code id				-- see gencode.dmp file
        # inherited GC  flag  (1 or 0)		-- 1 if node inherits genetic code from parent
        # mitochondrial genetic code id		-- see gencode.dmp file
        # inherited MGC flag  (1 or 0)		-- 1 if node inherits mitochondrial gencode from parent
        # GenBank hidden flag (1 or 0)            -- 1 if name is suppressed in GenBank entry lineage
        # hidden subtree root flag (1 or 0)       -- 1 if this subtree has no sequence data yet
        # comments				-- free-text comments and citations
        ### additional fields
        #  is_reference_genome (1 or 0)    -- 1 if it is the reference genome of a species
        is_ref = 1 if is_ref else 0
        nodes_buffer = [taxid, parent_taxid, rank, "XX", 0, 0, 11, 1, 1, 0, (0 if rank is not None else 1),
                        0, "", is_ref]
        node_dump.write("\t|\t".join(map(str, nodes_buffer)) + "\n")

    def write_name(taxid, name, key):
        if name is None:
            return
        buf = [taxid, name, "", key]
        names_dump.write("\t|\t".join(map(str, buf)) + "\n")

    acc_re = re.compile(r"[RSGB]{2}_GC[AF]_(?P<acc>\d+)\.\d+")
    lev2id = {}
    for genome_acc, genome_meta in meta.items():
        lineage = genome_meta['gtdb_taxonomy'].split(';')
        parent = 1
        for lev in lineage:
            if not lev in lev2id:
                taxid = hash_to_int(lev)
                rank = PREFIX_2_RANK[lev[:3]]
                write_node(taxid, parent, rank)
                write_name(taxid, lev, "scientific name")
                write_name(taxid, lev[3:], "common_name")
                lev2id[lev] = taxid
            parent = lev2id[lev]
        # add the genome itself
        m = acc_re.match(genome_acc)
        assert m is not None
        taxid = hash_to_int(m.group('acc'))
        is_ref = genome_meta["gtdb_genome_representative"] == genome_acc
        write_node(taxid, parent, rank="subspecies", is_ref=is_ref)
        write_name(taxid, genome_acc, "scientific name")
        write_name(taxid, genome_meta['ncbi_taxid'], 'ncbi_taxid')
        write_name(taxid, genome_meta["ncbi_organism_name"], "ncbi_organism_name")
        write_name(taxid, genome_meta['ncbi_genbank_assembly_accession'], 'ncbi_genbank_assembly_accession')
        common_name = genome_meta['ncbi_organism_name']
        if not common_name.endswith(genome_meta['ncbi_strain_identifiers']):
            common_name += " " + genome_meta['ncbi_strain_identifiers']
        write_name(taxid, common_name, "common_name")


def download_gtdb_release(rel=None, dom=None, target_folder=None):
    from . import cwd
    if dom is None:
        dom = ["ar53", "bac120"]
    if isinstance(dom, str):
        dom = [dom]
    if rel is None:
        rel = "latest"
    if target_folder is not None:
        target_folder = "./"
    with cwd(target_folder):
        for d in dom:
            meta_fn = download_dom(d, rel)
            build_tax_dump(meta_fn)


def download_dom(dom, rel):
    from .build_db import download_file
    logger.info(f"download tax release '{rel}' for '{dom}' from {GTDB_DOWNLOAD_BASE_URL}")
    file = f"{dom}_metadata.tsv.gz"
    url = f"{GTDB_DOWNLOAD_BASE_URL}/{rel}/{file}"
    download_file(url, file)
    return file


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    download_gtdb_release()
