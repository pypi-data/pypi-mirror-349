import os
import pwd


def drop_privileges_to_user(user: str):
    """
    Assuming you are running as root, drop privileges to that of
    the `user` provided

    Args:
        user: the name of the user to drop privileges to
    """
    # nothing to do for non-root users
    if os.getuid() != 0:
        return

    # fetch password database entry for the given user
    pwnam = pwd.getpwnam(user)

    # set groups (first) then user and group ids
    os.setgroups(os.getgrouplist(pwnam.pw_name, pwnam.pw_gid))
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)

    # set the home directory
    os.environ["HOME"] = pwnam.pw_dir
