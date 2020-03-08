<template>
  <div>
      <div class="top_area">
      <h3>店铺列表</h3>
      <el-button class="add_new_shop" @click="addShopDialog = true">添加店铺</el-button>
        <el-dialog class="p_info_dialog" title="添加新店铺" :visible.sync="addShopDialog">
          <div class="p_info_dialog_container">
            <img class="p_info_img" :src="newShop.img" alt="p_img">
            <el-form>
              <el-form-item label="店铺名称">
                <el-input class="p_info_name_input"
                v-model="newShop.name"
                placeholder="请输入名称"></el-input>
              </el-form-item>
              <el-form-item label="店铺描述">
                <el-input
                  class="p_info_desc_input"
                  type="textarea"
                  :rows="2"
                  placeholder="请输入内容"
                  v-model="newShop.description">
                </el-input>
              </el-form-item>
            </el-form>
            （店内商品在店铺管理中添加）
          </div>
          <div slot="footer" class="dialog-footer">
            <el-button @click="cancelAddShop">取 消</el-button>
            <el-button type="primary" @click="addShopDialog = false">确 定</el-button>
          </div>
        </el-dialog>
    </div>
    <div  v-for="shop in showshops" :key="shop.id" @click="getShopDetail(shop.id)">
      <shop-card class="card"
      :shopImg="shop.img"
      :name="shop.name"
      :salesVolume="shop.salesVolume"
      :productAmount="shop.productAmount"
      :preProductImgs="preProductImgs"
      ></shop-card>
    </div>
    <el-pagination class="pagination" layout="prev, pager, next" 
      :total="shopList.length"
      :page-size="showPageSize"
      @current-change="pageChange"></el-pagination>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import shopCard from '@/components/shops/shopCard.vue';
import { IShopPreItem, IShopItem } from '@/typing/shops/typings';
import AppIcon from '../../../public/images/accountBook.jpg';
import store from '@/store';
import { LOAD_ALL_SHOPS, GET_ALL_SHOPS, ADD_NEW_SHOP } from '../../store/modules/shop/constants';
import { UID } from '@/store/modules/user/constants';

@Component({
  name: 'shops',
  components: {
      shopCard
  },
  async beforeRouteEnter(to: any, from: any, next: any) {
    await store.dispatch(`shop/${LOAD_ALL_SHOPS}`);
    const shops = store.getters[`shop/${GET_ALL_SHOPS}`];
    const USERID = store.getters[`user/${UID}`];
    console.log(shops);
    console.log(USERID);
    next((vm: any) => {
      vm.shopList = [ ...shops ];
      vm.USERID = USERID;
    });
  }
})
export default class Shops extends Vue {
  shopList: IShopPreItem[] = [];
  USERID = -1;
  preProductImgs: any[] = [AppIcon, AppIcon, AppIcon];
  showPageSize = 3;
  showshops: IShopPreItem[] = [];
  addShopDialog = false;
  newShop: IShopItem = {
    id: -1,
    uid: this.USERID,
    name: '',
    description: '',
    salesVolumes: 0,
    productAmount: 0,
    img: AppIcon
  };
  mounted() {
    this.showShopsInit();
  }

  showShopsInit() {
    for (let i = 0; i < this.showPageSize && i < this.shopList.length; ++i) {
      this.showshops.push(this.shopList[i]);
    }
  }

  pageChange(curPage: number) {
    this.showshops = [];
    for (let i = this.showPageSize * (curPage - 1), time = 0;
    time < this.showPageSize && i < this.shopList.length; ++i, ++time) {
      this.showshops.push(this.shopList[i]);
    }
  }

  getShopDetail(sid: number) {
    this.$router.push({
      name: 'shop-detail',
      params: {
        sid: String(sid)
      }
    });
  }

  newShopInfoClear() {
    this.newShop = {
      id: -1,
      uid: this.USERID,
      name: '',
      description: '',
      salesVolumes: 0,
      productAmount: 0,
      img: AppIcon
    };
  }

  cancelAddShop() {
    this.newShopInfoClear();
    this.addShopDialog = false;
  }

  async submitAddShop() {
    const fields = Object.freeze({ ...this.newShop });
    const result = await this.$store.dispatch(`shop/${ADD_NEW_SHOP}`, fields);
    if (result.status) {
      this.$notify({
        title: '创建成功',
        message: '新店铺已创建',
        type: 'success'
      });
      this.newShop.id = +result.sid;
      this.shopList.push({ ...this.newShop });
      this.newShopInfoClear();
    } else {
      this.$notify.error({
          title: '创建失败',
          message: '请稍后再试'
        });
    }
  }
}
</script>

<style lang="scss" scoped>
.top_area {
  position: relative;

  .add_new_shop {
    position: absolute;
    top: 0;
    left: 1000px;
  }
}

.card {
  margin-bottom: 20px;
}
.pagination {
  float: right;
}

.p_info_dialog_container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  
  .p_info_img {
    width: 200px;
    height: 250px;
    margin-bottom: 15px;
  }

  .p_info_name_input, .p_info_desc_input {
    width: 240px;
  }
}
</style>