from datetime import datetime
import pytz


def format_datetime_with_timezone(timezone_str='Asia/Shanghai', output_format="%Y-%m-%d %H:%M:%S,%f", dt=None):
    """
    格式化当前日期时间，支持时区。

    :param timezone_str: 时区字符串，例如 'Asia/Shanghai'
    :param output_format: 输出的日期时间格式，默认是 "%Y-%m-%d %H:%M:%S"
    :param dt: 要格式化的 datetime 对象，默认为 None 表示当前时间
    :return: 格式化后的日期时间字符串
    """
    if dt is None:
        # 使用当前 UTC 时间
        dt = datetime.utcnow().replace(tzinfo=pytz.utc)

    try:
        # 获取指定时区
        tz = pytz.timezone(timezone_str)

        # 将输入的时间转换为指定时区的时间
        localized_dt = dt.astimezone(tz)

        # 返回格式化后的时间字符串
        return localized_dt.strftime(output_format)

    except Exception as e:
        return f"时间格式化错误: {str(e)}"


# 示例用法
if __name__ == "__main__":
    # 格式化为上海时间
    formatted_time = format_datetime_with_timezone('Asia/Shanghai')
    print(f"格式化后的时间: {formatted_time}")

    formatted_time = format_datetime_with_timezone('UTC')
    print(f"格式化后的时间: {formatted_time}")
