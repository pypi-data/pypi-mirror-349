#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import shutil
import tempfile
import time
from .logs import logger
from .errors import FileCopyError, FileNotFoundError

log = logger(__name__)


def match_opt(option, line):
    """
    Match an option line.
    """
    option = re.escape(option)
    return re.match(' *%s( |\t)*=' % option, line) \
        or re.match('# *%s( |\t)*=' % option, line) \
        or re.match('; *%s( |\t)*=' % option, line)


# ==============================================================
# match_active_opt
def match_active_opt(option, line):
    """
    Match an active option line.
    """
    option = re.escape(option)
    return re.match(' *%s( |\t)*=' % option, line)


def backup_local(fn):
    """
    make a date-marked backup of the specified file, return True or False on success or failure
    :param fn:  file name
    :return:
    """
    # backups named basename-YYYY-MM-DD@HH:MM:SS~
    ext = time.strftime("%Y-%m-%d@%H:%M:%S~", time.localtime(time.time()))
    backupdest = '%s.%s' % (fn, ext)

    try:
        shutil.copy2(fn, backupdest)
    except (shutil.Error, IOError) as e:
        FileCopyError(msg='Could not make backup of %s to %s: %s' % (fn, backupdest, e))
    return backupdest


def get_ini_lines(filename):
    """
    读取INI文件内容，并返回每一行组成的列表。
    如果文件不存在或为空，则返回空列表。
    """
    if not os.path.exists(filename):
        return []

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 确保每行都以换行符结尾
    for i in range(len(lines)):
        if not lines[i].endswith('\n'):
            lines[i] += '\n'

    return lines


