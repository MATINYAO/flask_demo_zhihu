# 配置文件

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "xxxxxxxxx"
DATABASE = "caijioa"

# 连接数据库
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱配置，按个人的去申请
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_TLS = True
MAIL_PORT = 587
MAIL_USERNAME = "xxxxxxxx@qq.com"
MAIL_PASSWORD = "xxxxxxxxxxx"
MAIL_DEFAULT_SENDER = "xxxxxxxx@qq.com"

SECRET_KEY = "adsfbuiasdfbqwer123;'dfa.,"
