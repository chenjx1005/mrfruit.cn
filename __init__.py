from flask import Flask
import alipay
# configuration
DATABASE = '/home/mrfruit/fruit2/data.db'
DEBUG = True
SECRET_KEY = 'development key'

alipayTool=alipay.alipay(
                partner="2088302144896577",
                key="hugp0odb7elvw131cjla0s6x2aoxizqp",
                sellermail="18768114571",
                notifyurl="http://www.mrfruit.cn/test",
                returnurl="http://www.mrfruit.cn/test2",
                showurl=""
                )

app = Flask(__name__)
app.config.from_object(__name__)

import fruit2.views

