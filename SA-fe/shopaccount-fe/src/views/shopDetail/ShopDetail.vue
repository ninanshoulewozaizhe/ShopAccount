<template>
  <div>
    <div class="products_preview">
      <div>
        <h3>店内商品</h3>
      </div>
      <div class="products_container">
        <div class="card_wrapper" v-for="product in showProducts" 
          :key="product.id" @click="getProductDetail(product.id)">
          <product-card class="p_card"  
          :name="product.name"
          :image="`/getImg?f=${product.img}`"
          :salesVolume="product.salesVolumes"></product-card>
        </div>
        <div class="no_products_tips" v-if="!showProducts.length">
          店内暂无商品，请前往店铺管理添加商品。
        </div>
        <span class="product_get_more" @click="getShopManage">店铺管理>></span>
    </div>
    </div>
    <div class="shop_sales_statistics">
      <div class="products_sales_today">
        <h3>今日商品销量(总计: {{ productSalesVolumeToday }} 件)</h3>
        <el-table class="sales_show_table" :data="showTable" border>
          <el-table-column align="center" prop="pname" label="商品名称" width="300"></el-table-column>
          <el-table-column align="center" prop="salesVolumes" label="销量" ></el-table-column>
        </el-table>
        <el-pagination class="table_pagination" layout="prev, pager, next" 
        :total="allTableData.length"
        :page-size="showtableSize"
        @current-change="tablePageChange"></el-pagination>
      </div>
      <div class="products_sales_date">
        <h3>店铺销量统计</h3>
        <span>日期选择：</span>
        <el-date-picker
          v-model="salesDatePick"
          type="daterange"
          align="right"
          unlink-panels
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          :clearable="false"
          :picker-options="datePickerOptions"
          @change="datePickerChange">
        </el-date-picker>
        <ve-line :data="chartData"></ve-line>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';
import { IProductDetailItem, SalesChartRowItem,
  IndexOJ, SalesChartData } from '@/typing/productDetail/typings';
import { SalesRecordItem } from '@/typing/salesStatus/typings';
import productCard from '@/components/home/productCard.vue';
import store from '@/store';
import { LOAD_CUR_SHOP, GET_CUR_SHOP, ADD_NEW_SHOP } from '@/store/modules/shop/constants';
import { LOAD_CUR_SHOP_PRE_PRODUCTS, GET_CUR_SHOP_PRODUCTS } from '@/store/modules/product/constants';
import { LOAD_CUR_SHOP_TODAY_SALES, GET_CUR_SHOP_TODAY_SALES,
  LOAD_CUR_SHOP_PERIOD_SALES, GET_CUR_SHOP_PERIOD_SALES } from '@/store/modules/salesStatus/constants';

@Component({
  name: 'shopDetail',
  components: {
    productCard
  },
  async beforeRouteEnter(to: any, from: any, next: any) {
    const sid = to.params.sid;
    const todayStr = new Date().toISOString().split('T')[0];
    const weekAgoStr = new Date(+new Date() - 3600 * 1000 * 24 * 6).toISOString().split('T')[0];
    const dateStr = new Date().toISOString().split('T')[0];
    await store.dispatch(`product/${LOAD_CUR_SHOP_PRE_PRODUCTS}`, sid);
    await store.dispatch(`salesStatus/${LOAD_CUR_SHOP_TODAY_SALES}`, {sid, date: dateStr});
    await store.dispatch(`salesStatus/${LOAD_CUR_SHOP_PERIOD_SALES}`, {sid, from: weekAgoStr, to: todayStr});
    const products = store.getters[`product/${GET_CUR_SHOP_PRODUCTS}`];
    const todaySales = store.getters[`salesStatus/${GET_CUR_SHOP_TODAY_SALES}`];
    const chartRowRawData = store.getters[`salesStatus/${GET_CUR_SHOP_PERIOD_SALES}`];
    next((vm: any) => {
      vm.SID = sid;
      vm.showProducts = JSON.parse(JSON.stringify(products));
      vm.allTableData = JSON.parse(JSON.stringify(todaySales));
      vm.tableDataformat();
      vm.showTableInit();
      vm.chartDataInit(chartRowRawData, new Date(+new Date() - 3600 * 1000 * 24 * 6), new Date());
    });
  }
})
export default class ShopDetail extends Vue {
  allTableData: SalesRecordItem[] = [];
  showtableSize = 4;
  showTable: SalesRecordItem[]  = [];
  showProducts: IProductDetailItem[] = [];
  SID = -1;

  chartData: SalesChartData = {
    columns: ['日期', '销量'],
    rows: []
  };


