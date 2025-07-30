import json
from .cli.tabular import Table, Column

def to_did(namespace, name):
    return f"{namespace}:{name}"

def from_did(did):
    return tuple(did.split(":", 1))

def pretty_json(data):
    return json.dumps(data, indent=2, sort_keys=True)
    
def parse_attrs(text):
    parts = [w.split("=",1) for w in text.split()]
    out = {}
    for k, v in parts:
        try:    v = int(v)
        except:
            try:    v = float(v)
            except:
                v = {"null":None, "true":True, "false":False}.get(v, v)
        out[k]=v
    return out
    
def print_handles(handles, print_replicas):
    
    state_order = {
        "initial":      0,
        "reserved":     1,
        "done":         3,
        "failed":       4
    }
    
    table = Table("Status", "Available", "Replicas", "Attempts", "Timeouts", "Worker", 
            Column("File" + (" / RSE, avlbl, URL" if print_replicas else ""),
                left=True)
    )

    handles = list(handles)

    for h in handles:
        #print("print_handles: handle:", h)
        if h.get("replicas") is not None: 
            h["is_available"] = any(r["available"] and r.get("rse_available") for r in h["replicas"].values())
        else: 
            h['is_available'] = False

    handles = sorted(handles, key=lambda h: (0 if h["is_available"] else 1, state_order[h["state"]], h["attempts"], h["namespace"], h["name"]))

    for f in handles:
        rlist = f.get('replicas')
        available_replicas = 0 if rlist is None else len([r for r in rlist.values() if r["available"] and r["rse_available"]])
        nreplicas = 0 if rlist is None else len(rlist)
        state = f["state"]
        timeouts = f.get('attributes', {}).get("timeouts", 0)
        if available_replicas > 0:
            file_available = "yes"
        else:
            file_available = "no"
        table.add_row(
            state,
            file_available,
            "%4d/%-4d" % (available_replicas, nreplicas),
            f["attempts"],
            timeouts,
            f["worker_id"] if f["worker_id"] else "-",
            "%s:%s" % (f["namespace"], f["name"])
        )
        if print_replicas:
            for r in sorted(f["replicas"].values(), key=lambda r: r["preference"]):
                table.add_row(None, None, None, None, None,
                    " %-10s %-3s %s" % (r["rse"], 
                        "yes" if r["available"] else "no", r["url"] or ""
                    )
                )
    table.print()




