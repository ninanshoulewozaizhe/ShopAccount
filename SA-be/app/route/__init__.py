from app import app
from app.route.productController import product_controller
from app.route.shopController import shop_controller
from app.route.userController import user_controller
from app.route.salesController import sales_controller

def bp_register():
    # 蓝图挂载
    app.register_blueprint(product_controller)
    app.register_blueprint(shop_controller)
    app.register_blueprint(user_controller)
    app.register_blueprint(sales_controller)