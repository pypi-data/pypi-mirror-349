from .core import do_ini, backup_local, match_opt, match_active_opt, get_ini_lines

# if __name__ == '__main__':
#     do_ini("/etc/hosts", section="test", option="test", value="test", state="present")
#     do_ini("/etc/anotherconf", section="test", option="test", value="test", state="present")
#     do_ini("/etc/anotherconf", section="drinks", option="db", value="hu", state="present", backup=True)
#     do_ini("/etc/anotherconf", section="drinks", option="name", value="hu", state="present", backup=True, _diff=True)
#     do_ini("/etc/anotherconf", section="drinks", option="db3", value="", state="present", backup=True,
#            allow_no_value=True)
#     do_ini("/etc/anotherconf", section="drinks", option="db2", value="hu2", state="present", backup=True,
#            no_extra_spaces=True)
#     changed, backup_file, diff, msg = do_ini("/etc/anotherconf2", section="drinks", option="db", mode="get")
#     print(changed, backup_file, diff, msg['options'])
