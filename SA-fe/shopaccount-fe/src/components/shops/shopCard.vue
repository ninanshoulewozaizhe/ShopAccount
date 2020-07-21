<template>
  <div>
    <el-card class="card" shadow="hover">
      <div class="card_body">
        <img class="shop_img" :src="`/getImg?f=${shopImg}`" alt="shopImg">
        <div class="shop_desc">
          <div class="shop_name">{{ name }}</div>
          <div class="shop_Pinfo">
            <span class="sales_volume">总销量:{{salesVolume}}</span>
            <span class="product_amount">共 {{ productAmount }} 件宝贝</span>
          </div>
        </div>
        <img class="shop_img p_img" v-for="(pImg, index) in preProductImgs" :key="index" :src="`/getImg?f=${pImg}`" alt="pImg">
      </div>
    </el-card>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';

@Component({
  name: 'shopCard'
})
export default class ShopCard extends Vue {

@Prop({ default: '' }) readonly shopImg?: any;
@Prop() readonly name!: string;
@Prop({default: 0 }) readonly salesVolume !: number;
@Prop({default: 0 }) readonly productAmount !: number;
@Prop() readonly preProductImgs!: any[];

}
</script>

<style lang="scss" scoped>

.card {
  width: 1150px;
}

.card_body {
  display: flex;
  flex-direction: row;

  .shop_img {
    height: 120px;
    width: 120px;
  }

  .shop_desc {
    position: relative;
    height: 110px;
    width: 200px;
    padding-top: 10px;
    margin-left: 20px;

    .shop_name {
      font-size: 20px;
    }

    .shop_Pinfo {
      position: absolute;
      bottom: 10px;
      width: 200px;
      .product_amount {
        float: right;
      }
    }
  }

  .p_img {
    margin-left: 40px;
  }
}
</style>