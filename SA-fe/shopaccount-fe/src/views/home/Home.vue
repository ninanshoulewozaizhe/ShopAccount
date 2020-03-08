<template>
    <div>
      <product-list 
      :allProducts="allProducts"
      :showPageSize="showPageSize"
      ></product-list>
      <div v-if="allProducts.length == 0">暂无店铺商品，请前往店铺列表选择店铺添加商品哦</div>        
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import productList from '@/components/home/productList.vue';
import { IProductItem } from '@/typing/home/typings';
import store from '@/store';
import { LOAD_ALL_PRODUCTS, GET_ALL_PRODUCTS } from '@/store/modules/product/constants';


@Component({
  name: 'home',
  components: {
    productList
  },
  async beforeRouteEnter(to: any, from: any, next: any) {
    await store.dispatch(`product/${LOAD_ALL_PRODUCTS}`);
    const products = store.getters[`product/${GET_ALL_PRODUCTS}`];
    console.log(products);
    next((vm: any) => {
      vm.allProducts = [ ...products ];
    });
  }
})
export default class Home extends Vue {
  allProducts: IProductItem[] = [];

  showPageSize = 10;

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