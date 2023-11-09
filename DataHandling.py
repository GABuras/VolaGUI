def count_rows(textfile):
    with open(f"./data/{textfile}", "r") as file:
        for count, line in enumerate(file):
            pass
    return count

command_data = {
    "pslist" : {
        "columns": 12,
        "headers": ["PID","PPID","ImageFileName","Offset(V)","Threads","Handles","SessionId","Wow64"
                    ,"CreateTime","ExitTime","File","output"]
    },
    "psscan" : {
        "columns": 12,
        "headers": ["PID","PPID","ImageFileName","Offset(V)","Threads","Handles","SessionId","Wow64"
                    ,"CreateTime","ExitTime","File","output"]
    },
    "rows": count_rows
}