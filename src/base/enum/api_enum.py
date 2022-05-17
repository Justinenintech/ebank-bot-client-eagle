from enum import Enum


class Api(Enum):
    """
    设备注册接口
    """
    Register_Device_Url = "/botApi/bot/register"

    """
    心跳监测接口
    """
    Heartbeat_Url = "/botApi/bot/heartbeat/{botId}"

    """
    获取任务 get 根据ip，序列号获取当前设备的任务
    """
    Get_Task_Url = "/botApi/bot/task/load/{botId}"

    """
    完成任务接口
    """
    Done_Task_Url = "/botApi/bot/task/done/{taskId}"

    """
    推送图形码给任务接口
    """
    Push_Captcha_Task_Url = "/botApi/bot/task/captcha/{taskId}"

    """
    提交交易码接口
    """
    Trade_No_Url = "/botApi/bot/task/tradeNo/{tradeNo}/{taskId}"

    """
    获取otp 接口
    """
    Get_Otp_Url = "/botApi/bot/task/load/otp/{taskId}"

    """
    获取任务详情，验证码之后使用此 接口
    """
    Get_Task_Detail_Url = "/botApi/bot/task/load/captcha/{taskId}"

    """
    推送二维码 接口
    """
    Push_Qr_Task_Url = "/botApi/bot/task/qr/{taskId}"

    """
    登录结果接口
    """
    Login_Error_Result_Url = "/botApi/bot/task/login/result/{taskId}"

    """
    支付回调 接口
    """
    Pay_Result_Url = "/botApi/bot/task/payment/confirm/{taskId}"

    """
    推送otp的 交易码信息
    """
    Otp_Tradeno_Url = "/botApi/bot/task/otp/tradeno/{taskId}"

    """
    获取登录信息 接口
    """
    Login_Info_Url = "/botApi/bot/task/login/ebank/{botId}/{taskId}"

    """
    推送opt验证结果 接口
    """
    Otp_Intermediate_State = "/botApi/bot/task/opt/result/{taskId}"

    def get_heartbeat_url(self, bot_id) -> str:
        """
        获取心跳 地址
        :param bot_id: 机器人id
        :return:  获取任务url
        """
        return self.value.replace("{botId}", bot_id)

    def get_task_url(self, bot_id) -> str:
        """
        获取任务 url
        :param bot_id: 机器人id
        :return: 获取任务url
        """
        return self.value.replace("{botId}", bot_id)
