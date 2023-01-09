


def no_motion_finder(motions):
    motion = set(motions)
    if "no_motion" in motion and len(motion)==1:
        return "True"
    else:
        return "False"