<template>
    <div>
      <div class="chart_container">
        <div class="today_sales_statistics">
          <h3>今日销售情况</h3>
          <ve-histogram :data="chartData"></ve-histogram>
        </div>
        <div class="all_sales_statistics">
          <h3>总销售情况</h3>
          <ve-histogram :data="chartData"></ve-histogram>
        </div>
      </div>
      <div class="sales_detail_table">
        <h3>商品销量排行</h3>
        <el-table :data="tableData">
          <el-table-column prop="name" label="商品" width="250"></el-table-column>
          <el-table-column prop="salesVolume" label="销量" width="180"></el-table-column>
          <el-table-column prop="shop" label="店铺" width="300"></el-table-column>
        </el-table>
      </div>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IProductItem } from '@/typing/home/typings';

@Component({
  name: 'salesStatus'
})
export default class SalesStatus extends Vue {
  chartData = {
    columns: ['店铺', '销量'],
    rows: [
      { 店铺: '1/1', 销量: 1393},
      { 店铺: '1/2', 销量: 3530},
      { 店铺: '1/3', 销量: 2923},
      { 店铺: '1/4', 销量: 1723},
      { 店铺: '1/5', 销量: 3792},
      { 店铺: '1/6', 销量: 4593}
    ]
  };
  tableData: IProductItem[] = [
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
}
</script>

<style lang="scss" scoped>
.chart_container {
  display: flex;
  .today_sales_statistics, .all_sales_statistics {
    width: 40%;
  }
  .today_sales_statistics {
    margin-right: 100px;
  }
}
</style>