  datePickerOptions = {
    shortcuts: [{
      text: '最近一周',
      onClick(picker: any) {
        const end = new Date();
        const start = new Date();
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 6);
        picker.$emit('pick', [start, end]);
      }
    }, {
      text: '最近一个月',
      onClick(picker: any) {
        const end = new Date();
        const start = new Date();
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
        picker.$emit('pick', [start, end]);
      }
    }],
    disabledDate(curDate: any) {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 31);
      return curDate < start || curDate > end;
    }
  };

  salesDatePick = [new Date(+new Date() - 3600 * 1000 * 24 * 6), new Date()];

  mounted() {
    this.showTableInit();
  }

  tableDataformat() {
    for (const record of this.allTableData) {
      if (typeof record.sales === 'string') {
        record.sales = JSON.parse(record.sales);
      }
      record.salesVolumes = Object.values(record.sales).reduce((pre: number, cur: number) => {
        return pre + cur;
      }, 0);
    }
  }

  showTableInit() {
    for (let i = 0; i < this.showtableSize && i < this.allTableData.length; ++i) {
      this.showTable.push(this.allTableData[i]);
    }
  }

  get productSalesVolumeToday() {
    return this.allTableData.reduce((pre, cur) => {
      if (cur.salesVolumes) {
        return pre + cur.salesVolumes;
      }
      return pre;
    }, 0);
  }

  tablePageChange(curPage: number) {
    this.showTable = [];
    for (let i = this.showtableSize * (curPage - 1), time = 0;
    time < this.showtableSize && i < this.allTableData.length; ++i, ++time) {
      this.showTable.push(this.allTableData[i]);
    }
  }

  async datePickerChange() {
    const fixDatePick = [new Date(+this.salesDatePick[0] + 3600 * 1000 * 24),
      new Date(+this.salesDatePick[1] + 3600 * 1000 * 24)];
    const from = fixDatePick[0].toISOString().split('T')[0];
    const to = fixDatePick[1].toISOString().split('T')[0];
    await this.$store.dispatch(`salesStatus/${LOAD_CUR_SHOP_PERIOD_SALES}`, {sid: this.SID, from, to});
    const data = store.getters[`salesStatus/${GET_CUR_SHOP_PERIOD_SALES}`];
    this.chartDataInit(data, fixDatePick[0], fixDatePick[1]);
    console.log(data);
  }

  chartDataInit(rowRawData: SalesRecordItem[], from: Date, to: Date) {
    const datePeriodObj: SalesChartRowItem[] = this.datePeriodObjInit(from, to);
    for (const record of rowRawData) {
      if (record) {
        for (const rowItem of datePeriodObj) {
          const rdate = new Date(record.date).toISOString().split('T')[0];
          if (rowItem.日期 === rdate) {
            if (typeof record.sales === 'string') {
              const data: IndexOJ = JSON.parse(record.sales);
              rowItem.销量 += Object.values(data).reduce((pre: number, cur: number) => {
                return pre + (+cur);
              }, 0);
            }
          }
        }
      }
    }
    this.$set(this.chartData, 'rows', datePeriodObj);
    console.log(this.chartData);
  }

  datePeriodObjInit(from: Date, to: Date): SalesChartRowItem[] {
    const datePeriodObj: SalesChartRowItem[] = [];
    let temp = from;
    const endDateStr = to.toISOString().split('T')[0];
    for (let i = 1; temp.toISOString().split('T')[0] <= endDateStr; ++i) {
      const tempRowItem: SalesChartRowItem = {
        日期: temp.toISOString().split('T')[0],
        销量: 0
      };
      datePeriodObj.push(tempRowItem);
      temp = new Date(+from + 3600 * 1000 * 24 * i);
    }
    return datePeriodObj;
  }

  getProductDetail(pid: number) {
    this.$router.push({
      name: 'product-detail',
      params: {
        pid: String(pid)
      }
    });
  }

  getShopManage() {
    const sid = this.$route.params.sid;
    this.$router.push({
      name: 'shop-manage',
      params: {
        sid: String(sid)
      }
    });
  }
}
</script>

<style lang="scss" scoped>
.products_preview {
  .card_wrapper {
    display: inline-block;

    .p_card {
      margin-right: 20px;
    }
  }
  
  .no_products_tips {
    margin-bottom: 10px;
  }
  .product_get_more {
    color: #20A4E5;
    position: relative;
    bottom: 3px;
  }

  .product_get_more:hover {
    font-weight: bold;
    cursor: pointer;
    
  }
}

.shop_sales_statistics {

  .products_sales_today {
    width: 40%;
  }

  .table_pagination {
    float: right;
    margin-top: 10px;
  }

  .products_sales_date {
    margin-top: 60px;

    span {
      font-weight: bold;
    }
  }
}
</style>