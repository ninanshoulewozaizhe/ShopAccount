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
          <el-table-column prop="product" label="商品" width="250"></el-table-column>
          <el-table-column prop="salesVolume" label="销量" width="180"></el-table-column>
          <el-table-column prop="shop" label="店铺" width="300"></el-table-column>
        </el-table>
      </div>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

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
  tableData = [{
    product: '韩版卫衣',
    salesVolume: '11',
    shop: '上海市普陀区金沙江路 1518 弄'
  }, {
    product: '韩版卫衣',
    salesVolume: '11',
    shop: '上海市普陀区金沙江路 1517 弄'
  }, {
    product: '韩版卫衣',
    salesVolume: '11',
    shop: '上海市普陀区金沙江路 1519 弄'
  }, {
    product: '韩版卫衣',
    salesVolume: '11',
    shop: '上海市普陀区金沙江路 1516 弄'
  }];
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