def do_ini(filename, section=None, option=None, value=None,
           state='present', backup=False, no_extra_spaces=False,
           create=False, check_mode=False, _diff=False,
           allow_no_value=False, mode='set'):
    """
    :param filename:
    :param section:
    :param option:
    :param value:
    :param state:
    :param backup: 控制是否备份文件
    :param no_extra_spaces: 控制是否去除多余的空格
    :param create: 控制是否创建文件
    :param check_mode: 控制是否为检查模式
    :param _diff: 控制是否显示差异
    :param allow_no_value: 控制是否允许没有值
    :param mode: 控制操作模式，可选值为 'set' 或 'get'
    :return: changed, backup_file, diff, msg
    """
    if mode == 'get':
        ini_lines = get_ini_lines(filename)
        result = {
            'section': section,
            'option': option,
            'value': None,
            'options': {},
            'exists': False
        }
        in_section = False
        found_section = False

        for line in ini_lines:
            line = line.strip()
            if line.startswith('['):
                current_section = line[1:-1]
                if section and current_section == section:
                    in_section = True
                    found_section = True
                else:
                    in_section = False
            elif in_section and '=' in line:
                parts = line.split('=', 1)
                key = parts[0].strip()
                val = parts[1].strip() if len(parts) > 1 else None
                if key:
                    result['options'][key] = val
                    result['exists'] = True

        if not found_section:
            msg = "get not found in section '%s'" % section
        elif result['exists']:
            msg = "get option '%s' in section '%s'" % (option, section)
        else:
            msg = "option '%s' not found in section '%s'" % (option, section)
        return result['exists'], None, {}, {**result, 'msg': msg}

    if mode == 'set':
        diff = dict(
            before='',
            after='',
            before_header='%s (content)' % filename,
            after_header='%s (content)' % filename,
        )

        if not os.path.exists(filename):
            if not create:
                FileNotFoundError(msg='Destination %s does not exist !' % filename)
            destpath = os.path.dirname(filename)
            if not os.path.exists(destpath) and not check_mode:
                os.makedirs(destpath)
            ini_lines = []
        else:
            ini_file = open(filename, 'r')
            try:
                ini_lines = ini_file.readlines()
            finally:
                ini_file.close()

        if _diff:
            diff['before'] = ''.join(ini_lines)

        changed = False

        # ini file could be empty
        if not ini_lines:
            ini_lines.append('\n')

        # last line of file may not contain a trailing newline
        if ini_lines[-1] == "" or ini_lines[-1][-1] != '\n':
            ini_lines[-1] += '\n'
            changed = True

        # append fake section lines to simplify the logic
        # At top:
        # Fake random section to do not match any other in the file
        # Using commit hash as fake section name
        fake_section_name = "ad01e11446efb704fcdbdb21f2c43757423d91c5"

        # Insert it at the beginning
        ini_lines.insert(0, '[%s]' % fake_section_name)

        # At botton:
        ini_lines.append('[')

        # If no section is defined, fake section is used
        if not section:
            section = fake_section_name

        within_section = not section
        section_start = 0
        msg = 'OK'
        if no_extra_spaces:
            assignment_format = '%s=%s\n'
        else:
            assignment_format = '%s = %s\n'

        for index, line in enumerate(ini_lines):
            if line.startswith('[%s]' % section):
                within_section = True
                section_start = index
            elif line.startswith('['):
                if within_section:
                    if state == 'present':
                        # insert missing option line at the end of the section
                        for i in range(index, 0, -1):
                            # search backwards for previous non-blank or non-comment line
                            if not re.match(r'^[ \t]*([#;].*)?$', ini_lines[i - 1]):
                                if not value and allow_no_value:
                                    ini_lines.insert(i, '%s\n' % option)
                                else:
                                    ini_lines.insert(i, assignment_format % (option, value))
                                msg = 'option added'
                                changed = True
                                break
                    elif state == 'absent' and not option:
                        # remove the entire section
                        del ini_lines[section_start:index]
                        msg = 'section removed'
                        changed = True
                    break
            else:
                if within_section and option:
                    if state == 'present':
                        # change the existing option line
                        # 会遍历 ini_lines 并根据状态进行操作（添加、修改、删除）
                        if match_opt(option, line):
                            if not value and allow_no_value:
                                newline = '%s\n' % option
                            else:
                                newline = assignment_format % (option, value)
                            option_changed = ini_lines[index] != newline
                            changed = changed or option_changed
                            if option_changed:
                                msg = 'option changed'
                            ini_lines[index] = newline
                            if option_changed:
                                # remove all possible option occurrences from the rest of the section
                                index = index + 1
                                while index < len(ini_lines):
                                    line = ini_lines[index]
                                    if line.startswith('['):
                                        break
                                    if match_active_opt(option, line):
                                        del ini_lines[index]
                                    else:
                                        index = index + 1
                            break
                    elif state == 'absent':
                        # delete the existing line
                        if match_active_opt(option, line):
                            del ini_lines[index]
                            changed = True
                            msg = 'option changed'
                            break

        # remove the fake section line
        del ini_lines[0]
        del ini_lines[-1:]

        if not within_section and option and state == 'present':
            ini_lines.append('[%s]\n' % section)
            if not value and allow_no_value:
                ini_lines.append('%s\n' % option)
            else:
                ini_lines.append(assignment_format % (option, value))
            changed = True
            msg = 'section and option added'

        if _diff:
            diff['after'] = ''.join(ini_lines)

        log.debug("INI lines before processing: %s", ''.join(ini_lines))
        backup_file = None
        # 修改后的数据写入,只有当 changed == True 且 check_mode == False 时才会写入磁盘
        if changed and not check_mode:
            if backup:
                backup_file = backup_local(filename)
            try:
                tmpdir = tempfile.mkdtemp()
                tmpfd, tmpfile = tempfile.mkstemp(dir=tmpdir)
                f = os.fdopen(tmpfd, 'w')
                f.writelines(ini_lines)
                f.close()
            except Exception as e:
                raise e
            try:
                shutil.move(tmpfile, filename)
            except Exception as e:
                raise e
        return changed, backup_file, diff, msg

# ==============================================================
# main
