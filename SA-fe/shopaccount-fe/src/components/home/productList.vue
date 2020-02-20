<template>
  <div>
    <div>
      <div class="card_wrapper"  v-for="product in showProducts" :key="product.id" @click="getProductDetail(product.id)">
        <product-card class="p_card"
          :name="product.name" 
          :shop="product.shop" 
          :salesVolume="product.salesVolume"></product-card>
      </div>
      
    <el-pagination class="pagination" layout="prev, pager, next" 
    :total="allProducts.length"
    :page-size="showPageSize"
    @current-change="pageChange"></el-pagination>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IProductItem } from '@/typing/home/typings';
import AppIcon from '../../../public/images/accountBook.jpg';
import productCard from './productCard.vue';

@Component({
  name: 'productList',
  components: {
    productCard
  }
})
export default class ProductList extends Vue {

@Prop() readonly allProducts!: IProductItem[];
@Prop() readonly showPageSize!: number;

  showProducts: IProductItem[] = [];

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

  getProductDetail(pid: number) {
    this.$router.push({
      name: 'product-detail',
      params: {
        pid: String(pid)
      }
    });
  }

}
</script>

<style lang="scss" scoped>
.card_wrapper {
    display: inline-block;

    .p_card {
      margin-right: 20px;
      margin-bottom: 20px;
    }
  }

.pagination {
  text-align: right;
}
</style>