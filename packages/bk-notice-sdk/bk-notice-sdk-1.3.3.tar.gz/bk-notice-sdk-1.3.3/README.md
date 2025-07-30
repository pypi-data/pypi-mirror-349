# bk-notice-sdk

## [Quick Start]()
> PS: 使用本sdk需要到对应环境网关的 apigw 申请权限

以下为使用本功能模块的简单配置：

1. 安装版本获取平台公告模块(内部仓库)：

    ```
    pip install bk-notice-sdk
    ```

2. 在项目配置文件中的**INSTALLED_APPS**内添加**bk_notice_sdk**：

    ```
    INSTALLED_APPS += (
        'bk_notice_sdk'
    )
    ```

3. 在项目的`urls.py`中配置路由：

   ```
   urlpatterns = [
       ...,
       url(r'^notice/', include(('bk_notice_sdk.urls', 'notice'), namespace='notice')),
   ] 
   ```
   接入系统可根据需要修改路由前缀。

4. 配置环境变量(也可以在`settings.py`中配置, 见下)
   ```
   # 需将 bkapi.example.com 替换为真实的云 API 域名，在 PaaS 3.0 部署的应用，可从环境变量中获取 BK_API_URL_TMPL
   BK_API_URL_TMPL = "http://bkapi.example.com/api/{api_name}/"
   ```
5. 如果需要自定义配置，在`settings.py`中添加如下配置：
    ```
    BK_NOTICE = {
        'STAGE': 'stage', # 默认读取环境变量，如果读取不到默认为'prod'
        'LANGUAGE_COOKIE_NAME': "xxx", # 若不配置默认 blueking_language
        'DEFAULT_LANGUAGE': 'en', # 默认语言
        'PLATFORM': 'xxx', # 平台注册的 code，用于获取系统通知消息时进行过滤，默认使用 app_code
        'BK_API_URL_TMPL': "http://bkapi.example.com/api/{api_name}/", # 若不配置则读取环境变量
        'BK_API_APP_CODE': 'xxx', # 用于调用 apigw 认证，默认获取 SaaS 的 APP_CODE
        'BK_API_SECRET_KEY': 'xxx', # 用于调用 apigw 认证，默认获取 SaaS 的 SECRET_KEY
    }
    ```
   上述配置按需配置即可，没有的配置项将使用默认值
6. 注册平台

   如果需要注册本平台到通知中心可以执行以下命令:
   ```
   python manage.py register_application
   ```
   > PS: 若本地调试不需要注册平台则不需要执行该命令或者执行以下命令跳过
   ```
   python manage.py register_application --skip
   ```
7. 启动项目：

    ```
    python manage.py runserver
    ```
8. 可用接口

   | 路由       | 方法   | 参数 | 描述     |
      |----------|------|----|--------|
   | announcements/ | GET  | 无  | 获取平台公告 |

   **示例：**
   项目运行后，访问[http://ip:port/notice/announcements/]()即可获取当前**platform**(平台)的公告。

   `注意: 这里的 notice 路由，若在 settings.py 自定义了 ENTRANCE_URL 则为对应的路由`
