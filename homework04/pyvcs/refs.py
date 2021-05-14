import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    # PUT YOUR CODE HERE
    with open(gitdir / ref, "w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    ...


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    # PUT YOUR CODE HERE
    if refname == "HEAD":
        with open(gitdir / refname, "r") as f:
            ref = f.read().split(" ")[1].rstrip("\n")
        with open(gitdir / ref, "r") as f:
            content = f.read()
    else:
        path_to_ref = gitdir / refname
        with open(path_to_ref, "r") as f:
            content = f.read()
    return content


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    # PUT YOUR CODE HERE
    with open(gitdir / "HEAD", "r") as f:
        ref = f.read().split(" ")[1].rstrip("\n")
    if pathlib.Path.exists(gitdir / ref):
        with open(gitdir / ref, "r") as f:
            content = f.read()
        return content
    else:
        return None


def is_detached(gitdir: pathlib.Path) -> bool:
    # PUT YOUR CODE HERE
    with open(gitdir / "HEAD", "r") as f:
        ref = f.read()
    if ref.find("ref:") == -1:
        return True
    else:
        return False


def get_ref(gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    with open(gitdir / "HEAD", "r") as f:
        ref = f.read().split(" ")[1].rstrip("\n")
    return ref
