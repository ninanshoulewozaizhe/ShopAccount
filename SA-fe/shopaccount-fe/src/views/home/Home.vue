<template>
    <div>
      <div>
        <product-card class="p_card" v-for="product in showProducts" 
        :key="product.id" 
        :name="product.name" 
        :shop="product.shop" 
        :salesVolume="product.salesVolume"></product-card>
      </div>
      <el-pagination class="pagination" layout="prev, pager, next" 
      :total="allProducts.length"
      :size="8"
      @current-change="pageChange"></el-pagination>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import productCard from '@/components/home/productCard.vue';
import { IProductItem } from './typings';

@Component({
  name: 'home',
  components: {
    productCard
  }
})
export default class Home extends Vue {
  allProducts: IProductItem[] = [
    {id: 1, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 2, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 3, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 4, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 5, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 6, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 7, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 8, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 9, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 10, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 11, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 12, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 13, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'},
    {id: 14, name: '韩版卫衣', salesVolume: 11, sid: 1, shop: '好再来服饰'}
  ];

  showProducts: IProductItem[] = [];
  showPageSize = 10;

  mounted() {
    this.showProductsInit();
  }

  showProductsInit() {
    for (let i = 0; i < this.showPageSize && i < this.allProducts.length; ++i) {
      this.showProducts.push(this.allProducts[i]);
    }
  }

  pageChange(curPage: number) {
    this.showProducts = [];
    for (let i = this.showPageSize * (curPage - 1), time = 0;
    time < this.showPageSize && i < this.allProducts.length; ++i, ++time) {
      this.showProducts.push(this.allProducts[i]);
    }
  }
}
</script>

<style lang="scss" scoped>
.p_card {
  margin-right: 20px;
  margin-bottom: 20px;
}

.pagination {
  float: right;
}
</style>