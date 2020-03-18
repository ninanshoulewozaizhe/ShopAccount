<template>
    <div>
      <div class="chart_container">
        <div class="today_sales_statistics">
          <h3>今日销售情况</h3>
          <ve-histogram :data="todayChartData"></ve-histogram>
        </div>
        <div class="all_sales_statistics">
          <h3>总销售情况</h3>
          <ve-histogram :data="totalChartData"></ve-histogram>
        </div>
      </div>
      <div class="sales_detail_table">
        <h3>商品销量排行</h3>
        <el-table :data="tableData">
          <el-table-column prop="name" label="商品" width="250"></el-table-column>
          <el-table-column prop="salesVolumes" label="销量" width="180"></el-table-column>
          <el-table-column prop="shop" label="店铺" width="300"></el-table-column>
        </el-table>
      </div>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IProductItem } from '@/typing/home/typings';
import { IProductDetailItem } from '@/typing/productDetail/typings';

@Component({
  name: 'salesStatus'
})
export default class SalesStatus extends Vue {
  todayChartData = {
    columns: ['店铺', '销量'],
    rows: [
      { 店铺: '潮流最前线', 销量: 191},
      { 店铺: '喵喵之家', 销量: 121},
      { 店铺: '满天星', 销量: 142},
      { 店铺: '爱恋之城', 销量: 35}
    ]
  };

  totalChartData = {
    columns: ['店铺', '销量'],
    rows: [
      { 店铺: '潮流最前线', 销量: 876},
      { 店铺: '喵喵之家', 销量: 475},
      { 店铺: '满天星', 销量: 462},
      { 店铺: '爱恋之城', 销量: 233}
    ]
  };

  tableData: IProductItem[] = [
    {id: 1, name: '白色商务衬衫', salesVolumes: 266, sid: 1, shop: '潮流最前线'},
    {id: 2, name: '圆领夹克', salesVolumes: 156, sid: 1, shop: '潮流最前线'},
    {id: 3, name: '美国进口猫粮', salesVolumes: 132, sid: 2, shop: '喵喵之家'},
    {id: 4, name: '冰雪之心', salesVolumes: 122, sid: 4, shop: '爱恋之城'},
    {id: 5, name: '玫瑰花', salesVolumes: 101, sid: 3, shop: '满天星'},
    {id: 6, name: '美国进口狗粮', salesVolumes: 76, sid: 2, shop: '喵喵之家'},
    {id: 7, name: '丁香花', salesVolumes: 56, sid: 3, shop: '满天星'},
    {id: 8, name: '木质猫屋', salesVolumes: 42, sid: 2, shop: '喵喵之家'},
    {id: 9, name: '黑色嘻哈T恤', salesVolumes: 31, sid: 1, shop: '潮流最前线'},
    {id: 10, name: '木质猫屋', salesVolumes: 22, sid: 4, shop: '爱恋之城'}
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