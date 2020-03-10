<template>
  <div>
    <h3>店铺管理</h3>
    <div class="s_info_container">
      <img class="s_img" :src="`/getImg?f=${shop.img}&t=${Math.random()}`" alt="s_img">
      <div class="s_info">
        <div>
          <div class="s_name">{{ shop.name }}</div>
          <div class="s_desc">{{ shop.description }}</div>
        </div>
        <div class="bottom_container">
          <div class="s_sales_volumes">已卖 {{ shop.salesVolumes }} 件</div>
          <div class="sales_statistic_btns_g1" v-if="!getSalesDetail">
            <el-button @click="getSalesDetailfn">查看销量详细统计</el-button>
            <el-button @click="updateShopDialog = true">更新店铺信息</el-button>
            <el-button @click="AddNewProductDialog = true">添加商品</el-button>
            <el-button type="danger">删除店铺</el-button>
            <el-dialog class="info_dialog" title="更新店铺信息" :visible.sync="updateShopDialog">
              <div class="info_dialog_container">
                <el-upload
                  class="avatar-uploader"
                  action="/shopImg"
                  :show-file-list="false"
                  :on-success="shopAvatarUploadSuccess"
                  :before-upload="beforeAvatarUpload">
                  <img v-if="modifyShop.img" :src="`/getImg?f=${modifyShop.img}&t=${Math.random()}`" class="avatar">
                  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>
                <el-form>
                  <el-form-item label="店铺名称">
                    <el-input class="info_name_input"
                    v-model="modifyShop.name"
                    placeholder="请输入名称"></el-input>
                  </el-form-item>
                  <el-form-item label="店铺描述">
                    <el-input
                      class="info_desc_input"
                      type="textarea"
                      :rows="2"
                      placeholder="请输入内容"
                      v-model="modifyShop.description">
                    </el-input>
                  </el-form-item>
                </el-form>
              </div>
              <div slot="footer" class="dialog-footer">
                <el-button @click="cancelUpdateShopInfo">取 消</el-button>
                <el-button type="primary" @click="submitUpdateShopInfo">确 定</el-button>
              </div>
            </el-dialog>
            <el-dialog class="info_dialog" title="添加商品" :visible.sync="AddNewProductDialog">
              <div class="info_dialog_container">
                <el-upload
                  class="avatar-uploader"
                  action="/shopImg"
                  :show-file-list="false"
                  :on-success="productAvatarUploadSuccess"
                  :before-upload="beforeAvatarUpload">
                  <img v-if="newProduct.img" :src="`/getImg?f=${newProduct.img}&t=${Math.random()}`" class="avatar">
                  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>
                <el-form>
                  <el-form-item label="商品名称">
                    <el-input class="info_name_input"
                    v-model="newProduct.name"
                    placeholder="请输入名称"></el-input>
                  </el-form-item>
                  <el-form-item label="商品描述">
                    <el-input
                      class="info_desc_input"
                      type="textarea"
                      :rows="2"
                      placeholder="请输入内容"
                      v-model="newProduct.description">
                    </el-input>
                  </el-form-item>
                  <el-form-item label="更新/添加种类库存">
                    <br/>
                    <el-autocomplete
                      class="p_info_new_type_input"
                      v-model="PNewType"
                      :fetch-suggestions="querySearch"
                      placeholder="请输入种类"
                    ></el-autocomplete> : 
                    <el-input class="p_info_new_type_stocks_input" type="number" v-model="PNewTypeAmount"></el-input>
                    <el-button type="primary" @click="updatePType">确定</el-button>
                  </el-form-item>
                </el-form>
                <div>
                  <div class="type_list" v-for="type in Object.keys(newProduct.type)" :key="String(type)">
                    <div>{{`${type} : ${newProduct.type[type]}`}}</div>
                    <i class="el-icon-delete" @click="deletePType(type)"></i>
                  </div>
                </div>
              </div>
              <div slot="footer" class="dialog-footer">
                <el-button @click="AddNewProductDialog = false">取 消</el-button>
                <el-button type="primary" @click="AddNewProductDialog = false">确 定</el-button>
              </div>
            </el-dialog>
          </div>
          <div class="sales_statistic_btns_g2" v-else>
            <el-button @click="getSalesDetailfn">返回预览</el-button>
          </div>
        </div>
      </div>
    </div>
    <div class="s_sales_preview" v-if="!getSalesDetail">
      <div class="product_list">
        <h3>商品列表</h3>
        <product-list
        :allProducts="allProducts"
        :showPageSize="showPageSize"
        ></product-list>
        <div>店内暂无商品，请添加商品。</div>
      </div>
      <!-- <div class="products_sales_date">
        <h3>销量统计</h3>
        <span>日期选择：</span>
        <el-date-picker
          v-model="salesDatePick"
          type="daterange"
          align="right"
          unlink-panels
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          :picker-options="datePickerOptions"
          @change="datePickerChange">
        </el-date-picker>
        <ve-line></ve-line>
      </div> -->
    </div>
    <div class="sales_detail_table" v-else>
      <el-table></el-table>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';
