import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    dir = pathlib.Path(workdir)
    git_dir = os.environ.get('GIT_DIR', default='.pyvcs')
    if os.path.exists(dir / git_dir):
        return dir / git_dir
    else:
        if git_dir in dir.parts:
            path = pathlib.Path()
            while git_dir in dir.parts:
                path = dir
                dir = dir.parent
            return path
        raise Exception('Not a git repository')

def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    dir = workdir
    git_dir = os.environ.get('GIT_DIR', default='.pyvcs')
    if not os.path.isdir(dir):
        raise Exception(f'{dir} is not a directory')
    os.makedirs(dir / git_dir)
    os.makedirs(dir / git_dir / "refs" / "heads")
    os.makedirs(dir / git_dir / "refs" / "tags")
    os.makedirs(dir / git_dir / "objects")
    with open(dir / git_dir / "HEAD", 'w') as file:
        file.write("ref: refs/heads/master\n")
    with open(dir / git_dir / "config", 'w') as file:
        file.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
    with open(dir / git_dir / "description", 'w') as file:
        file.write("Unnamed pyvcs repository.\n")
    return dir / git_dir
