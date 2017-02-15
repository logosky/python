#!/usr/bin/env python
# -*- coding: utf8 -*-

"""Get id data from MySQL"""

import sys
import subprocess

def _get_table_name_by_id(ID, type=1):
    def rs_hash(key):
        a = 63689
        b = 378551
        hash = 0
        for i in range(len(key)):
            hash = hash * a + ord(key[i])
            a = a * b
            hash = hash % (2**32)
        return hash & 0x7FFFFFFF

    def FNVHash1(key):
        p = 16777619
        hash = 2166136261
        for i in range(len(key)):
            hash = (hash ^ ord(key[i])) * p
            hash = hash % (2**32)

        hash += hash << 13
        hash = hash % (2**32)
        hash ^= hash >> 7
        hash = hash % (2**32)
        hash += hash << 3
        hash = hash % (2**32)
        hash ^= hash >> 17
        hash = hash % (2**32)
        hash += hash << 5
        hash = hash % (2**32)
        return hash & 0x7FFFFFFF

    db_prefix = "d_test_"
    offset = rs_hash("%s" % ID) % 100
    db_name = "%s%s" % (db_prefix, offset)
    offset = FNVHash1("%s" % ID) % 100
    table_name = 't_test_%s' % offset
    return (db_name, table_name)

class ShellHelper(object):
    last_err = ""

    def run_cmd(self, command):
        """Run command and return (out,err)"""
        if type(command) == str:
            command = command.split(" ")
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        out, err = p.communicate()
        self.last_err = err
        return out

    def mysql_exec(self, mysql_shell, db, sql):
        mysql_command = mysql_shell.split(' ')
        mysql_command.append(db)
        mysql_command.extend(['-s', '-e', sql])
        return self.run_cmd(mysql_command).split('\n')

MYSQLSHELL = 'mysql -h1 -P36 -ud_user -pd_pwd --default-character-set=utf8'

def mysqlshell_to_conf(mysql_shell):
    matched = re.match(r'mysql -h(?P<host>[0-9.]*) -P(?P<port>[0-9]*) -u(?P<user>[^ ]*) -p(?P<passwd>[^ ]*)', mysql_shell)
    return matched.groupdict()

def main():
    if len(sys.argv) <= 1:
        print "Usage: %s <id>" % sys.argv[0]
        return

    c_id = sys.argv[1]
    shell = ShellHelper()

    db_name, table_name = ('d_test', 't_test')
    sql = "select * from %s where c_media_id='%s'\G" % (table_name, c_id)
    results = shell.mysql_exec(MYSQLSHELL, db_name, sql)
    if len(results) > 1:
        print "# %s %s" % (MYSQLSHELL, db_name)
        print "mysql> %s" % (sql)
        print '\n'.join(results)

main()
