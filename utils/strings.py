# 去掉所有换行符
def remove_newlines(value: str):
    # [电台DJ声音] [电台DJ声音结束]
    value = value.replace("[电台DJ声音]", "")
    value = value.replace("[电台DJ声音结束]", "")
    return ''.join(value.splitlines())
