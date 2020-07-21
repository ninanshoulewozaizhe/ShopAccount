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
import { IShopPreItem } from '@/typing/shops/typings';
import { IProductDetailItem, IndexOJ } from '@/typing/productDetail/typings';
import { SalesRecordItem, ShopsSalesItem,
  ShopSalesChartData, ShopSalesChartRowItem } from '@/typing/salesStatus/typings';
import store from '@/store';
import { LOAD_ALL_SHOPS, GET_ALL_SHOPS } from '@/store/modules/shop/constants';
import { LOAD_ALL_SHOPS_SALES_RANK, LOAD_ALL_SHOPS_TODAY_SALES,
  GET_ALL_SHOPS_SALES_RANK, GET_ALL_SHOPS_TODAY_SALES } from '@/store/modules/salesStatus/constants';

@Component({
  name: 'salesStatus',
  async beforeRouteEnter(to: any, from: any, next: any) {
    const dateStr = new Date().toISOString().split('T')[0];
    await store.dispatch(`salesStatus/${LOAD_ALL_SHOPS_TODAY_SALES}`, {date: dateStr});
    await store.dispatch(`shop/${LOAD_ALL_SHOPS}`);
    await store.dispatch(`salesStatus/${LOAD_ALL_SHOPS_SALES_RANK}`);
    const allShopsTodaySales = store.getters[`salesStatus/${GET_ALL_SHOPS_TODAY_SALES}`];
    const shops = store.getters[`shop/${GET_ALL_SHOPS}`];
    const allShopsSalesRank = store.getters[`salesStatus/${GET_ALL_SHOPS_SALES_RANK}`];
    console.log(allShopsTodaySales);
    console.log(shops);
    console.log(allShopsSalesRank);
    next((vm: any) => {
      vm.todayChartDataInit(allShopsTodaySales);
      vm.totalChartDataInit(shops);
      vm.tableData = [ ...allShopsSalesRank ].reverse();
    });
  }
})
export default class SalesStatus extends Vue {
  todayChartData: ShopSalesChartData = {
    columns: ['店铺', '销量'],
    rows: []
  };

  totalChartData: ShopSalesChartData = {
    columns: ['店铺', '销量'],
    rows: []
  };

  tableData: IProductDetailItem[] = [];

  todayChartDataInit(data: ShopsSalesItem) {
    Object.keys(data).map((key) => {
      const temp: ShopSalesChartRowItem = {
        店铺: key,
        销量: 0
      };
      for (const record of data[key]) {
        if (typeof record.sales === 'string') {
          const sales: IndexOJ = JSON.parse(record.sales);
          temp.销量 +=  Object.values(sales).reduce((pre: number, cur: number) => {
            return pre + (+cur);
          }, 0);
        }
      }
      this.todayChartData.rows.push(temp);
    });
  }

  totalChartDataInit(shops: IShopPreItem[]) {
    for (const shop of shops) {
      const temp: ShopSalesChartRowItem = {
        店铺: shop.name,
        销量: shop.salesVolumes
      };
      this.totalChartData.rows.push(temp);
    }
  }


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
.el-table::before {
  width: 0;
}
</style>
