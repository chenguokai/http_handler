from easydict import EasyDict as ed

config = ed({
    "encoding_wechat" : 'utf-8',
    "encoding_alipay" : "gbk",
    "focus" : ['交易时间','类型','交易对方','金额','收/支'],
    "disable_database" : True,
    "path" : "/var/www/html"
})