import productList from '@/components/home/productList.vue';
import { IProductDetailItem, ISuggestObj, IProductSalesItem } from '@/typing/productDetail/typings';
import { IShopItem } from '@/typing/shops/typings';
import { IProductItem } from '@/typing/home/typings';
import store from '@/store';
import { LOAD_CUR_SHOP_PRODUCTS, GET_CUR_SHOP_PRODUCTS } from '@/store/modules/product/constants';
import { LOAD_CUR_SHOP, GET_CUR_SHOP, UPDATE_SHOP } from '@/store/modules/shop/constants';
@Component({
  name: 'shopManage',
  components: {
    productList
  },
  async beforeRouteEnter(to: any, from: any, next: any) {
    const sid = to.params.sid;
    const dateStr = new Date().toISOString().split('T')[0];
    await store.dispatch(`product/${LOAD_CUR_SHOP_PRODUCTS}`, sid);
    await store.dispatch(`shop/${LOAD_CUR_SHOP}`, sid);
    const products = store.getters[`product/${GET_CUR_SHOP_PRODUCTS}`];
    const shop = store.getters[`shop/${GET_CUR_SHOP}`];
    console.log(products);
    console.log(shop);
    next((vm: any) => {
      vm.allProducts = [ ...products ];
      vm.shop = { ...shop };
      vm.modifyShop = { ...shop };
    });
  }
})
export default class ShopManage extends Vue {
  getSalesDetail = false;
  updateShopDialog = false;
  AddNewProductDialog = false;
  showSalesDialog = false;
  shop: IShopItem = {
    id: 1,
    uid: 1,
    name: '',
    description: '',
    salesVolumes: 0,
    productAmount: 0,
    img: ''
  };

  modifyShop: IShopItem = JSON.parse(JSON.stringify(this.shop));

  newProduct: IProductDetailItem = {
    id: -1,
    name: '',
    description: '',
    salesVolumes: 0,
    img: '',
    sid: this.shop.id,
    shop: this.shop.name,
    type: {}
  };
  PNewType = '';
  PNewTypeAmount = 0;
  allProducts: IProductDetailItem[] = [];
  showPageSize = 8;

  // datePickerOptions = {
  //   shortcuts: [{
  //     text: '最近一周',
  //     onClick(picker: any) {
  //       const end = new Date();
  //       const start = new Date();
  //       start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
  //       picker.$emit('pick', [start, end]);
  //     }
  //   }, {
  //     text: '最近一个月',
  //     onClick(picker: any) {
  //       const end = new Date();
  //       const start = new Date();
  //       start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
  //       picker.$emit('pick', [start, end]);
  //     }
  //   }],
  //   disabledDate(curDate: any) {
  //     const end = new Date();
  //     const start = new Date();
  //     start.setTime(start.getTime() - 3600 * 1000 * 24 * 31);
  //     return curDate < start || curDate > end;
  //   }
  // };

  // salesDatePick = [];

  // datePickerChange() {
  //   console.log(this.salesDatePick);
  // }

  getSalesDetailfn() {
    this.getSalesDetail = !this.getSalesDetail;
  }

  querySearch(queryString: string, cb: any) {
    const suggestStrs = this.formatSuggestStrs(Object.keys(this.newProduct.type));
    const results = queryString ? suggestStrs.filter(this.createFilter(queryString)) : suggestStrs;
    // 调用 callback 返回建议列表的数据
    cb(results);
  }

