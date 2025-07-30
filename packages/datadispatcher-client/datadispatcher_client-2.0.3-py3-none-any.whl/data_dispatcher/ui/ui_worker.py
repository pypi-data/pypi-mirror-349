import sys, time, json
from .ui_lib import to_did, from_did, pretty_json
from .cli import CLI, CLICommand, InvalidOptions, InvalidArguments
from data_dispatcher.api import NotFoundError

class NextFileCommand(CLICommand):
    
    Opts = "jt:c:w:"
    MinArgs = 1
    Usage = """[options] <project_id> -- get next available file
             -w <worker id>     -- specify worker id
             -c <cpu site>      -- choose the file according to the CPU/RSE proximity map for the CPU site
             -j                 -- JSON output
             -t <timeout>       -- wait for next file until "timeout" seconds, 
                                   otherwise, wait until the project finishes
    """

    def __call__(self, command, client, opts, args):
        project_id = int(args[0])
        worker_id = opts.get("-w")
        json_out = "-j" in opts
        timeout = opts.get("-t")
        if timeout is not None: timeout = int(timeout)
        cpu_site = opts.get("-c")

        try:
            reply = client.next_file(project_id, cpu_site=cpu_site, worker_id=worker_id, timeout=timeout)
        except NotFoundError:
            print("project not found")
            sys.exit(1)

        if isinstance(reply, dict):
            if json_out:
                reply["replicas"] = sorted(reply["replicas"].values(), key=lambda r: 1000000 if r.get("preference") is None else r["preference"])
                print(pretty_json(reply))
            else:
                print("%s:%s" % (reply["namespace"], reply["name"]))
        else:
            resp = "timeout" if reply else "done"
            if json_out:
                print('{"state": "%s"}' % resp)
            else:
                print(resp)
            sys.exit(1)        # timeout
           

class DoneCommand(CLICommand):
   
    Opts = "w:"
    MinArgs = 2
    Usage = """[options] <project id> (<DID>|all)                          -- mark a file as done
        -w <worker id>      -- specify worker id
        "all" means mark all files reserved by the worker as done
    """

    def __call__(self, command, client, opts, args):
        project_id, did = args
        worker_id = opts.get("-w")

        if did == "all":
            dids = [to_did(h["namespace"], h["name"]) for h in client.reserved_handles(project_id)]
        else:
            dids = [did]

        for did in dids:
            client.file_done(int(project_id), did, worker_id)
    
class FailedCommand(CLICommand):
    
    Opts = "fw:"
    MinArgs = 2
    Usage = """[options] <project id> (<DID>|all)                      -- mark a file as failed
        -f                  -- final, do not retry the file
        -w <worker id>      -- specify worker id
        "all" means mark all files reserved by the worker as failed
    """
    
    def __call__(self, command, client, opts, args):
        project_id, did = args
        worker_id = opts.get("-w")
        retry = not "-f" in opts

        if did == "all":
            dids = [to_did(h["namespace"], h["name"]) for h in client.reserved_handles(project_id)]
        else:
            dids = [did]
        for did in dids:
            client.file_failed(int(project_id), did, retry, worker_id)

class IDCommand(CLICommand):
    
    Opts = "n"
    Usage = """[-n|<worker id>]                                 -- set or print worker id
        -n          -- generate random worker id
        
        worker id will be saved in <CWD>/.data_dispatcher_worker_id
    """
    
    def __call__(self, command, client, opts, args):
        if "-n" in opts:
            worker_id = client.new_worker_id()
        elif args:
            worker_id = args[0]
            client.new_worker_id(worker_id)
        else:
            worker_id = client.WorkerID
        if not worker_id:
            print("worker id unknown")
            sys.exit(1)
        print(worker_id)
        
class ListReservedCommand(CLICommand):
    
    MinArgs = 1
    Opts = "jw:"
    Usage = """[-j] [-w <worker id>] <project id>              -- list files allocated to the worker
        -j                      -- as JSON
        -w <worker id>          -- specify worker id. Otherwise, use my worker id    
    """

    def __call__(self, command, client, opts, args):
        project_id = int(args[0])
        worker_id = opts.get("-w", client.WorkerID)
        as_json = "-j" in opts
        
        try:    handles = client.reserved_handles(project_id, worker_id)
        except NotFoundError:
            print("project not found", file=sys.stderr)
            sys.exit(1)

        if as_json:
            print(pretty_json(handles))
        else:
            for h in handles:
                for name, val in h.items():
                    print(f"{name:10s}: {val}")
                


WorkerCLI = CLI(
    "id",       IDCommand(),
    "list",     ListReservedCommand(),
    "next",     NextFileCommand(),
    "done",     DoneCommand(),
    "failed",   FailedCommand()
)
