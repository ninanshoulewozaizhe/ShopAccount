<template>
    <div>
      <product-list 
      :allProducts="allProducts"
      :showPageSize="showPageSize"
      ></product-list>        
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import productList from '@/components/home/productList.vue';
import { IProductItem } from '@/typing/home/typings';

@Component({
  name: 'home',
  components: {
    productList
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