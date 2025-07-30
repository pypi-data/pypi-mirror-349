#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
from .utils import BaseModule
from .core import do_ini


# from logs import logger
#
# log = logger(__name__)


def main():
    module = BaseModule(
        argument_spec=dict(
            dest=dict(required=True, help="目标INI文件路径"),
            section=dict(required=True, help="要操作的section名称"),
            option=dict(required=False, help="要操作的option名称"),
            value=dict(required=False, help="设置的值"),
            backup=dict(default=False, type='bool', help="是否开启备份"),
            state=dict(default='present', choices=['present', 'absent'], help="状态：present/absent"),
            no_extra_spaces=dict(required=False, default=False, type='bool', help="是否移除空格"),
            create=dict(default=True, type='bool', help="如果文件不存在是否创建"),
        ),
        other_arg_spec=dict(
            check_mode=dict(default=False, type='bool', help="运行在check模式"),
            diff=dict(default=False, type='bool', help="显示配置差异"),
            allow_no_value=dict(default=True, type='bool', help="允许value为空"),
            mode=dict(default='set', type='str', choices=['set', 'get'], help="操作模式：set/get"),
        )
    )
    dest = os.path.expanduser(module.params.get('dest'))
    section = module.params.get("section")
    option = module.params.get("option", None)
    value = module.params.get("value", None)
    state = module.params.get("state")
    backup = module.params.get("backup")
    no_extra_spaces = module.params['no_extra_spaces']
    create = module.params['create']
    check_mode = module.params['check_mode']
    has_diff = module.params['diff']
    has_allow_no_value = module.params['allow_no_value']
    mode = module.params['mode']

    # log.debug(
    #     "dest:{} \nsection:{} \noption:{} \nvalue:{} \nstate:{} \nbackup:{} \nno_extra_spaces:{} \ncreate:{} \ncheck_mode:{} \nhas_diff:{} \nhas_allow_no_value:{} \nmode:{}".format(
    #         dest, section, option, value, state, backup, no_extra_spaces, create, check_mode, has_diff,
    #         has_allow_no_value, mode)
    # )
    (changed, backup_file, diff, msg) = do_ini(dest, section, option, value, state, backup, no_extra_spaces,
                                               create, check_mode, has_diff, has_allow_no_value, mode)

    results = {'changed': changed, 'stdout': msg, 'dest': dest, 'diff': diff, 'mode': mode}
    if backup_file is not None:
        results['backup_file'] = backup_file

    module.exit_json(**results)
