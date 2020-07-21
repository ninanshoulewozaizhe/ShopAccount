<template>
  <div>
    <div>
      <div class="card_wrapper"  v-for="product in showProducts" :key="product.id" @click="getProductDetail(product.id)">
        <product-card class="p_card"
          :name="product.name" 
          :shop="product.shop"
          :image="`/getImg?f=${product.img}`"
          :salesVolume="product.salesVolumes"></product-card>
      </div>
      <el-pagination class="pagination" layout="prev, pager, next" 
      :total="allProducts.length"
      :page-size="showPageSize"
      :current-page="curPage"
      @current-change="pageChange"
      v-if="allProducts.length != 0"></el-pagination>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';
import productCard from './productCard.vue';
import { IProductDetailItem } from '@/typing/productDetail/typings';
@Component({
  name: 'productList',
  components: {
    productCard
  }
})
export default class ProductList extends Vue {

@Prop() readonly allProducts!: IProductDetailItem[];
@Prop() readonly showPageSize!: number;

  showProducts: IProductDetailItem[] = [];
  curPage = 1;

  mounted() {
    this.showProductsInit();
  }

  showProductsInit() {
    for (let i = 0; i < this.showPageSize && i < this.allProducts.length; ++i) {
      this.showProducts.push(this.allProducts[i]);
    }
  }

  updateList() {
    this.pageChange(this.curPage);
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