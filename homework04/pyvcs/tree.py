import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    # PUT YOUR CODE HERE
    content = b""
    for entry in index:
        if "/" in entry.name:
            dir_name = entry.name[:entry.name.find("/")]
            child_content = oct(entry.mode)[2:].encode() + b" "
            child_content += entry.name[entry.name.find("/") + 1:].encode() + b"\0"
            child_content += entry.sha1
            mode = b"40000 "
            name = dir_name.encode() + b"\0"
            sha1 = bytes.fromhex(hash_object(child_content, "tree", True))
        else:
            mode = oct(entry.mode)[2:].encode() + b" "
            name = entry.name.encode() + b"\0"
            sha1 = entry.sha1
        content += mode + name + sha1
    result = hash_object(content, "tree", write=True)
    return result

def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    # PUT YOUR CODE HERE
    ...
