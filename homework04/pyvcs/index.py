import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        # PUT YOUR CODE HERE
        return struct.pack(f"!10l 20s H {len(self.name)}s {8 - ((len(self.name) + 62) % 8)}x",
                           self.ctime_s,
                           self.ctime_n,
                           self.mtime_s,
                           self.mtime_n,
                           self.dev,
                           self.ino & 0xFFFFFFFF,
                           self.mode,
                           self.uid,
                           self.gid,
                           self.size,
                           self.sha1,
                           self.flags,
                           self.name.encode())

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        # PUT YOUR CODE HERE
        unpacked_data = list(struct.unpack(f"!10l 20s H {len(data[62:])}s", data))
        unpacked_data[-1] = unpacked_data[-1].strip(b'\x00').decode()
        return GitIndexEntry(*unpacked_data)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    # PUT YOUR CODE HERE
    index = []
    if os.path.exists(gitdir / "index"):
        file = open(gitdir / "index", 'rb')
        data_from_file = file.read()
        count_of_entries = struct.unpack('!L', data_from_file[8:12])[0]
        start_pos = 12
        for i in range(count_of_entries):
            end_pos = start_pos + 62 + data_from_file[start_pos + 62:].find(b'\x00')
            index.append(GitIndexEntry.unpack(data_from_file[start_pos:end_pos]))
            start_pos = end_pos + (8 - ((62 + len(index[i].name)) % 8))
    return index


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    index = bytes()
    num_of_version = 2
    index = b'DIRC' + struct.pack('!L', num_of_version) + struct.pack('!L', len(entries))
    for i in entries:
        index = index + GitIndexEntry.pack(i)
    sha = struct.pack('!20s', hashlib.sha1(index).digest())
    index = index + sha
    with open(gitdir / "index", 'wb') as file:
        file.write(index)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    files_data = read_index(gitdir)
    for i in files_data:
        if details:
            rights = "{:6o}".format(i.mode)
            stage = (i.flags >> 12) & 3
            print(rights, ' ', i.sha1.hex(), ' ', stage, '\t', i.name, sep='', end='\n')
        else:
            print(i.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    # PUT YOUR CODE HERE
    cur_index = read_index(gitdir)
    paths = sorted(paths)
    for i in paths:
        with open(i, 'r') as file:
            data = file.read().encode()
        hash = hash_object(data, fmt="blob", write=True)
        cur_index.append(GitIndexEntry(ctime_s=int(os.stat(i).st_ctime),
                       ctime_n=0,
                       mtime_s=int(os.stat(i).st_mtime),
                       mtime_n=0,
                       dev=int(os.stat(i).st_dev),
                       ino=int(os.stat(i).st_ino),
                       mode=int(os.stat(i).st_mode),
                       uid=int(os.stat(i).st_uid),
                       gid=int(os.stat(i).st_gid),
                       size=int(os.stat(i).st_size),
                       sha1=bytes.fromhex(hash),
                       flags=7,
                       name = str(i)))
    cur_index = sorted(cur_index, key=lambda x: x.name)

    if write:
        write_index(gitdir, cur_index)