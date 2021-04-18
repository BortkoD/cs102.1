import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    content = data.decode()
    header = f"{fmt} {len(content)}\0"
    store = header + content
    hash = hashlib.sha1(store.encode()).hexdigest()
    if write:
        new_dir = hash[0:2]
        new_file = hash[2:len(hash)]
        dir = pathlib.Path(".").absolute()
        git_dir = os.environ.get('GIT_DIR', default='.pyvcs')
        os.makedirs(dir / git_dir / "objects" / new_dir, exist_ok=True)
        with open(dir / git_dir / "objects" / new_dir / new_file, 'wb') as file:
            file.write(zlib.compress(store.encode()))
    return hash

def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    # PUT YOUR CODE HERE
    ...


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    ...


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
