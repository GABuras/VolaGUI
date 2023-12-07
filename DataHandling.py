def count_rows(textfile):
    with open(f"./data/{textfile}", "r") as file:
        for count, line in enumerate(file):
            pass
    return count

command_data = {
    # This is not real (?)
    "dlldump" : {
        "columns": 0,
        "rows": count_rows,
        "headers": [],
        "params": [],
        "description":"",
        "info": ""
    },
    "dlllist" : {
        "columns": 9,
        "rows": count_rows,
        "headers": ["PID", "Process", "Base", "Size", "Name", "Path", "LoadTime","File", "output"],
        "params": [],
        "description":"\nLists the loaded modules in a particular windows memory image",
        "info": "Volatility 3 Framework 2.5.0\nusage: volatility windows.dlllist.DllList [-h] [--pid [PID ...]] [--dump]\noptional arguments:\n-h, --help       show this help message and exit \n--pid [PID ...]  Process IDs to include (all other processes are excluded) \n--dump           Extract listed DLLs"
    },
    # This is not real (?)
    "moddump" : {
        "columns": 0,
        "rows": count_rows,
        "headers": [],
        "params": [],
        "description":"",
        "info": ""
    },
    "modules" : {
        "columns": 7,
        "rows": count_rows,
        "headers": ["Offset","Base","Size","Name","Path","File","output"],
        "params": [],
        "description":"\nLists the loaded kernel modules",
        "info": "Volatility 3 Framework 2.5.0 \nusage: volatility windows.modules.Modules [-h] [--dump] [--name NAME] \noptional arguments: \n-h, --help   show this help message and exit \n--dump       Extract listed modules \n--name NAME  module name/sub string"
    },
    "modscan" : {
        "columns": 7,
        "rows": count_rows,
        "headers": ["Offset","Base","Size","Name","Path","File","output"],
        "params": [],
        "description":"\nScans for modules present in a particular windows memory image",
        "info": "Volatility 3 Framework 2.5.0 \nusage: volatility windows.modscan.ModScan [-h] [--dump] \noptional arguments: \n-h, --help  show this help message and exit \n--dump      Extract listed modules"
    },
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
    "pstree" : {
        "columns": 12,
        "rows": count_rows,
        "headers": ["PID","PPID","ImageFileName","Offset(V)","Threads","Handles","SessionId","Wow64"
                    ,"CreateTime","ExitTime","File","output"],
        "params": ["Display physcial offsets","PID"],
        "description": "\nPlugin for listing processes in a tree based on their parent process ID",
        "info": "Volatility 3 Framework 2.5.0 \nusage: volatility windows.pstree.PsTree [-h] [--physical] [--pid [PID ...]] \noptional arguments: \n-h, --help       show this help message and exit \n--physical       Display physical offsets instead of virtual \n--pid [PID ...]  Process ID to include (with ancestors and descendants, all other processes are excluded) "
    },
    # This is not real (?)
    "hivedump" : {
        "columns": 0,
        "rows": count_rows,
        "headers": [],
        "params": [],
        "description":"",
        "info": ""
    },
    "hivelist" : {
        "columns": 4,
        "rows": count_rows,
        "headers": ["Offset","FileFullPath","File","output"],
        "params": ["Filter"],
        "description":"\nLists the registry hives present in a particular	memory image",
        "info": "Volatility 3 Framework 2.5.0 \nusage: volatility windows.registry.hivelist.HiveList [-h] [--filter FILTER][--dump] \noptional arguments: \n-h, --help       show this help message and exit \n--filter FILTER  String to filter hive names returned \n--dump           Extract listed registry hives "
    },
    "hivescan" : {
        "columns": 1,
        "rows": count_rows,
        "headers": ["Offset"],
        "params": [],
        "description":"\nScans for registry hives present in a particular windows memory image",
        "info": "Volatility 3 Framework 2.5.0 \nusage: volatility windows.registry.hivescan.HiveScan [-h] \noptional arguments: \n-h, --help  show this help message and exit "
    },



}

command_list = {"DLLs": ["dlldump", "dlllist"],
                "Modules": ["moddump", "modules", "modscan"],
                "Processes": ["pslist", "psscan", "pstree"],
                "Registry": ["hivedump", "hivelist", "hivescan"]}
commands = ["dlldump", "dlllist", "moddump", "modules", "modscan", "pslist", "psscan", "pstree", "hivedump", "hivelist", "hivescan"]
#supported_commands = ["pslist", "psscan"]
supported_commands = ["dlllist", "modules", "modscan", "pslist", "psscan", "hivelist", "hivescan"]

service = None
service_changed = False