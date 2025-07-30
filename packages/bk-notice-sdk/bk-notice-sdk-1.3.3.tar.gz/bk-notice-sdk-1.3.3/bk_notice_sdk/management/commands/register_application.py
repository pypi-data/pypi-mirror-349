from django.core.management.base import BaseCommand

from bk_notice_sdk.views import api_call


class Command(BaseCommand):
    help = "注册平台"

    def add_arguments(self, parser):
        # 添加一个新的命令行选项 '--skip'
        parser.add_argument("--skip", action="store_true", help="跳过注册平台，不执行任何操作")  # 使用该参数时，将此选项的值设置为 True
        parser.add_argument("--raise_error", action="store_true", help="注册失败是否抛出异常")  # 使用该参数时，将此选项的值设置为 True

    def handle(self, *args, **options):
        # 检查是否接收到 '--skip' 参数
        if options["skip"]:
            self.stdout.write(self.style.WARNING("跳过注册平台"))
            return  # 执行提前结束

        try:
            print("[bk-notice-sdk]call register_application start")
            response = api_call(
                api_method="register_application", success_message="注册平台成功", error_message="注册平台异常", success_code=201
            )
            if response.get("result") is True:
                self.stdout.write(self.style.SUCCESS("成功注册平台"))
            else:
                msg = f"注册平台失败: {response['message']}"
                self.stdout.write(self.style.WARNING(msg))
                if options["raise_error"]:
                    raise Exception(msg)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"注册平台异常: {e}"))
            if options["raise_error"]:
                raise e
