<template>
  <el-card class="card" shadow="hover">
    <img class="image" :src="image" alt="product">
    <div class="name">{{ name }}</div>
    <div class="sales_volume">已卖 {{ salesVolume }} 件</div>
    <div class="shop">{{ shop }}</div>
  </el-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';

@Component({
  name: 'productCard'
})
export default class ProductCard extends Vue {

@Prop({ default: AppIcon }) readonly image?: any;
@Prop() readonly name!: string;
@Prop({default: 0 }) readonly salesVolume !: number;
@Prop() readonly shop?: string;

}
</script>

<style lang="scss" scoped>
.card {
  display: inline-block;
  width: 250px;
  height: 360px;
  
  .image {
    width: 200px;
    height: 250px;
    margin-bottom: 10px;
  }

  .name {
    font-size: 16px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  .sales_volume {
    font-size: 14px;
    font-weight: bold;
  }

  .shop {
    float: right;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
}
</style>