  formatSuggestStrs(suggestStrs: string[]): ISuggestObj[] {
    const SuggestStrsObjArr: ISuggestObj[] = [];
    suggestStrs.forEach((str) => {
      SuggestStrsObjArr.push({value: str});
    });
    return SuggestStrsObjArr;
  }

  createFilter(queryString: string) {
    return (type: ISuggestObj) => {
      return (type.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
    };
  }

  deletePType(deleteType: string) {
    const originType = JSON.parse(JSON.stringify(this.newProduct.type));
    for (const type in originType) {
      if (type === deleteType) {
        delete originType[type];
        this.$set(this.newProduct, 'type', originType);
      }
    }
  }

  updatePType() {
    this.PNewType = this.PNewType.trim();
    if (this.PNewType) {
      this.$set(this.newProduct.type, this.PNewType, this.PNewTypeAmount);
    }
  }

  beforeAvatarUpload(file: any) {
    const isJPGorPNG = file.type === 'image/jpeg' || file.type === 'image/png';
    const isLt10M = file.size / 1024 / 1024 < 10;
    if (!isJPGorPNG) {
      this.$message.error('请上传图片类型的文件');
      return false;
    }
    if (!isLt10M) {
      this.$message.error('上传头像图片大小不能超过 10MB');
      return false;
    }
    return isJPGorPNG && isLt10M;
  }

  shopAvatarUploadSuccess(res: any) {
    console.log(res);
    this.modifyShop.img = res.data;
    console.log(this.modifyShop.img);
    this.$message.success('图片上传成功');
  }

  productAvatarUploadSuccess(res: any) {
    console.log(res);
    this.newProduct.img = res.data;
    console.log(this.newProduct.img);
    this.$message.success('图片上传成功');
  }

  cancelUpdateShopInfo() {
    this.modifyShop = { ...this.shop };
    this.updateShopDialog = false;
  }

  async submitUpdateShopInfo() {
    const fields = Object.freeze({ ...this.modifyShop });
    console.log(fields);
    const result = await this.$store.dispatch(`shop/${UPDATE_SHOP}`, fields);
    this.updateShopDialog = false;
    if (result === 'OK') {
      this.$notify({
        title: '更新成功',
        message: '店铺信息已更新',
        type: 'success'
      });
      this.shop = { ...this.modifyShop };
    } else {
        this.$notify.error({
          title: '更新失败',
          message: result || '更新失败，请稍后重试'
        });
        this.modifyShop = { ...this.shop };
    }
  }

}
</script>

<style lang="scss" scoped>
.s_info_container {
  display: flex;
  .s_img {
    width: 200px;
    height: 250px;
    margin: 0 20px 20px 20px;
  }

  .s_info {
    position: relative;
    height: 250px;

    .s_name, .s_desc {
      font-size: 18px;  
    }

    .s_name {
      font-weight: bold;
      margin-bottom: 10px;
    }

    .bottom_container {
      position: absolute;
      bottom: 0;

      .s_sales_volumes {
        font-weight: bold;
        margin-bottom: 10px;
      }
      .sales_statistic_btns_g1, .sales_statistic_btns_g2 {
        display: flex;
      }

      .info_dialog_container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        
        .avatar-uploader {
          width: 178px;
          height: 178px;
          border: 1px dashed #d9d9d9;
          border-radius: 6px;
          cursor: pointer;
          position: relative;
          overflow: hidden;    
        }

        .avatar-uploader:hover {
          border-color: #409EFF;
        }

        .avatar-uploader-icon {
          font-size: 28px;
          color: #8c939d;
          width: 178px;
          height: 178px;
          line-height: 178px;
          text-align: center;
        }
        .avatar {
          width: 178px;
          height: 178px;
          display: block;
        }

        .info_name_input, .info_desc_input {
          width: 240px;
        }

        .p_info_new_type_input {
          width: 150px;
        }

        .p_info_new_type_stocks_input {
          width: 100px;
          margin-right: 10px;
        }

        .type_list {
          display: flex;
          width: 300px;
          justify-content: space-between;
        }
      }
    }
  }
}

.recent_sales_volumes_statistic {
  margin-top: 20px;

  .sales_table {
    margin-top: 10px;
  }
}
</style>
