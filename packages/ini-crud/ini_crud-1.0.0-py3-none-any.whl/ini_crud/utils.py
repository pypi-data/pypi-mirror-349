# -*- coding: utf-8 -*-
import sys
import json
from argparse import ArgumentParser, SUPPRESS
from typing import Dict, List, Any, Optional

"""
# 命令行示例
python cli.py name=api state=present port=80 enabled=yes tags=api,web config='{"env":"prod"}'

# json格式
python cli.py '{"name": "api", "state": "present", "port": 80, "enabled": true, "tags": ["api", "web"], "config": {"env": "prod"}}'
"""


class BaseModule:
    def __init__(
            self,
            argument_spec: Dict[str, Dict[str, Any]],
            required_one_of: List[List[str]] = None,
            mutually_exclusive: List[List[str]] = None,
            required_together: List[List[str]] = None,
            required_if: List[List[str]] = None,
            supports_check_mode: bool = False,
            add_file_common_args: bool = False,
            other_arg_spec: Dict[str, Any] = None
    ):
        self.argument_spec = argument_spec
        self.supports_check_mode = supports_check_mode  # 支持check模式
        self.other_arg_spec = other_arg_spec or {}

        # 解析参数
        self.params = self._parse_arguments()
        self._validate_arguments()

    def _parse_arguments(self) -> Dict[str, Any]:
        """解析命令行参数（支持标准Ansible格式）"""
        parser = ArgumentParser(add_help=True)  # 启用默认帮助支持
        parser.add_argument('args', nargs='*', help=SUPPRESS)
        # 动态添加参数和帮助信息
        for key, spec in {**self.argument_spec, **self.other_arg_spec}.items():
            help_text = spec.get('help', '')  # 获取帮助信息
            action = 'store_true' if spec.get('type') == 'bool' else None
            parser.add_argument('--{}'.format(key), dest=key, action=action, help=help_text)
        args, _ = parser.parse_known_args()

        # 如果没有传入任何参数，则打印帮助信息
        if len(sys.argv) <= 1 or (len(args.args) == 0 and not self._is_json(sys.argv[-1])):
            parser.print_help()
            sys.exit(1)
        params: Dict[str, Any] = {}
        # 优先解析JSON格式参数（最后一个参数为JSON）
        if len(args.args) >= 1 and self._is_json(args.args[-1]):
            params = json.loads(args.args[-1])
            args.args = args.args[:-1]  # 移除已解析的JSON参数

        # 解析key=value参数
        for arg in args.args:
            if '=' in arg:
                key, value = arg.split('=', 1)
                # 处理带引号的参数值
                if value.startswith(("'", '"')) and value.endswith(("'", '"')):
                    value = value[1:-1]  # 移除引号
                params[key] = self._convert_type(key, value)

        # 合并 argument_spec 和 other_arg_spec 的默认值和类型转换
        for key, spec in {**self.argument_spec, **self.other_arg_spec}.items():
            if key not in params and 'default' in spec:
                params[key] = spec['default']
            elif key in params:
                # 如果已存在，再做一次类型转换（确保布尔值等正确）
                params[key] = self._convert_type(key, str(params[key]))

        # 处理check_mode参数
        if self.supports_check_mode and 'check_mode' in params:
            self.check_mode = params['check_mode']
        else:
            self.check_mode = False  # 默认关闭

        return params

    @staticmethod
    def _is_json(s: str) -> bool:
        """判断是否为JSON字符串"""
        try:
            json.loads(s)
            return True
        except json.JSONDecodeError:
            return False

    def _convert_type(self, key: str, value: str) -> Any:
        """根据argument_spec转换参数类型"""
        spec = self.argument_spec.get(key, {})
        type_ = spec.get('type', 'str')

        if type_ == 'int':
            return int(value)
        elif type_ == 'bool':
            if value.lower() in ('false', 'no', 'off', '0', 'f', 'n'):
                return False
            if value.lower() in ('true', 'yes', 'on', '1', 't', 'y'):
                return True
        elif type_ == 'list':
            return value.split(',') if value else []
        elif type_ == 'dict':
            return json.loads(value) if self._is_json(value) else {}
        elif type_ == 'path':
            return value  # 路径类型可自定义处理
        return value  # 字符串直接返回

    def _validate_arguments(self):
        """校验必选参数和类型"""
        errors = []
        # 校验required参数
        for key, spec in self.argument_spec.items():
            if spec.get('required', False) and key not in self.params:
                errors.append("Required parameter missing: {}".format(key))
        # 校验choices参数
        for key, spec in self.argument_spec.items():
            choices = spec.get('choices')
            if choices and self.params.get(key) not in choices:
                errors.append("Invalid value for {}: {}, must be in {}".format(key, self.params.get(key), choices))
        if errors:
            self.fail_json("\n".join(errors))

    def exit_json(self, changed: bool = False, msg: str = "Success", **kwargs) -> None:
        """返回标准JSON结果"""
        result = {"changed": changed, "msg": msg, **self.params, **kwargs}
        if self.supports_check_mode:
            result["check_mode"] = self.check_mode
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    def fail_json(self, msg: str, **kwargs) -> None:
        """返回错误JSON结果"""
        result = {"failed": True, "msg": msg, **self.params, **kwargs}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

# def main():
#     # 定义标准argument_spec格式
#     module_args = dict(
#         name=dict(required=True, type='str'),
#         state=dict(
#             required=False,
#             type='str',
#             choices=['present', 'absent'],
#             default='present'
#         ),
#         port=dict(type='int', default=8080),
#         enabled=dict(type='bool', default=False),
#         tags=dict(type='list'),
#         config=dict(type='dict'),
#     )
#
#     # 初始化模块（支持check_mode等特性）
#     module = AnsibleModule(
#         argument_spec=module_args,
#         supports_check_mode=True
#     )
#
#     # 业务逻辑示例
#     try:
#         # 处理check_mode
#         if module.check_mode:
#             module.exit_json(changed=False, msg="Check mode: 无实际操作")
#
#         # 模拟业务操作
#         result = {
#             "changed": True,
#             "msg": "资源 {} 状态为 {}.".format(module.params["name"], module.params['state']),
#             "port": module.params["port"],
#             "enabled": module.params["enabled"]
#         }
#         # 添加可选参数
#         if module.params.get('tags'):
#             result['tags'] = module.params['tags']
#         if module.params.get('config'):
#             result['config'] = module.params['config']
#
#         module.exit_json(**result)
#
#     except Exception as e:
#         module.fail_json(msg=str(e))
#
#
# if __name__ == "__main__":
#     main()
