#!/usr/bin/env python3

import subprocess as sp
import os
import shlex
from console import fg, bg, fx
import click
import datetime as dt

def get_user_pass():
    FI = "~/.influx_userpassdb"
    FI = os.path.expanduser(FI)
    with open(FI) as f:
        res = f.readlines()
    u = res[0].strip()
    p = res[1].strip()
    d = res[2].strip()
    return u, p, d


def call_cmd(CMD2, database=None, fromdb=None, todb=None, silent=False):
    u, p, _ = get_user_pass()
    CMD = ""
    if database is None:
        CMD = f"influx -username '{u}' -password '{p}' -execute '{CMD2}'"
    else:
        CMD = f"influx -username '{u}' -password '{p}' -database {database} -execute '{CMD2}'"
    CMDx = shlex.split(CMD)
    result = sp.run(CMDx, capture_output=True, text=True )
    if result.returncode != 0:
        print("!...  PROBLEM", CMDx)
        ok = False
    else:
        if not silent:
            print(fg.darkgray, result.stdout, fg.default)
    return result.stdout


def show_databases():
    print(fg.blue, "showinfg database", fg.default)
    res = call_cmd( "  SHOW DATABASES " )
    #print(res)
    res = res.split("\n")[3:]
    print(res, ":")
    res = [ x for x in res if (len(x) > 0) and (x[0] != "_") and (x[0] != "-")  and (x.find("name") < 0)and (x.find("i_am_") < 0)  ]
    print(res)
    return res

def create_database( db ):
    print(fg.blue, "creating database", fg.default)
    res = call_cmd( f"  CREATE DATABASE '{db}' " ).strip().split("\n")
    #print(res, ":")
    #res = [ x for x in res if (x[0] != "_") and (x[0] != "-")  and (x.find("name") < 0)and (x.find("i_am_") < 0)]
    print(res)

def drop_database( db ):
    print(fg.blue, "dropping database", fg.default)
    res = call_cmd( f"  DROP DATABASE '{db}' " ).strip().split("\n")
    #print(res, ":")
    #res = [ x for x in res if (x[0] != "_") and (x[0] != "-")  and (x.find("name") < 0)and (x.find("i_am_") < 0)]
    print(res)

def show_measurements(database):
    print(fg.blue, f"showing measurements @ {database}", fg.default)
    res = call_cmd( f"SHOW MEASUREMENTS  ", database=database)
    #
    res = res.split("\n")[3:]
    #print(res, ":")
    res = [ x for x in res if (len(x) > 0) and (x[0] != "_") and (x[0] != "-")  and (x.find("name") < 0)and (x.find("i_am_") < 0)  ]
    print(res)
    return res

def copy_measurement(m1, db1, db2, silent=False):
    if not silent:
        print(fg.blue, f"copy measurement {m1} from {db1} to {db2}", fg.default)
    CMD = f"SELECT * INTO {db2}..{m1} FROM {db1}..{m1} group by *"
    if not silent:
        print(CMD)
    res = CMD
    res = call_cmd( CMD, database=db2)
    if not silent:
        print(res)
    return res
    #res = call_cmd( f"SELECT * INTO {m1}..[{db2}] FROM {m1}..[{db1}] group by *", fromdb=db1, to_db=db2)
    #print(res)
#select * into Verhaeg_Energy..[measurement_name_destination] from Verhaeg_IoT..[measurement_name_source] group by *

def delete_measurement(m1, db1):
    print(fg.blue, f"delete measurement {m1} from {db1} ", fg.default)
    CMD = f"DROP MEASUREMENT {m1} "
    res = CMD
    res = call_cmd( CMD, database=db1)
    return res
    #res = call_cmd( f"SELECT * INTO {m1}..[{db2}] FROM {m1}..[{db1}] group by *", fromdb=db1, to_db=db2)
    #print(res)
#select * into Verhaeg_Energy..[measurement_name_destination] from Verhaeg_IoT..[measurement_name_source] group by *



