# -*- coding: utf-8 -*-
"""
@Time        : 2023/3/22 11:43 下午
@Author      : 章光辉
@Email       : 
@Software    : PyCharm
@Description : 签名
"""
import time
import json
import hashlib


def generate_sign(method, path, params, app_secret, hash_type: str = 'sha256'):
    """
    生成签名
    :param method: 方法，例如 "GET", "POST"
    :param path: 路径，例如 "/v2/in/map/rgeo"
    :param params: 其他参数
    :param app_secret: app 秘钥
    :param hash_type: 加密方式，默认是 'sha256'，还支持 'md5'
    :return:
    """
    sign_str = method + path + "?"
    for key in sorted(params.keys()):
        if key == 'sign':
            continue
        sign_str += key + "=" + str(params[key]) + "&"
    sign_str = sign_str[:-1]
    sign_str += app_secret
    if hash_type == 'md5':
        sign = hashlib.md5(sign_str.encode())
    else:
        sign = hashlib.sha256(sign_str.encode())
    return sign.hexdigest()


def make_payload(path: str, method: str, app_id: str, app_secret: str, data: dict, content_type: str = 'json',
                 hash_type: str = 'sha256') -> list:
    """
    生成包含签名的结构体，可以直接作为 requests 的 get 或 post 等方法的 params 参数使用。

    :param path: 路径，例如 "/v2/in/map/rgeo"
    :param method: 方法，例如 "GET", "POST"
    :param app_id: APP ID
    :param app_secret: app 秘钥
    :param data: 原始数据（不包含 app_id/timestamp/sign 等字段）
    :param content_type: 签名类型，默认是 'json'，还支持 'x-www-form-urlencoded'
    :param hash_type: 加密方式，默认是 'sha256'，还支持 'md5'
    :return: 如果其中一组算路失败, 将会返回 duration = 0 和 distance = 0. 但是不影响其他的 pairs.
    """
    assert method in {"GET", "POST"}

    # 构造请求
    if method == 'POST':
        payload = {
            'app_id': app_id,
            'timestamp': int(time.time()),
            'hash_type': hash_type,
            'sign': '',
        }
        temp = payload.copy()
        if content_type == 'x-www-form-urlencoded':
            temp.update(data)
        else:
            temp['jsonBody'] = json.dumps(data)
        payload["sign"] = generate_sign("POST", path, temp, app_secret, hash_type)
    else:
        payload = {
            **data,
            'app_id': app_id,
            'timestamp': int(time.time()),
            'hash_type': hash_type,
            'sign': '',
        }
        payload["sign"] = generate_sign("GET", path, payload, app_secret, hash_type)
    return payload
