def count_rows(textfile):
    with open(f"./data/{textfile}", "r") as file:
        for count, line in enumerate(file):
            pass
    return count

command_data = {
    "pslist" : {
        "columns": 12,
        "rows": count_rows,
        "headers": ["PID","PPID","ImageFileName","Offset(V)","Threads","Handles","SessionId","Wow64"
                    ,"CreateTime","ExitTime","File","output"],
        "params": ["PID"],
        "description": "\nTo list the processes of a system, use the pslist command. This walks the doubly-linked list pointed to by PsActiveProcessHead and shows the offset, process name, process ID, the parent process ID, number of threads, number of handles, and date/time when the process started and exited. This plugin does not detect hidden or unlinked processes (but psscan can do that).",
        "info": "Volatility 3 Framework 2.4.1\nusage: volatility windows.pslist.PsList [-h] [--physical] [--pid [PID ...]] [--dump]\noptions:\n-h, --help       show this help message and exit\n--physical       Display physical offsets instead of virtual\n--pid [PID ...]  Process ID to include (all other processes are excluded)\n--dump           Extract listed processes"
    },
    "psscan" : {
        "columns": 12,
        "rows": count_rows,
        "headers": ["PID","PPID","ImageFileName","Offset(V)","Threads","Handles","SessionId","Wow64"
                    ,"CreateTime","ExitTime","File","output"],
        "params": ["PID"],
        "description":"\nTo enumerate processes using pool tag scanning, use the psscan command. This can find processes that previously terminated (inactive) and processes that have been hidden or unlinked by a rootkit.",
        "info": "Volatility 3 Framework 2.4.1\nusage: volatility windows.psscan.PsScan [-h] [--pid [PID ...]] [--dump] [--physical]\noptions:\n-h, --help       show this help message and exit\n--pid [PID ...]  Process ID to include (all other processes are excluded)\n--dump           Extract listed processes\n--physical       Display physical offset instead of virtual"
    },
}

command_list = {"DLLs": ["dlldump", "dlllist"],
                "Modules": ["moddump", "modules", "modscan"],
                "Processes": ["pslist", "psscan", "pstree"],
                "Registry": ["hivedump", "hivelist", "hivescan"]}
commands = ["dlldump", "dlllist", "moddump", "modules", "modscan", "pslist", "psscan", "pstree", "hivedump", "hivelist", "hivescan"]
supported_commands = ["pslist", "psscan"]

service = None
service_changed = False