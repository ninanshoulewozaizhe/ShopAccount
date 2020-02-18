<template>
  <div>
    <div class="top_area">
      <h3>店铺列表</h3>
      <el-button class="add_new_shop">添加店铺</el-button>
    </div>
    <div  v-for="shop in showshops" :key="shop.id" @click="getShopDetail(shop.id)">
      <shop-card class="card"
      :shopImg="shop.img"
      :name="shop.name"
      :salesVolume="shop.salesVolume"
      :productAmount="shop.productAmount"
      :preProductImgs="shop.preProductImgs"
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
import { IShopItem } from './typings';
import AppIcon from '../../../public/images/accountBook.jpg';

@Component({
  name: 'shops',
  components: {
      shopCard
  }
})
export default class Shops extends Vue {
  shopList: IShopItem[] = [
    {id: 1, img: AppIcon, name: 'nice', salesVolume: 1, productAmount: 10, preProductImgs: [AppIcon, AppIcon, AppIcon]},
    {id: 2, img: AppIcon, name: 'nice', salesVolume: 1, productAmount: 10, preProductImgs: [AppIcon, AppIcon, AppIcon]},
    {id: 3, img: AppIcon, name: 'nice', salesVolume: 1, productAmount: 10, preProductImgs: [AppIcon, AppIcon, AppIcon]},
    {id: 4, img: AppIcon, name: 'nice', salesVolume: 1, productAmount: 10, preProductImgs: [AppIcon, AppIcon, AppIcon]},
    {id: 5, img: AppIcon, name: 'nice', salesVolume: 1, productAmount: 10, preProductImgs: [AppIcon, AppIcon, AppIcon]}
  ];
  showPageSize = 3;
  showshops: IShopItem[] = [];

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
</style>