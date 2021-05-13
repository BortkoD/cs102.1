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
    header = f"{fmt} {len(data)}\0"
    store = header.encode() + data
    hash = hashlib.sha1(store).hexdigest()
    if write:
        new_dir = hash[:2]
        new_file = hash[2:]
        dir = pathlib.Path(".").absolute()
        git_dir = os.environ.get('GIT_DIR', default='.pyvcs')
        os.makedirs(dir / git_dir / "objects" / new_dir, exist_ok=True)
        with open(dir / git_dir / "objects" / new_dir / new_file, 'wb') as file:
            file.write(zlib.compress(store))
    return hash


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    dir = obj_name[:2]
    part_of_name = obj_name[2:]
    if len(obj_name) < 4 or len(obj_name) > 40:
        raise Exception(f"Not a valid object name {obj_name}")
    cur_dir = gitdir
    if os.path.exists(cur_dir / "objects" / dir):
        files = list(map(str, sorted(pathlib.Path(cur_dir / "objects" / dir).glob(f"{part_of_name}*"))))
        if len(files) >= 1:
            i = 0
            for name in files:
                name = name.split('/')
                name = name[len(name) - 1]
                files[i] = dir + name
                i += 1
            return files
        else:
            raise Exception(f"Not a valid object name {obj_name}")
    else:
        raise Exception(f"Not a valid object name {obj_name}")


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    with open(gitdir / "objects" / sha[:2] / sha[2:], 'rb') as file:
        obj_data = zlib.decompress(file.read())
    fmt = obj_data[:obj_data.find(b" ")].decode()
    content = obj_data[obj_data.find(b"\x00") + 1:]
    return fmt, content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    entries = []
    while data:
        sha_begin = data.index(b"\00")
        mode: bytes
        name: bytes
        mode, name = data[:sha_begin].split(b" ")
        sha = data[sha_begin + 1 : sha_begin + 21]
        data = data[sha_begin + 21 :]
        entries.append((int(mode.decode()), name.decode(), sha.hex()))
    return entries


def cat_file(obj_name: str, pretty: bool = True) -> None:
    git_dir = pathlib.Path(os.environ.get('GIT_DIR', default='.pyvcs'))
    fmt, content = read_object(obj_name, git_dir)
    result = ""
    if fmt == "blob" or fmt == "commit":
        result = content.decode()
    else:
        entries = read_tree(content)
        for entry in entries:
            result += f"{str(entry[0]).zfill(6)} {read_object(entry[2], git_dir)[0]} {entry[2]}\t{entry[1]}\n"
    print(result)


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
