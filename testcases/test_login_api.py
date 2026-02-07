import pytest
import requests

@pytest.mark.api
def test_get_public_key():
    """测试获取RSA公钥接口"""
    # 发送GET请求获取公钥
    resp = requests.request("GET", "http://115.191.47.61/api/login/auth/publicKey")
    # 断言响应状态码和内容
    assert resp.status_code == 200
    assert resp.json()["code"] == 200
    assert resp.json()["msg"] == "success"
    assert 'data' in resp.json()
    assert 'publicKey' in resp.json()['data']
    assert 'timestamp' in resp.json()['data']
    assert 'algorithm' in resp.json()['data']
    assert resp.json()['data']['algorithm'] == 'RSA'
    # 提取公钥和时间戳
    public_key = resp.json()['data']['publicKey']
    print(public_key)