def show_measurement_newest_sample(m1, db1, silent=False):
    if not silent: print(fg.blue, f"newest measurement {m1} from {db1} ", fg.default)
    CMD = f"SELECT * FROM {m1} ORDER BY time DESC LIMIT 10"
    res = call_cmd( CMD, database=db1, silent=silent)
    #res = res.split("\n")[3:]
    #res = [x for x in res if len(x) > 0] # last line
    #if not silent: print(res)
    return res

def show_measurement_newest(m1, db1, silent=False):
    if not silent: print(fg.blue, f"newest measurement {m1} from {db1} ", fg.default)
    CMD = f"SELECT * FROM {m1} ORDER BY time DESC LIMIT 1"
    res = call_cmd( CMD, database=db1, silent=silent)
    res = res.split("\n")[3:]
    res = [x for x in res if len(x) > 0] # last line
    res = res[0].split()[0] # t
    res = int(res)
    if not silent: print(res)
    timen = dt.datetime.fromtimestamp(res / 1e9)
    if not silent: print(timen)
    now = dt.datetime.now()
    age = (now - timen)
    if not silent: print("AGE", age)
    sage = str(age)[:-7]
    sdate = str(timen)[:-7]
    if not silent: print("AGE", age, "    ",  sage, sdate)
    return timen


def show_measurement_oldest(m1, db1, silent=False):
    if not silent: print(fg.blue, f"oldest measurement {m1} from {db1} ", fg.default)
    CMD = f"SELECT * FROM {m1} ORDER BY time ASC LIMIT 1"
    res = call_cmd( CMD, database=db1, silent=silent)
    res = res.split("\n")[3:]
    res = [x for x in res if len(x) > 0] # last line
    res = res[0].split()[0] # t
    res = int(res)
    if not silent: print(res)
    timen = dt.datetime.fromtimestamp(res / 1e9)
    if not silent: print(timen)
    now = dt.datetime.now()
    age = (now - timen)
    sage = str(age)[:-7]
    sdate = str(timen)[:-7]
    if not silent: print("AGE", age, "    ", sage, sdate)
    return timen

def show_measurement_newest_oldest(m1, db1, silent=False):
    tn = show_measurement_newest(m1, db1, silent=True)
    to = show_measurement_oldest(m1, db1, silent=True)
    period = str(tn - to)
    if period[-7] == ".":period = period[:-7]
    now = dt.datetime.now()
    age = now - tn
    sage = str(age)[:-7]
    ID = f" measurement {m1} of {db1}"
    # remove fractions if present
    stn = str(tn)
    if len(stn) > 21: stn = stn[:-7]
    sto = str(to)
    if len(sto) > 21: sto = sto[:-7]
    res = f"\n{ID}\n--------------------------\nAGE    = {sage}   \nPERIOD = {period}\nNEWEST = {stn}\nOLDEST = {sto}"
    if not silent: print(res)
    return res

@click.command()
@click.argument('command')
@click.option('--name', '-n')
@click.option('--fromdb', '-f', default=None)
@click.option('--todb', '-t', default=None)
def main(command, name, fromdb, todb):
    print("Hi")
    if command == "sd":
        show_databases()
    elif command == "cd":
        if name is None:
            print("X... name is none")
        create_database( name )
    elif command == "sm":
        if name is None:
            print("X... name is none")
            return
        show_measurements( name )
    elif command == "cm":
        if name is None or fromdb is None or todb is None:
            print("X... name or db is none")
            return
        copy_measurement( name, fromdb, todb )
    elif command == "sn":
        if name is None or fromdb is None:
            print("X... name or db is none")
            return
        show_measurement_newest( name, fromdb )
    elif command == "so":
        if name is None or fromdb is None:
            print("X... name or db is none")
            return
        show_measurement_oldest( name, fromdb )
    elif command == "sno":
        if name is None or fromdb is None:
            print("X... name or db is none")
            return
        show_measurement_newest_oldest( name, fromdb )
    elif command == "sns":
        if name is None or fromdb is None:
            print("X... name or db is none")
            return
        show_measurement_newest_sample( name, fromdb )

if __name__ == "__main__":
    main()
